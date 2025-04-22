"""Sensor platform for OBIS Meter."""
import logging
from datetime import timedelta
import serial
import serial_asyncio
import re
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import (
    CONF_NAME,
    CONF_PORT,
    CONF_TIMEOUT,
    ELECTRIC_POTENTIAL_VOLT,
    ELECTRIC_CURRENT_AMPERE,
    POWER_WATT,
    ENERGY_KILO_WATT_HOUR,
)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from .const import (
    DOMAIN,
    CONF_BAUDRATE,
    CONF_BYTESIZE,
    CONF_PARITY,
    CONF_STOPBITS,
    DEFAULT_BAUDRATE,
    DEFAULT_BYTESIZE,
    DEFAULT_PARITY,
    DEFAULT_STOPBITS,
    DEFAULT_TIMEOUT,
)

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the OBIS Meter sensor platform from config entry."""
    config = config_entry.data
    port = config[CONF_PORT]
    name = config[CONF_NAME]
    baudrate = config.get(CONF_BAUDRATE, DEFAULT_BAUDRATE)
    bytesize = config.get(CONF_BYTESIZE, DEFAULT_BYTESIZE)
    parity = config.get(CONF_PARITY, DEFAULT_PARITY)
    stopbits = config.get(CONF_STOPBITS, DEFAULT_STOPBITS)
    timeout = config.get(CONF_TIMEOUT, DEFAULT_TIMEOUT)

    try:
        reader, writer = await serial_asyncio.open_serial_connection(
            url=port,
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
            timeout=timeout,
        )
    except serial.SerialException as exc:
        _LOGGER.error("Unable to connect to the OBIS Meter: %s", exc)
        return

    obis_meter = OBISMeter(reader, writer, name)
    await obis_meter.async_update()

    sensors = [
        OBISMeterSensor(obis_meter, "voltage", ELECTRIC_POTENTIAL_VOLT, "mdi:lightning-bolt"),
        OBISMeterSensor(obis_meter, "current", ELECTRIC_CURRENT_AMPERE, "mdi:current-ac"),
        OBISMeterSensor(obis_meter, "power", POWER_WATT, "mdi:flash"),
        OBISMeterSensor(obis_meter, "energy", ENERGY_KILO_WATT_HOUR, "mdi:counter"),
        OBISMeterSensor(obis_meter, "frequency", "Hz", "mdi:sine-wave"),
    ]

    async_add_entities(sensors, True)

class OBISMeter:
    """Representation of an OBIS Meter."""

    def __init__(self, reader, writer, name):
        """Initialize the OBIS Meter."""
        self._reader = reader
        self._writer = writer
        self._name = name
        self.data = {}

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Update the OBIS Meter data."""
        try:
            # Send identification request
            self._writer.write(b"/?!\r\n")
            await self._writer.drain()
            ident = await self._reader.readuntil(b"\r\n")
            
            # Send ACK and baud rate selection
            self._writer.write(b"\x06051\r\n")
            await self._writer.drain()
            
            # Read response
            response = await self._reader.readuntil(b"\x03")
            
            # Parse data for your meter
            self._parse_response(response.decode('ascii', errors='ignore'))
            
        except Exception as exc:
            _LOGGER.error("Error communicating with OBIS Meter: %s", exc)
            self.data = {}

    def _parse_response(self, response):
        """Parse the response from the meter."""
        self.data = {}
        
        # Voltage (example for string "0E0701FF(50.00)")
        if match := re.search(r'0E0701FF\(([\d.]+)\)', response):
            self.data["voltage"] = float(match.group(1))
        
        # Current (example for string "1F0700FF(000.512)")
        if match := re.search(r'1F0700FF\(([\d.]+)\)', response):
            self.data["current"] = float(match.group(1))
        
        # Power (example for string "100700FF(00456.0)")
        if match := re.search(r'100700FF\(([\d.]+)\)', response):
            self.data["power"] = float(match.group(1))
        
        # Energy (example for string "0F0880FF(002094.68,...)")
        if match := re.search(r'0F0880FF\(([\d.]+)', response):
            self.data["energy"] = float(match.group(1))
        
        # Frequency (example for string "0D07FFFF(10.986)")
        if match := re.search(r'0D07FFFF\(([\d.]+)\)', response):
            self.data["frequency"] = float(match.group(1))

class OBISMeterSensor(SensorEntity):
    """Representation of a sensor from an OBIS Meter."""

    def __init__(self, obis_meter, parameter, unit, icon):
        """Initialize the sensor."""
        self._obis_meter = obis_meter
        self._parameter = parameter
        self._attr_unit_of_measurement = unit
        self._attr_icon = icon
        self._attr_name = f"{obis_meter._name} {parameter}"
        self._attr_unique_id = f"{obis_meter._name}_{parameter}"
        self._attr_should_poll = True

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._obis_meter.data.get(self._parameter)

    async def async_update(self):
        """Get the latest data from the OBIS Meter."""
        await self._obis_meter.async_update()