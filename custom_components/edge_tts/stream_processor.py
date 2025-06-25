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
    # Заглушки, чтобы код оставался синтаксически верным.
    def remove_incompatible_characters(text: str) -> str: return text
    pass

_LOGGER = logging.getLogger(__name__)

# Количество миллисекунд, которое мы отрезаем с конца каждого фрагмента
TRIM_MS_FROM_END = 750

SYNTHESIS_DELAY_S = 0.1

class EdgeStreamProcessor:
    def __init__(self):
        pass

    async def _preprocess_stream(self, text_stream: AsyncIterable[str]) -> AsyncIterable[str]:
        """Cleans text by removing incompatible characters and custom markers."""
        async for chunk in text_stream:
            yield remove_incompatible_characters(chunk).replace('*', '')

    def _find_sentence(self, buffer_text: str) -> tuple[str, str]:
        """
        Extracts the first complete sentence from the buffer using a language-agnostic
        approach for decimal points.
        """
        if not buffer_text:
            return "", ""

        # Use a unique placeholder to temporarily replace decimal points within numbers.
        DECIMAL_PLACEHOLDER = "##DEC##"
        safe_text = re.sub(r'(\d)\.(\d)', fr'\1{DECIMAL_PLACEHOLDER}\2', buffer_text)

        match = re.search(r"[.!?]", safe_text)
        if match:
            end_index = match.start() + 1
            sentence_part = safe_text[:end_index]
            rest_part = safe_text[end_index:]
            
            final_sentence = sentence_part.replace(DECIMAL_PLACEHOLDER, '.')
            final_rest = rest_part.replace(DECIMAL_PLACEHOLDER, '.')
            
            return final_sentence.strip(), final_rest.strip()

        max_chars = 200
        if len(safe_text) > max_chars:
            search_area = safe_text[:max_chars + 20]
            last_space_index = search_area.rfind(" ")
            if last_space_index > 0:
                sentence_part = safe_text[:last_space_index]
                rest_part = safe_text[last_space_index:]
            else: # Force split if no space is found
                sentence_part = safe_text[:max_chars]
                rest_part = safe_text[max_chars:]

            final_sentence = sentence_part.replace(DECIMAL_PLACEHOLDER, '.')
            final_rest = rest_part.replace(DECIMAL_PLACEHOLDER, '.')
            return final_sentence.strip(), final_rest.strip()

        # If no sentence end is found and text is not too long, it's a remainder.
        return "", buffer_text

    async def _sentence_generator(self, text_stream: AsyncIterable[str]) -> AsyncGenerator[str, None]:
        """Yields complete, speakable sentences from a text stream."""
        buffer = ""
        async for chunk in text_stream:
            buffer += chunk
            while True:
                # Используем наш новый надежный метод
                sentence, rest = self._find_sentence(buffer)
                
                if sentence:
                    if re.search(r'\w', sentence):
                        yield sentence
                    buffer = rest
                else:
                    # Если предложение не найдено, ждем новых данных
                    break
                    
        # Обрабатываем остаток в буфере после окончания потока
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
                # Добавляем небольшую задержку между запросами к TTS-серверу.
                await asyncio.sleep(SYNTHESIS_DELAY_S)

                try:
                    mp3_sentence_bytes = b''
                    async for audio_chunk in self._synthesize_and_stream(sentence, voice, rate, pitch, volume):
                        mp3_sentence_bytes += audio_chunk
                    
                    if not mp3_sentence_bytes:
                        continue

                    # БЕЗУСЛОВНО обрезаем конец КАЖДОГО сгенерированного фрагмента.
                    trimmed_mp3 = await asyncio.to_thread(self._trim_end_of_audio, mp3_sentence_bytes)
                    
                    if trimmed_mp3:
                        await output_queue.put(trimmed_mp3)

                except Exception as e:
                    _LOGGER.error("Failed to process sentence '%s': %s", sentence[:30], e)
        finally:
            # Сигнализируем, что поток данных завершен
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

    async def async_process_to_single_file(
        self, text: str, voice: str, rate: str, pitch: str, volume: str
    ) -> bytes | None:
        """
        Processes a full text string into a single, seamless, and valid MP3 file.
        This method is for non-streaming use cases (e.g., caching).
        It synthesizes each sentence, trims the end, and then properly joins them
        using pydub to ensure a single valid MP3 header in the final output.
        """
        _LOGGER.debug("Processing text to a single file.")

        # Шаг 1: Разделение текста на предложения с помощью нашего существующего генератора.
        # Мы создаем временный "stream" из одного куска текста.
        async def text_stream():
            yield text
        
        sentences_generator = self._sentence_generator(self._preprocess_stream(text_stream()))
        
        # Шаг 2: Синтез и сборка AudioSegment'ов для каждого предложения.
        all_segments = []
        try:
            async for sentence in sentences_generator:
                if not sentence.strip():
                    continue

                # Добавляем задержку, чтобы не перегружать TTS-сервер
                await asyncio.sleep(SYNTHESIS_DELAY_S)
                
                # Синтезируем предложение в байты
                mp3_sentence_bytes = b''
                try:
                    async for audio_chunk in self._synthesize_and_stream(sentence, voice, rate, pitch, volume):
                        mp3_sentence_bytes += audio_chunk
                    
                    if not mp3_sentence_bytes:
                        _LOGGER.warning("TTS synthesis for sentence returned no data: %s", sentence[:30])
                        continue

                    # Преобразуем байты в AudioSegment и сразу обрезаем
                    segment = await asyncio.to_thread(
                        AudioSegment.from_file, io.BytesIO(mp3_sentence_bytes), format="mp3"
                    )
                    
                    if len(segment) > TRIM_MS_FROM_END:
                        trimmed_segment = segment[:-TRIM_MS_FROM_END]
                        all_segments.append(trimmed_segment)
                    else:
                        all_segments.append(segment) # Добавляем как есть, если короче обрезки
                
                except Exception as e:
                    _LOGGER.warning("Failed to process sentence '%s' for single file: %s", sentence[:30], e)
                    # Продолжаем со следующим предложением, не прерывая весь процесс
                    continue
        except Exception as e:
            _LOGGER.error("Error in sentence generator during single file processing: %s", e)
            return None

        if not all_segments:
            _LOGGER.error("No audio segments were generated for the text.")
            return None

        # Шаг 3: "Сложение" всех сегментов в один и экспорт.
        _LOGGER.debug("Joining %d audio segments into a single file.", len(all_segments))
        
        def join_and_export_segments():
            final_audio = sum(all_segments, AudioSegment.empty())            
            output_buffer = io.BytesIO()
            final_audio.export(output_buffer, format="mp3")
            return output_buffer.getvalue()

        try:
            final_mp3_bytes = await asyncio.to_thread(join_and_export_segments)
            return final_mp3_bytes
        except Exception as e:
            _LOGGER.error("Failed to join and export final audio file: %s", e)
            return None
