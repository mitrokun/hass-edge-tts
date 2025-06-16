# --- START OF FILE stream_processor.py (ФИНАЛЬНАЯ УПРОЩЕННАЯ ВЕРСИЯ) ---

import asyncio
import re
import logging
import io
from typing import AsyncIterable, AsyncGenerator

try:
    import edge_tts
    import edge_tts.exceptions
    from edge_tts.communicate import remove_incompatible_characters
    from pydub import AudioSegment
except ImportError:
    def remove_incompatible_characters(text: str) -> str: return text
    pass

_LOGGER = logging.getLogger(__name__)


TRIM_MS_FROM_END = 750

class EdgeStreamProcessor:
    def __init__(self):
        pass

    async def _preprocess_stream(self, text_stream: AsyncIterable[str]) -> AsyncIterable[str]:
        """Cleans text by removing incompatible characters and custom markers."""
        async for chunk in text_stream:
            yield remove_incompatible_characters(chunk).replace('*', '')

    async def _sentence_generator(self, text_stream: AsyncIterable[str]) -> AsyncGenerator[str, None]:
        """Yields complete, speakable sentences from a text stream."""
        buffer = ""
        async for chunk in text_stream:
            buffer += chunk
            while True:
                sentence, rest = "", ""
                for punct in ".!?":
                    if punct in buffer:
                        sentence, rest = buffer.split(punct, 1)
                        sentence += punct; break
                if sentence:
                    if re.search(r'\w', sentence): yield sentence
                    buffer = rest
                elif len(buffer) >= 200:
                    if re.search(r'\w', buffer): yield buffer
                    buffer = ""
                else: break
        if buffer.strip() and re.search(r'\w', buffer.strip()):
            yield buffer.strip()

    def _trim_end_of_audio(self, audio_data: bytes) -> bytes:
        """
        Uses pydub to quickly trim a fixed amount of time from the end of an audio segment.
        This is a synchronous, CPU-bound function.
        """
        try:
            segment = AudioSegment.from_file(io.BytesIO(audio_data), format="mp3")
            if len(segment) <= TRIM_MS_FROM_END:
                return audio_data
            
            return segment[:-TRIM_MS_FROM_END].export(format="mp3").read()

        except Exception as e:
            _LOGGER.warning("Could not trim end of audio, returning original. Error: %s", e)
            return audio_data

    async def async_process_stream(
        self, text_stream: AsyncIterable[str], voice: str, rate: str, pitch: str, volume: str
    ) -> AsyncIterable[bytes]:
        """
        The main public method. It sets up a simplified processing pipeline
        that trims the end of EACH synthesized sentence for a seamless stream.
        """
        output_queue = asyncio.Queue(maxsize=10)

        processing_task = asyncio.create_task(
            self._process_all_text(text_stream, output_queue, voice, rate, pitch, volume)
        )

        while True:
            try:
                chunk = await output_queue.get()
                if chunk is None: break
                yield chunk
                output_queue.task_done()
            except asyncio.CancelledError: break
        
        if not processing_task.done():
            processing_task.cancel()
            await asyncio.sleep(0)

    async def _process_all_text(
        self, text_stream: AsyncIterable[str], output_queue: asyncio.Queue,
        voice: str, rate: str, pitch: str, volume: str
    ):
        try:
            sentences_generator = self._sentence_generator(self._preprocess_stream(text_stream))
            
            async for sentence in sentences_generator:
                try:
                    mp3_sentence_bytes = b''
                    async for audio_chunk in self._synthesize_and_stream(sentence, voice, rate, pitch, volume):
                        mp3_sentence_bytes += audio_chunk
                    
                    if not mp3_sentence_bytes:
                        continue

                    trimmed_mp3 = await asyncio.to_thread(self._trim_end_of_audio, mp3_sentence_bytes)
                    
                    if trimmed_mp3:
                        await output_queue.put(trimmed_mp3)

                except Exception as e:
                    _LOGGER.error("Failed to process sentence '%s': %s", sentence[:30], e)
        finally:
            await output_queue.put(None)

    async def _synthesize_and_stream(
        self, text: str, voice: str, rate: str, pitch: str, volume: str
    ) -> AsyncIterable[bytes]:
        """Synthesizes a single text string and yields audio chunks."""
        if not re.search(r'\w', text): return
        _LOGGER.debug("Synthesizing: %s", text[:50])
        try:
            communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch, volume=volume, proxy="")
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    yield chunk["data"]
        except Exception:
            _LOGGER.exception("Error during synthesis for text: %s", text[:50])