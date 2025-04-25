import logging
from homeassistant import config_entries
import voluptuous as vol

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class NevaMTConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Neva MT Counter."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate user input here (e.g., check if port exists)
            return self.async_create_entry(title="Neva MT", data=user_input)

        data_schema = {
            vol.Required("port"): str,
        }

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(data_schema),
            errors=errors,
        )