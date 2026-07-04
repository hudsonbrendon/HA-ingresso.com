"""Binary sensor platform for Ingresso.com."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

ENTITY_DESCRIPTIONS = (
    BinarySensorEntityDescription(
        key="ingresso_availability",
        name="Ingresso Movies Available",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the binary_sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    async_add_entities(
        IngressoBinarySensor(
            coordinator=coordinator,
            entity_description=entity_description,
            entry_id=entry.entry_id,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class IngressoBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Ingresso binary_sensor class."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        entity_description: BinarySensorEntityDescription,
        entry_id: str,
    ) -> None:
        """Initialize the binary_sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = f"{entry_id}_{entity_description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": "Ingresso.com",
            "manufacturer": "Ingresso.com",
            "model": "API",
            "sw_version": "1.0",
        }

    @property
    def is_on(self) -> bool:
        """Return true if movies are available."""
        return len(self.coordinator.data) > 0 if self.coordinator.data else False
