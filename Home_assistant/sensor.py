import logging
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

DOMAIN = "neva_mt"

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Neva MT sensors based on a config entry."""
    from .neva_commands import NevaCommands  # Импортируем новый класс

    port = entry.data["port"]  # Порт для подключения к счетчику

    # Создаем экземпляр класса NevaCommands
    neva_commands = NevaCommands(port)

    async def async_update_data():
        """Fetch data from the counter."""
        return await hass.async_add_executor_job(neva_commands.read_all_parameters)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name=f"neva_mt_{port}",  # Добавляем порт в название координатора
        update_method=async_update_data,
        update_interval=timedelta(seconds=30),  # Интервал обновления данных
    )

    await coordinator.async_config_entry_first_refresh()

    sensors = [
        NevaMTSensor(coordinator, f"{port}_voltage_phase_a", "Voltage Phase A", SensorDeviceClass.VOLTAGE, "V"),
        NevaMTSensor(coordinator, f"{port}_voltage_phase_b", "Voltage Phase B", SensorDeviceClass.VOLTAGE, "V"),
        NevaMTSensor(coordinator, f"{port}_voltage_phase_c", "Voltage Phase C", SensorDeviceClass.VOLTAGE, "V"),
        NevaMTSensor(coordinator, f"{port}_current_phase_a", "Current Phase A", SensorDeviceClass.CURRENT, "A"),
        NevaMTSensor(coordinator, f"{port}_current_phase_b", "Current Phase B", SensorDeviceClass.CURRENT, "A"),
        NevaMTSensor(coordinator, f"{port}_current_phase_c", "Current Phase C", SensorDeviceClass.CURRENT, "A"),
        NevaMTSensor(coordinator, f"{port}_frequency", "Frequency", SensorDeviceClass.FREQUENCY, "Hz"),
        NevaMTSensor(coordinator, f"{port}_battery_level", "Battery Level", SensorDeviceClass.BATTERY, "%"),
        NevaMTSensor(coordinator, f"{port}_energy_t1", "Energy T1", SensorDeviceClass.ENERGY, "kWh"),
        NevaMTSensor(coordinator, f"{port}_energy_t2", "Energy T2", SensorDeviceClass.ENERGY, "kWh"),
        NevaMTSensor(coordinator, f"{port}_date_time", "Date and Time", SensorDeviceClass.TIMESTAMP, None),
    ]

    async_add_entities(sensors)

class NevaMTSensor(SensorEntity):
    """Representation of a Neva MT sensor."""

    def __init__(self, coordinator, unique_id, name, device_class, unit_of_measurement):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._unique_id = unique_id
        self._name = name
        self._device_class = device_class
        self._unit_of_measurement = unit_of_measurement

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return self._unique_id

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return self._device_class

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self._unique_id.split("_")[-1])

    @property
    def available(self):
        """Return if the sensor is available."""
        return self.coordinator.last_update_success

    async def async_update(self):
        """Update the sensor."""
        await self.coordinator.async_request_refresh()