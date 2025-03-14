"""Integração Ingresso.com para Home Assistant."""

import logging
from typing import Any

from homeassistant import config_entries, core
from homeassistant.const import Platform
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import IngressoApiClient
from .const import CONF_CITY_ID, CONF_CITY_NAME, CONF_PARTNERSHIP, CONF_THEATER, DOMAIN

PLATFORMS = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Configurar a integração Ingresso.com a partir de uma entrada de configuração."""
    session = async_get_clientsession(hass)
    client = IngressoApiClient(
        city_id=entry.data.get(CONF_CITY_ID),
        partnership=entry.data.get(CONF_PARTNERSHIP),
        session=session,
        theater=entry.data.get(CONF_THEATER),
    )

    try:
        await client.async_get_movies()
    except Exception as exception:
        raise ConfigEntryAuthFailed("Falha ao conectar") from exception

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "client": client,
        **entry.data,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(
    hass: core.HomeAssistant, entry: config_entries.ConfigEntry
) -> bool:
    """Descarregar uma entrada de configuração."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def async_migrate_entry(
    hass: core.HomeAssistant, config_entry: config_entries.ConfigEntry
) -> bool:
    """Migrar entrada antiga."""
    _LOGGER.debug("Migrando da versão %s", config_entry.version)

    # Preservar compatibilidade com as configurações existentes
    data = {
        CONF_CITY_ID: config_entry.data.get(CONF_CITY_ID),
        CONF_CITY_NAME: config_entry.data.get(CONF_CITY_NAME),
        CONF_PARTNERSHIP: config_entry.data.get(CONF_PARTNERSHIP),
    }

    # Adicionar informações do cinema se disponíveis
    if CONF_THEATER in config_entry.data:
        data[CONF_THEATER] = config_entry.data[CONF_THEATER]
        if "theater_name" in config_entry.data:
            data["theater_name"] = config_entry.data["theater_name"]

    hass.config_entries.async_update_entry(config_entry, data=data)

    return True
