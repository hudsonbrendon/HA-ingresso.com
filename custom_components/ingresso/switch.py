"""Switch platform for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback
    from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

ENTITY_DESCRIPTIONS = (
    SwitchEntityDescription(
        key="ingresso_switch",
        name="Ingresso Switch",
        icon="mdi:movie",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    client = hass.data[DOMAIN][entry.entry_id]["client"]

    async_add_entities(
        IngressoSwitch(
            coordinator=coordinator,
            client=client,
            entity_description=entity_description,
            entry_id=entry.entry_id,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class IngressoSwitch(CoordinatorEntity, SwitchEntity):
    """Ingresso switch class."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        client: Any,
        entity_description: SwitchEntityDescription,
        entry_id: str,
    ) -> None:
        """Initialize the switch class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._client = client
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
        """Return true if the switch is on."""
        # You can implement a meaningful state check here
        return len(self.coordinator.data) > 0 if self.coordinator.data else False

    async def async_turn_on(self, **_: Any) -> None:
        """Turn on the switch."""
        # Implement a meaningful action here if needed
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **_: Any) -> None:
        """Turn off the switch."""
        # Implement a meaningful action here if needed
        await self.coordinator.async_request_refresh()
