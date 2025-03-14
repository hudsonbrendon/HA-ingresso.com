"""Config flow for Ingresso integration."""

import logging
from typing import Any, Dict, List

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_CITY_ID,
    CONF_CITY_NAME,
    CONF_PARTNERSHIP,
    CONF_THEATER,
    CONF_THEATER_NAME,
    DEFAULT_PARTNERSHIP,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

# Base API URL for fetching data
API_BASE_URL = "https://api-content.ingresso.com"


class IngressoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Ingresso."""

    VERSION = 1

    def __init__(self):
        """Initialize the config flow."""
        self._cities = []
        self._theaters = []
        self._selected_city_id = None
        self._selected_city_name = None

    async def async_step_user(self, user_input=None):
        """Handle the initial step - selecting a city."""
        errors = {}

        # Fetch cities list if not already loaded
        if not self._cities:
            session = async_get_clientsession(self.hass)
            try:
                self._cities = await self._fetch_cities(session)
            except Exception as err:
                _LOGGER.error("Error fetching cities: %s", err)
                errors["base"] = "cannot_connect"
                return self.async_show_form(
                    step_id="user",
                    data_schema=vol.Schema({}),
                    errors=errors,
                )

        if user_input is not None:
            city_id = user_input.get(CONF_CITY_ID)
            # Find selected city name from ID for display purposes
            for city in self._cities:
                if city["id"] == city_id:
                    self._selected_city_id = city_id
                    self._selected_city_name = city["name"]
                    break

            # Continue to next step to select theater
            return await self.async_step_theater()

        # Prepare city choices for dropdown
        city_choices = {
            city["id"]: f"{city['name']} - {city['uf']}" for city in self._cities
        }

        # Build schema for city selection
        schema = vol.Schema(
            {
                vol.Required(CONF_CITY_ID): vol.In(city_choices),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    async def async_step_theater(self, user_input=None):
        """Handle the second step - selecting a theater."""
        errors = {}

        # Fetch theaters for the selected city
        if not self._theaters:
            session = async_get_clientsession(self.hass)
            try:
                self._theaters = await self._fetch_theaters(
                    session, self._selected_city_id, DEFAULT_PARTNERSHIP
                )
                if not self._theaters:
                    errors["base"] = "no_theaters"
                    return self.async_show_form(
                        step_id="theater",
                        data_schema=vol.Schema({}),
                        errors=errors,
                        description_placeholders={
                            "city_name": self._selected_city_name
                        },
                    )
            except Exception as err:
                _LOGGER.error("Error fetching theaters: %s", err)
                errors["base"] = "cannot_connect"
                return self.async_show_form(
                    step_id="theater",
                    data_schema=vol.Schema({}),
                    errors=errors,
                    description_placeholders={"city_name": self._selected_city_name},
                )

        if user_input is not None:
            theater_id = user_input.get(CONF_THEATER)
            theater_name = ""

            # Get the theater name
            for theater in self._theaters:
                if theater["id"] == theater_id:
                    theater_name = theater["name"]
                    break

            # Create entry with all the collected data
            return self.async_create_entry(
                title=f"{self._selected_city_name} - {theater_name}",
                data={
                    CONF_CITY_ID: self._selected_city_id,
                    CONF_CITY_NAME: self._selected_city_name,
                    CONF_PARTNERSHIP: DEFAULT_PARTNERSHIP,
                    CONF_THEATER: theater_id,
                    CONF_THEATER_NAME: theater_name,
                },
            )

        # Prepare theater choices for dropdown
        theater_choices = {theater["id"]: theater["name"] for theater in self._theaters}

        # Build schema for theater selection
        schema = vol.Schema(
            {
                vol.Required(CONF_THEATER): vol.In(theater_choices),
            }
        )

        return self.async_show_form(
            step_id="theater",
            data_schema=schema,
            errors=errors,
            description_placeholders={"city_name": self._selected_city_name},
        )

    async def _fetch_cities(
        self, session: aiohttp.ClientSession
    ) -> List[Dict[str, Any]]:
        """Fetch available cities from API."""
        all_cities = []

        try:
            async with session.get(f"{API_BASE_URL}/v0/states") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for state in data:
                        if state.get("cities"):
                            all_cities.extend(state["cities"])

            # Sort cities alphabetically by name
            return sorted(all_cities, key=lambda x: x["name"])
        except Exception as err:
            _LOGGER.error("Error fetching cities: %s", err)
            return []

    async def _fetch_theaters(
        self, session: aiohttp.ClientSession, city_id: str, partnership: str
    ) -> List[Dict[str, Any]]:
        """Fetch theaters for a specific city."""
        try:
            async with session.get(
                f"{API_BASE_URL}/v0/theaters/city/{city_id}/partnership/{partnership}"
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if isinstance(data, dict) and "items" in data:
                        return data["items"]
                    return []
                return []
        except Exception as err:
            _LOGGER.error("Error fetching theaters: %s", err)
            return []

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return IngressoOptionsFlowHandler(config_entry)


class IngressoOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle a option flow for Ingresso."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry
        self._cities = []
        self._theaters = []
        self._selected_city_id = self.config_entry.data.get(CONF_CITY_ID)
        self._selected_city_name = self.config_entry.data.get(CONF_CITY_NAME)

    async def async_step_init(self, user_input=None):
        """Handle options flow - selecting a city."""
        errors = {}

        # Fetch cities list if not already loaded
        if not self._cities:
            session = async_get_clientsession(self.hass)
            try:
                self._cities = await self._fetch_cities(session)
            except Exception as err:
                _LOGGER.error("Error fetching cities: %s", err)
                errors["base"] = "cannot_connect"
                return self.async_show_form(
                    step_id="init",
                    data_schema=vol.Schema({}),
                    errors=errors,
                )

        if user_input is not None:
            city_id = user_input.get(CONF_CITY_ID)
            # Find selected city name from ID for display purposes
            for city in self._cities:
                if city["id"] == city_id:
                    self._selected_city_id = city_id
                    self._selected_city_name = city["name"]
                    break

            # Continue to next step to select theater
            return await self.async_step_theater()

        # Prepare city choices for dropdown
        city_choices = {
            city["id"]: f"{city['name']} - {city['uf']}" for city in self._cities
        }

        # Build schema for city selection with default value from current config
        schema = vol.Schema(
            {
                vol.Required(CONF_CITY_ID, default=self._selected_city_id): vol.In(
                    city_choices
                ),
            }
        )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            errors=errors,
        )

    async def async_step_theater(self, user_input=None):
        """Handle the second step - selecting a theater."""
        errors = {}

        # Fetch theaters for the selected city
        if not self._theaters:
            session = async_get_clientsession(self.hass)
            try:
                self._theaters = await self._fetch_theaters(
                    session, self._selected_city_id, DEFAULT_PARTNERSHIP
                )
                if not self._theaters:
                    errors["base"] = "no_theaters"
                    return self.async_show_form(
                        step_id="theater",
                        data_schema=vol.Schema({}),
                        errors=errors,
                        description_placeholders={
                            "city_name": self._selected_city_name
                        },
                    )
            except Exception as err:
                _LOGGER.error("Error fetching theaters: %s", err)
                errors["base"] = "cannot_connect"
                return self.async_show_form(
                    step_id="theater",
                    data_schema=vol.Schema({}),
                    errors=errors,
                    description_placeholders={"city_name": self._selected_city_name},
                )

        if user_input is not None:
            theater_id = user_input.get(CONF_THEATER)
            theater_name = ""

            # Get the theater name
            for theater in self._theaters:
                if theater["id"] == theater_id:
                    theater_name = theater["name"]
                    break

            # Update config entry with new values
            new_data = {
                **self.config_entry.data,
                CONF_CITY_ID: self._selected_city_id,
                CONF_CITY_NAME: self._selected_city_name,
                CONF_PARTNERSHIP: DEFAULT_PARTNERSHIP,
                CONF_THEATER: theater_id,
                CONF_THEATER_NAME: theater_name,
            }

            self.hass.config_entries.async_update_entry(
                self.config_entry, data=new_data
            )
            return self.async_create_entry(title="", data={})

        # Get current theater ID
        current_theater_id = self.config_entry.data.get(CONF_THEATER, "")

        # Prepare theater choices for dropdown
        theater_choices = {theater["id"]: theater["name"] for theater in self._theaters}

        # Build schema for theater selection with default value if it exists in current theaters
        if current_theater_id in theater_choices:
            schema = vol.Schema(
                {
                    vol.Required(CONF_THEATER, default=current_theater_id): vol.In(
                        theater_choices
                    ),
                }
            )
        else:
            schema = vol.Schema(
                {
                    vol.Required(CONF_THEATER): vol.In(theater_choices),
                }
            )

        return self.async_show_form(
            step_id="theater",
            data_schema=schema,
            errors=errors,
            description_placeholders={"city_name": self._selected_city_name},
        )

    async def _fetch_cities(
        self, session: aiohttp.ClientSession
    ) -> List[Dict[str, Any]]:
        """Fetch available cities from API."""
        all_cities = []

        try:
            async with session.get(f"{API_BASE_URL}/v0/states") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for state in data:
                        if state.get("cities"):
                            all_cities.extend(state["cities"])

            # Sort cities alphabetically by name
            return sorted(all_cities, key=lambda x: x["name"])
        except Exception as err:
            _LOGGER.error("Error fetching cities: %s", err)
            return []

    async def _fetch_theaters(
        self, session: aiohttp.ClientSession, city_id: str, partnership: str
    ) -> List[Dict[str, Any]]:
        """Fetch theaters for a specific city."""
        try:
            async with session.get(
                f"{API_BASE_URL}/v0/theaters/city/{city_id}/partnership/{partnership}"
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if isinstance(data, dict) and "items" in data:
                        return data["items"]
                    return []
                return []
        except Exception as err:
            _LOGGER.error("Error fetching theaters: %s", err)
            return []
