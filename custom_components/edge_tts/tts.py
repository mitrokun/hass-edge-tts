# --- START OF FILE tts.py ---

import logging
from collections import defaultdict
from typing import Any

from homeassistant.components.tts import (
    ATTR_VOICE,
    TextToSpeechEntity,
    TTSAudioRequest,
    TTSAudioResponse,
    Voice,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    CONF_LANG,
    DEFAULT_LANG,
    CONF_VOICE,
    DEFAULT_VOICE,
    CONF_RATE,
    DEFAULT_RATE,
    CONF_VOLUME,
    DEFAULT_VOLUME,
    CONF_PITCH,
    DEFAULT_PITCH,
)
from .voices import SUPPORTED_VOICES
from .stream_processor import EdgeStreamProcessor

EDGE_TTS_VERSION = '7.0.2'
try:
    import edge_tts
    if '__version__' not in dir(edge_tts) or edge_tts.__version__ != EDGE_TTS_VERSION:
        raise Exception(f"edge_tts version is not {EDGE_TTS_VERSION}. Please install edge_tts {EDGE_TTS_VERSION}.")
    import edge_tts.exceptions
except ImportError:
    try:
        import edgeTTS
        raise Exception(f'Please uninstall edgeTTS and install edge_tts {EDGE_TTS_VERSION} instead.')
    except ImportError:
        raise Exception(f'edge_tts is required. Please install edge_tts {EDGE_TTS_VERSION}.')

_LOGGER = logging.getLogger(__name__)


def _prepare_voice_data(source_voices: dict[str, str]) -> tuple[dict, list, list]:
    """Преобразует исходный словарь голосов в структуры, удобные для HA."""
    grouped_voices = defaultdict(list)
    for voice_id, lang_code in source_voices.items():
        friendly_name = voice_id.replace(f"{lang_code}-", "", 1)
        grouped_voices[lang_code].append((friendly_name, voice_id))

    voices_by_lang = {
        lang: sorted(voices) for lang, voices in grouped_voices.items()
    }
    
    all_languages = sorted(voices_by_lang.keys())
    all_voice_ids = sorted(source_voices.keys())

    return voices_by_lang, all_languages, all_voice_ids


VOICES_BY_LANG, ALL_SUPPORTED_LANGUAGES, ALL_SUPPORTED_VOICES = _prepare_voice_data(SUPPORTED_VOICES)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Edge TTS from a config entry."""
    processor = hass.data[DOMAIN][config_entry.entry_id]["processor"]
    async_add_entities([EdgeTtsEntity(config_entry, processor)])


class EdgeTtsEntity(TextToSpeechEntity):
    """The Edge TTS entity."""

    def __init__(self, config_entry: ConfigEntry, processor: EdgeStreamProcessor):
        """Initialize the entity."""
        self._config_entry = config_entry
        self._processor = processor
        self._attr_name = "Edge TTS"
        self._attr_unique_id = config_entry.entry_id

    @property
    def default_language(self) -> str:
        """Return the default language from config options."""
        return self._config_entry.options.get(CONF_LANG, DEFAULT_LANG)

    @property
    def supported_languages(self) -> list[str]:
        """Return list of supported languages."""
        return ALL_SUPPORTED_LANGUAGES

    @property
    def supported_options(self) -> list[str]:
        """Return a list of supported options."""
        return [ATTR_VOICE, 'pitch', 'rate', 'volume']
    
    @property
    def default_options(self) -> dict[str, Any]:
        """Return a dict including default options."""
        return {
            ATTR_VOICE: self._config_entry.options.get(CONF_VOICE, DEFAULT_VOICE)
        }

    @callback
    def async_get_supported_voices(self, language: str) -> list[Voice] | None:
        """Return a list of supported voices for a language."""
        if not (voices := VOICES_BY_LANG.get(language)):
            return None
        return [Voice(voice_id, name) for name, voice_id in voices]

    def _format_param(self, value: Any, suffix: str) -> str:
        """Formats a numeric or string value into the required string format for edge-tts."""
        try:
            numeric_value = int(value)
            return f"{numeric_value:+d}{suffix}"
        except (ValueError, TypeError):
            return str(value)

    def _get_tts_params(self, language: str, options: dict) -> dict:
        """Helper to determine voice and other params from options."""
        conf = {**self._config_entry.options, **options}
        
        voice = conf.get(ATTR_VOICE)
        if not voice:
            default_voice_tuple = VOICES_BY_LANG.get(language, [("", DEFAULT_VOICE)])[0]
            voice = default_voice_tuple[1]

        return {
            "voice": voice,
            "rate": self._format_param(conf.get("rate", DEFAULT_RATE), "%"),
            "volume": self._format_param(conf.get("volume", DEFAULT_VOLUME), "%"),
            "pitch": self._format_param(conf.get("pitch", DEFAULT_PITCH), "Hz"),
        }

    async def async_get_tts_audio(
        self, message: str, language: str, options: dict | None = None
    ) -> tuple[str, bytes | None]:
        options = options or {}
        params = self._get_tts_params(language, options)
        _LOGGER.debug("Requesting non-streaming audio with params: %s", params)
        async def single_message_stream():
            yield message
        audio_generator = self._processor.async_process_stream(single_message_stream(), **params)
        try:
            mp3_chunks = [chunk async for chunk in audio_generator]
            if not mp3_chunks:
                _LOGGER.error("TTS synthesis failed to produce any audio for message: %s", message[:100])
                return "mp3", None
            return "mp3", b"".join(mp3_chunks)
        except Exception as e:
            _LOGGER.error("Error during non-streaming TTS audio generation: %s", e)
            return "mp3", None

    async def async_stream_tts_audio(self, request: TTSAudioRequest) -> TTSAudioResponse:
        params = self._get_tts_params(request.language, request.options)
        _LOGGER.debug("Requesting streaming audio with params: %s", params)
        audio_generator = self._processor.async_process_stream(request.message_gen, **params)
        return TTSAudioResponse(extension="mp3", data_gen=audio_generator)
