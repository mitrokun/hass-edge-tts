# --- START OF FILE stream_processor.py ---

import io
import re
import struct
import asyncio
import logging
from collections import deque
from typing import AsyncIterable, AsyncGenerator

try:
    import edge_tts
    import edge_tts.exceptions
    from edge_tts.communicate import remove_incompatible_characters
    from pydub import AudioSegment
except ImportError:
    def remove_incompatible_characters(text: str) -> str: return text
    AudioSegment = None
    pass

_LOGGER = logging.getLogger(__name__)

# Trim 750 ms from the end of each audio fragment, selected empirically
TRIM_MS_FROM_END = 750

# Delay between requests
SYNTHESIS_DELAY_S = 0.3

# Parallel api requests
CONCURRENCY_LIMIT = 3

# WAV
WAV_SAMPLE_RATE = 24000
WAV_BITS_PER_SAMPLE = 16
WAV_CHANNELS = 1

def create_wav_header(sample_rate: int, bits_per_sample: int, channels: int) -> bytes:
    """Creates a WAV header for streaming (unknown data size)."""
    chunk_size = 0xFFFFFFFF
    data_size = 0xFFFFFFFF
    byte_rate = sample_rate * channels * bits_per_sample // 8
    block_align = channels * bits_per_sample // 8
    header = struct.pack('<4sL4s4sLHHLLHH4sL',
                         b'RIFF', chunk_size, b'WAVE', b'fmt ',
                         16, 1, channels, sample_rate,
                         byte_rate, block_align, bits_per_sample,
                         b'data', data_size)
    return header

class EdgeStreamProcessor:
    """
    Handles the processing of text streams into audio streams (MP3 or WAV)
    using Microsoft Edge's TTS service.
    """

    def _find_sentence(self, buffer_text: str) -> tuple[str, str]:
        """
        Extracts the first complete sentence from the buffer.
        Handles decimal points inside numbers to avoid premature splitting.
        """
        if not buffer_text:
            return "", ""

        DECIMAL_PLACEHOLDER = "##DEC##"
        safe_text = re.sub(r'(\d)\.(\d)', fr'\1{DECIMAL_PLACEHOLDER}\2', buffer_text)

        match = re.search(r"[.!?]", safe_text)
        if match:
            end_index = match.start() + 1
            sentence_part, rest_part = safe_text[:end_index], safe_text[end_index:]
        else:
            max_chars = 200
            if len(safe_text) > max_chars:
                search_area = safe_text[:max_chars + 20]
                last_space_index = search_area.rfind(" ")
                if last_space_index > 0:
                    sentence_part, rest_part = safe_text[:last_space_index], safe_text[last_space_index:]
                else:
                    sentence_part, rest_part = safe_text[:max_chars], safe_text[max_chars:]
            else:
                return "", buffer_text # Not a full sentence and not too long, wait for more data

        final_sentence = sentence_part.replace(DECIMAL_PLACEHOLDER, '.').strip()
        final_rest = rest_part.replace(DECIMAL_PLACEHOLDER, '.').strip()
        return final_sentence, final_rest

    async def _sentence_generator(self, text_stream: AsyncIterable[str]) -> AsyncGenerator[str, None]:
        """Yields complete, speakable sentences from a raw text stream."""
        buffer = ""

        async for chunk in text_stream:
            buffer += chunk
            while True:
                sentence, rest = self._find_sentence(buffer)
                if sentence:
                    if re.search(r'\w', sentence):
                        yield sentence
                    buffer = rest
                else:
                    break
        if buffer.strip() and re.search(r'\w', buffer.strip()):
            yield buffer.strip()

    async def _synthesize_and_stream(
        self, text: str, voice: str, rate: str, pitch: str, volume: str
    ) -> AsyncIterable[bytes]:
        """Synthesizes a single text string and yields audio chunks."""
        _LOGGER.debug("Synthesizing: %s", text[:50])
        try:
            communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, volume=volume, proxy="")
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    yield chunk["data"]
        except Exception:
            _LOGGER.exception("Error during synthesis for text: %s", text[:50])

    async def _synthesize_and_process_sentence(
        self, sentence: str, voice: str, rate: str, pitch: str, volume: str
    ) -> AudioSegment | None:
        """
        Helper method that encapsulates the full processing pipeline for a single sentence.
        Returns a processed AudioSegment or None on failure.
        """
        clean_sentence = remove_incompatible_characters(sentence)
        clean_sentence = clean_sentence.replace('*', '')
        clean_sentence = re.sub(r'\s+', ' ', clean_sentence).strip()
        
        if not re.search(r'\w', clean_sentence):
            return None
        
        await asyncio.sleep(SYNTHESIS_DELAY_S)
        mp3_bytes = b''
        try:
            async for chunk in self._synthesize_and_stream(clean_sentence, voice, rate, pitch, volume):
                mp3_bytes += chunk
            
            if not mp3_bytes:
                _LOGGER.warning("TTS synthesis for sentence returned no data: %s", clean_sentence[:30])
                return None

            segment = await asyncio.to_thread(AudioSegment.from_file, io.BytesIO(mp3_bytes), format="mp3")
            
            if len(segment) > TRIM_MS_FROM_END:
                return segment[:-TRIM_MS_FROM_END]
            return segment
        except Exception as e:
            _LOGGER.warning("Could not process sentence '%s' into AudioSegment: %s", clean_sentence[:30], e)
            return None

    async def _generate_trimmed_segments(
        self, text_stream: AsyncIterable[str], voice: str, rate: str, pitch: str, volume: str
    ) -> AsyncGenerator[AudioSegment, None]:
        """
        An internal generator that processes a text stream to yield trimmed AudioSegments
        using a concurrent pipeline to hide latency.
        """
        sentences_generator = self._sentence_generator(text_stream)
        
        tasks = deque()

        async for sentence in sentences_generator:
            task = asyncio.create_task(
                self._synthesize_and_process_sentence(sentence, voice, rate, pitch, volume)
            )
            tasks.append(task)

            if len(tasks) >= CONCURRENCY_LIMIT:
                oldest_task = tasks.popleft()
                segment = await oldest_task
                if segment:
                    yield segment

        while tasks:
            task_to_finish = tasks.popleft()
            segment = await task_to_finish
            if segment:
                yield segment

    # --- Public-facing Methods ---

    async def async_process_to_single_file(
        self, text: str, voice: str, rate: str, pitch: str, volume: str
    ) -> bytes | None:
        """
        Processes a full text string into a single, seamless, and valid MP3 file.
        This is ideal for non-streaming use cases like caching.
        """
        _LOGGER.debug("Processing text to a single MP3 file.")
        async def text_stream(): yield text
        
        segments_generator = self._generate_trimmed_segments(text_stream(), voice, rate, pitch, volume)
        all_segments = [segment async for segment in segments_generator]

        if not all_segments:
            _LOGGER.error("No audio segments were generated for the text.")
            return None

        _LOGGER.debug("Joining %d audio segments into a single file.", len(all_segments))
        
        def join_and_export_segments():
            final_audio = sum(all_segments, AudioSegment.empty())
            if not final_audio:
                return None
            output_buffer = io.BytesIO()
            final_audio.export(output_buffer, format="mp3")
            return output_buffer.getvalue()

        try:
            return await asyncio.to_thread(join_and_export_segments)
        except Exception as e:
            _LOGGER.error("Failed to join and export final MP3 file: %s", e)
            return None

    async def async_process_stream_as_wav(
        self, text_stream: AsyncIterable[str], voice: str, rate: str, pitch: str, volume: str
    ) -> AsyncIterable[bytes]:
        """

        Processes a text stream into a valid, seamless, and uncompressed WAV audio stream.
        This is the recommended method for live streaming to clients.
        """
        _LOGGER.debug("Generating WAV stream with %d Hz, %d bit, %d channel(s)",
                      WAV_SAMPLE_RATE, WAV_BITS_PER_SAMPLE, WAV_CHANNELS)
        yield create_wav_header(WAV_SAMPLE_RATE, WAV_BITS_PER_SAMPLE, WAV_CHANNELS)

        segments_generator = self._generate_trimmed_segments(text_stream, voice, rate, pitch, volume)
        
        async for segment in segments_generator:
            def convert_to_pcm():
                standardized_segment = segment.set_frame_rate(WAV_SAMPLE_RATE) \
                                              .set_channels(WAV_CHANNELS) \
                                              .set_sample_width(WAV_BITS_PER_SAMPLE // 8)
                return standardized_segment.raw_data

            try:
                pcm_data = await asyncio.to_thread(convert_to_pcm)
                yield pcm_data
            except Exception as e:
                _LOGGER.warning("Could not convert AudioSegment to PCM data: %s", e)
                continue
