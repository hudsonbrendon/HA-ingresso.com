"""Support for Ingresso.com sensors."""

import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.util import dt

from .api import IngressoApiClient
from .const import (
    CONF_CITY_ID,
    CONF_CITY_NAME,
    CONF_PARTNERSHIP,
    CONF_THEATER,
    CONF_THEATER_NAME,
    DEFAULT_POSTER,
    DOMAIN,
    ICON,
)

_LOGGER = logging.getLogger(__name__)

# Service constants
SERVICE_GET_MOVIES = "get_movies"
ATTR_CITY_ID = "city_id"
ATTR_PARTNERSHIP = "partnership"
ATTR_THEATER = "theater"

# Service schema
GET_MOVIES_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_CITY_ID): cv.string,
        vol.Required(ATTR_PARTNERSHIP): cv.string,
        vol.Optional(ATTR_THEATER): cv.string,
    }
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Ingresso sensor."""
    config_data = hass.data[DOMAIN][config_entry.entry_id]
    client = config_data["client"]

    # Create a unique device identifier
    device_id = f"{config_data[CONF_CITY_ID]}_{config_data[CONF_PARTNERSHIP]}"
    if config_data.get(CONF_THEATER):
        device_id = f"{device_id}_{config_data.get(CONF_THEATER)}"

    # Create a device name
    if config_data.get(CONF_THEATER_NAME):
        device_name = f"Ingresso.com {config_data.get(CONF_THEATER_NAME)}"
    else:
        device_name = f"Ingresso.com {config_data[CONF_PARTNERSHIP].capitalize()} {config_data[CONF_CITY_NAME]}"

    sensor = IngressoSensor(
        client=client,
        city_id=config_data[CONF_CITY_ID],
        city_name=config_data[CONF_CITY_NAME],
        partnership=config_data[CONF_PARTNERSHIP],
        theater=config_data.get(CONF_THEATER, ""),
        theater_name=config_data.get(CONF_THEATER_NAME, ""),
        device_id=device_id,
        device_name=device_name,
        config_entry_id=config_entry.entry_id,
    )

    async_add_entities([sensor], update_before_add=True)

    # Register the service
    async def handle_get_movies(call: ServiceCall) -> None:
        """Handle the service call."""
        city_id = call.data.get(ATTR_CITY_ID)
        partnership = call.data.get(ATTR_PARTNERSHIP)
        theater = call.data.get(ATTR_THEATER, "")

        # Create a temporary API client for the service call
        temp_client = IngressoApiClient(
            city_id=city_id,
            partnership=partnership,
            session=async_get_clientsession(hass),
            theater=theater,
        )

        try:
            movies = await temp_client.async_get_movies()
            formatted_movies = []

            if movies:
                formatted_movies = [
                    {
                        "title": movie.get("title", "Não informado"),
                        "poster": movie["images"][0]["url"]
                        if movie.get("images")
                        else DEFAULT_POSTER,
                        "synopsis": movie.get("synopsis", "Não informado"),
                        "director": movie.get("director", "Não informado"),
                        "cast": movie.get("cast", "Não informado"),
                        "studio": movie.get("distributor", "Não informado"),
                        "genres": movie.get("genres", "Não informado"),
                        "runtime": movie.get("duration", "Não informado"),
                        "rating": movie.get("contentRating", "Não informado"),
                        "release": "$date",
                        "airdate": movie["premiereDate"]["localDate"].split("T")[0]
                        if movie.get("premiereDate")
                        and movie.get("premiereDate").get("localDate")
                        else "Não informado",
                        "ticket": movie.get("siteURL", "Não informado"),
                    }
                    for movie in movies
                ]

            # Make result available as a service response
            hass.states.async_set(
                f"{DOMAIN}.service_result",
                len(formatted_movies),
                {
                    "movies": formatted_movies,
                    "last_updated": dt.utcnow().isoformat(),
                },
            )

        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.error("Erro ao obter filmes via serviço: %s", error)
            hass.states.async_set(
                f"{DOMAIN}.service_result",
                "error",
                {
                    "error": str(error),
                },
            )

    # Register the service with Home Assistant
    hass.services.async_register(
        DOMAIN, SERVICE_GET_MOVIES, handle_get_movies, schema=GET_MOVIES_SCHEMA
    )


class IngressoDeviceEntity(SensorEntity):
    """Base entity class for Ingresso.com devices."""

    def __init__(
        self,
        device_id: str,
        device_name: str,
        config_entry_id: str,
    ) -> None:
        """Initialize the device entity."""
        self._device_id = device_id
        self._config_entry_id = config_entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=device_name,
            manufacturer="Ingresso.com",
            model="Cinema",
            sw_version="1.0",
            configuration_url="https://ingresso.com",
            # Remove the via_device parameter which is causing the warning
        )


class IngressoSensor(IngressoDeviceEntity):
    """Representation of an Ingresso.com sensor."""

    _attr_has_entity_name = True
    _attr_attribution = "Dados fornecidos por Ingresso.com"
    _attr_translation_key = "ingresso"

    def __init__(
        self,
        client: IngressoApiClient,
        city_id: str,
        city_name: str,
        partnership: str,
        theater: str,
        theater_name: str,
        device_id: str,
        device_name: str,
        config_entry_id: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(device_id, device_name, config_entry_id)

        self._client = client
        self._city_id = city_id
        self._city_name = city_name
        self._partnership = partnership
        self._theater = theater
        self._theater_name = theater_name
        self._state: Optional[StateType] = None
        self._available = True
        self._movies = [
            {
                "title_default": "$title",
                "line1_default": "$rating",
                "line2_default": "$release",
                "line3_default": "$runtime",
                "line4_default": "$studio",
                "icon": "mdi:arrow-down-bold",
            }
        ]

        # Create a unique ID based on city and theater
        unique_suffix = device_id
        self._attr_unique_id = f"{DOMAIN}_{unique_suffix}"

        # Create a meaningful name
        self._attr_name = "Filmes em Cartaz"
        self._attr_icon = ICON
        self._attr_native_unit_of_measurement = "filmes"
        self._last_updated = None

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return the state attributes."""
        return {
            "data": self._movies,
            "last_updated": self._last_updated,
            "theater_name": self._theater_name,
            "city_name": self._city_name,
        }

    async def async_update(self) -> None:
        """Update the sensor."""
        _LOGGER.debug("%s - Executando atualização", self.name)

        try:
            movie_data = await self._client.async_get_movies()

            if movie_data:
                formatted_movies = [
                    {
                        "title": movie.get("title", "Não informado"),
                        "poster": movie["images"][0]["url"]
                        if movie.get("images")
                        else DEFAULT_POSTER,
                        "synopsis": movie.get("synopsis", "Não informado"),
                        "director": movie.get("director", "Não informado"),
                        "cast": movie.get("cast", "Não informado"),
                        "studio": movie.get("distributor", "Não informado"),
                        "genres": movie.get("genres", "Não informado"),
                        "runtime": movie.get("duration", "Não informado"),
                        "rating": movie.get("contentRating", "Não informado"),
                        "release": "$date",
                        "airdate": movie["premiereDate"]["localDate"].split("T")[0]
                        if movie.get("premiereDate")
                        and movie.get("premiereDate").get("localDate")
                        else "Não informado",
                        "city": self._city_name,
                        "theater": self._theater_name,
                        "ticket": movie.get("siteURL", "Não informado"),
                    }
                    for movie in movie_data
                ]

                self._movies = [self._movies[0], *formatted_movies]
                self._state = len(formatted_movies)
                self._last_updated = dt.utcnow().isoformat()
                self._available = True

            else:
                self._available = False

        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.error("Erro ao atualizar sensor Ingresso.com: %s", error)
            self._available = False
