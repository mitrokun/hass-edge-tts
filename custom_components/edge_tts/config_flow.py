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

from .const import (
    DOMAIN,
    CONF_LANG, 
    CONF_RATE,
    CONF_VOLUME,
    CONF_PITCH,
    DEFAULT_LANG,
    DEFAULT_RATE,
    DEFAULT_VOLUME,
    DEFAULT_PITCH,
)


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
        # Может быть только одна запись Edge TTS
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

        # Создаем схему для формы настроек
        schema = vol.Schema(
            {
                vol.Optional(
                    CONF_LANG,
                    description={"suggested_value": self.options.get(CONF_LANG)},
                    default=DEFAULT_LANG,
                ): str,
                vol.Optional(
                    CONF_RATE,
                    description={"suggested_value": self.options.get(CONF_RATE)},
                    default=DEFAULT_RATE,
                ): str,
                vol.Optional(
                    CONF_VOLUME,
                    description={"suggested_value": self.options.get(CONF_VOLUME)},
                    default=DEFAULT_VOLUME,
                ): str,
                vol.Optional(
                    CONF_PITCH,
                    description={"suggested_value": self.options.get(CONF_PITCH)},
                    default=DEFAULT_PITCH,
                ): str,
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
