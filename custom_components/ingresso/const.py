"""Constants for the Ingresso integration."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

# API
BASE_URL = "https://api-content.ingresso.com/v0/templates/nowplaying/{}?partnership={}"
THEATER_URL = "https://api-content.ingresso.com/v0/templates/nowplaying/{}?partnership={}&theaters={}"
DEFAULT_POSTER = "https://www.promoview.com.br/uploads/2019/01/images/07.01.2019/ingresso.comlogo.jpg"

# Configuration
CONF_CITY_ID = "city_id"
CONF_CITY_NAME = "city_name"
CONF_PARTNERSHIP = "partnership"
DEFAULT_PARTNERSHIP = "encora"
CONF_THEATER = "theater"
CONF_THEATER_NAME = "theater_name"

# Misc
ICON = "mdi:movie"
SCAN_INTERVAL = 3600  # 1 hour
DOMAIN = "ingresso"
ATTRIBUTION = "Dados fornecidos por Ingresso.com"
