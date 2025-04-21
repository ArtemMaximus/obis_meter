"""Config flow for OBIS Meter integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
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
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_NAME],
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return ObisMeterOptionsFlow(config_entry)

class ObisMeterOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for OBIS Meter."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    CONF_BAUDRATE,
                    default=self.config_entry.options.get(CONF_BAUDRATE, DEFAULT_BAUDRATE)
                ): int,
                vol.Optional(
                    CONF_BYTESIZE,
                    default=self.config_entry.options.get(CONF_BYTESIZE, DEFAULT_BYTESIZE)
                ): vol.In(BYTESIZE_OPTIONS),
                vol.Optional(
                    CONF_PARITY,
                    default=self.config_entry.options.get(CONF_PARITY, DEFAULT_PARITY)
                ): vol.In(PARITY_OPTIONS),
                vol.Optional(
                    CONF_STOPBITS,
                    default=self.config_entry.options.get(CONF_STOPBITS, DEFAULT_STOPBITS)
                ): vol.In(STOPBITS_OPTIONS),
                vol.Optional(
                    CONF_TIMEOUT,
                    default=self.config_entry.options.get(CONF_TIMEOUT, DEFAULT_TIMEOUT)
                ): int,
                vol.Optional(
                    CONF_SCAN_INTERVAL,
                    default=self.config_entry.options.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL)
                ): int,
            })
        )