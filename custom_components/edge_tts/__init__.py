# --- START OF FILE __init__.py ---

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .stream_processor import EdgeStreamProcessor

PLATFORMS: list[str] = ["tts"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Edge TTS from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    processor = EdgeStreamProcessor()
    
    hass.data[DOMAIN][entry.entry_id] = {
        "processor": processor,
    }

    async def warm_up_tts(hass_ref: HomeAssistant):
        """
        Performs a 'dummy' TTS request to initialize connections
        and avoid blocking calls on the first real request.
        """
        async def dummy_stream():
            yield "init"

        audio_generator = processor.async_process_stream(
            dummy_stream(),
            voice="en-US-JennyNeural",
            rate="+0%",
            pitch="+0Hz",
            volume="+0%"
        )

        try:
            async for _ in audio_generator:
                pass
        except Exception:
            pass


    hass.async_create_task(warm_up_tts(hass))

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry when options are updated."""
    await hass.config_entries.async_reload(entry.entry_id)