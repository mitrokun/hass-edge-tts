# --- START OF FILE config_flow.py ---

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import (
    ConfigEntry,
    ConfigFlow,
    ConfigFlowResult,
    OptionsFlowWithConfigEntry,
)
from homeassistant.core import callback
from homeassistant.helpers.selector import selector

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
from .tts import ALL_SUPPORTED_LANGUAGES, ALL_SUPPORTED_VOICES


class EdgeTtsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Edge TTS."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> OptionsFlowWithConfigEntry:
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        if user_input is not None:
            return self.async_create_entry(title="Edge TTS", data={})

        return self.async_show_form(step_id="user")


class OptionsFlowHandler(OptionsFlowWithConfigEntry):
    """Handle an options flow for Edge TTS."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Optional(
                    CONF_LANG,
                    default=self.options.get(CONF_LANG, DEFAULT_LANG),
                ): selector({
                    "select": {
                        "options": ALL_SUPPORTED_LANGUAGES,
                        "mode": "dropdown",
                    }
                }),
                vol.Optional(
                    CONF_VOICE,
                    default=self.options.get(CONF_VOICE, DEFAULT_VOICE),
                ): selector({
                    "select": {
                        "options": ALL_SUPPORTED_VOICES,
                        "mode": "dropdown",
                    }
                }),
                vol.Optional(
                    CONF_RATE,
                    default=self.options.get(CONF_RATE, DEFAULT_RATE),
                ): selector({
                    "number": {
                        "min": -100,
                        "max": 100,
                        "step": 1,
                        "mode": "slider",
                        "unit_of_measurement": "%",
                    }
                }),
                vol.Optional(
                    CONF_VOLUME,
                    default=self.options.get(CONF_VOLUME, DEFAULT_VOLUME),
                ): selector({
                    "number": {
                        "min": -100,
                        "max": 100,
                        "step": 1,
                        "mode": "slider",
                        "unit_of_measurement": "%",
                    }
                }),
                vol.Optional(
                    CONF_PITCH,
                    default=self.options.get(CONF_PITCH, DEFAULT_PITCH),
                ): selector({
                    "number": {
                        "min": -100,
                        "max": 100,
                        "step": 1,
                        "mode": "slider",
                        "unit_of_measurement": "Hz",
                    }
                }),
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
