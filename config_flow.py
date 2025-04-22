"""Config flow for OBIS Meter integration."""
from __future__ import annotations

import voluptuous as vol
from serial import SerialException
import serial_asyncio

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    DEFAULT_NAME,
    DEFAULT_BAUDRATE,
    DEFAULT_BYTESIZE,
    DEFAULT_PARITY,
    DEFAULT_STOPBITS,
    DEFAULT_TIMEOUT,
    DEFAULT_SCAN_INTERVAL,
    CONF_NAME,
    CONF_PORT,
    CONF_BAUDRATE,
    CONF_BYTESIZE,
    CONF_PARITY,
    CONF_STOPBITS,
    CONF_TIMEOUT,
    CONF_SCAN_INTERVAL,
    PARITY_OPTIONS,
    BYTESIZE_OPTIONS,
    STOPBITS_OPTIONS,
)

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
    vol.Required(CONF_PORT): str,
    vol.Optional(CONF_BAUDRATE, default=DEFAULT_BAUDRATE): int,
    vol.Optional(CONF_BYTESIZE, default=DEFAULT_BYTESIZE): vol.In(BYTESIZE_OPTIONS),
    vol.Optional(CONF_PARITY, default=DEFAULT_PARITY): vol.In(PARITY_OPTIONS),
    vol.Optional(CONF_STOPBITS, default=DEFAULT_STOPBITS): vol.In(STOPBITS_OPTIONS),
    vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): int,
    vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_SCAN_INTERVAL): int,
})

class ObisMeterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for OBIS Meter."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        
        if user_input is not None:
            try:
                # Test connection
                reader, writer = await serial_asyncio.open_serial_connection(
                    url=user_input[CONF_PORT],
                    baudrate=user_input[CONF_BAUDRATE],
                    bytesize=user_input[CONF_BYTESIZE],
                    parity=user_input[CONF_PARITY],
                    stopbits=user_input[CONF_STOPBITS],
                    timeout=user_input[CONF_TIMEOUT],
                )
                writer.close()
                await writer.wait_closed()
                
                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input
                )
                
            except SerialException:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> ObisMeterOptionsFlow:
        """Get the options flow for this handler."""
        return ObisMeterOptionsFlow(config_entry)

class ObisMeterOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for OBIS Meter."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    CONF_BAUDRATE,
                    default=self.config_entry.options.get(CONF_BAUDRATE, self.config_entry.data[CONF_BAUDRATE])
                ): int,
                vol.Optional(
                    CONF_BYTESIZE,
                    default=self.config_entry.options.get(CONF_BYTESIZE, self.config_entry.data[CONF_BYTESIZE])
                ): vol.In(BYTESIZE_OPTIONS),
                vol.Optional(
                    CONF_PARITY,
                    default=self.config_entry.options.get(CONF_PARITY, self.config_entry.data[CONF_PARITY])
                ): vol.In(PARITY_OPTIONS),
                vol.Optional(
                    CONF_STOPBITS,
                    default=self.config_entry.options.get(CONF_STOPBITS, self.config_entry.data[CONF_STOPBITS])
                ): vol.In(STOPBITS_OPTIONS),
                vol.Optional(
                    CONF_TIMEOUT,
                    default=self.config_entry.options.get(CONF_TIMEOUT, self.config_entry.data[CONF_TIMEOUT])
                ): int,
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=self.config_entry.options.get(CONF_SCAN_INTERVAL, self.config_entry.data[CONF_SCAN_INTERVAL])
                ): int,
            })
        )