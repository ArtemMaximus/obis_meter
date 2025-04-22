"""Constants for OBIS Meter integration."""
from homeassistant.const import (
    CONF_NAME,
    CONF_PORT,
    CONF_TIMEOUT,
)

DOMAIN = "obis_meter"
PLATFORMS = ["sensor"]

DEFAULT_NAME = "OBIS Meter"
DEFAULT_TIMEOUT = 10
DEFAULT_SCAN_INTERVAL = 30
DEFAULT_BAUDRATE = 9600
DEFAULT_BYTESIZE = 7
DEFAULT_PARITY = "E"
DEFAULT_STOPBITS = 1

CONF_BAUDRATE = "baudrate"
CONF_BYTESIZE = "bytesize"
CONF_PARITY = "parity"
CONF_STOPBITS = "stopbits"
CONF_SCAN_INTERVAL = "scan_interval"

PARITY_OPTIONS = ["N", "E", "O", "M", "S"]
BYTESIZE_OPTIONS = [5, 6, 7, 8]
STOPBITS_OPTIONS = [1, 1.5, 2]