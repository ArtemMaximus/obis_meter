"""Initialize the Neva MT Counter component."""
from .const import DOMAIN

async def async_setup(hass, config):
    """Set up the Neva MT Counter component from configuration.yaml."""
    if DOMAIN not in config:
        return True

    # Создаем Config Entry из YAML-конфигурации
    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": "yaml"},
            data=config[DOMAIN],
        )
    )

    return True

async def async_setup_entry(hass, entry):
    """Set up Neva MT Counter from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    return True
