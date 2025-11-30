"""Button entities for Notify Manager integration.

Erstellt Buttons die auf der Geräte-Seite angezeigt werden:
- Panel öffnen
- Test-Benachrichtigung
- Verlauf löschen
"""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_SHOW_SIDEBAR

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Notify Manager button entities."""
    entities = [
        NotifyManagerOpenPanelButton(hass, entry),
        NotifyManagerTestButton(hass, entry),
        NotifyManagerClearHistoryButton(hass, entry),
    ]
    
    async_add_entities(entities)


class NotifyManagerOpenPanelButton(ButtonEntity):
    """Button to open the Notify Manager panel."""
    
    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.CONFIG
    
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the button."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_open_panel"
        self._attr_name = "Panel öffnen"
        self._attr_icon = "mdi:open-in-new"
        
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Notify Manager",
            manufacturer="Custom Integration",
            model="Notification Manager",
            sw_version="1.2.3.3",
            configuration_url="/notify-manager",
        )
    
    async def async_press(self) -> None:
        """Handle the button press."""
        # Fire an event that the frontend can listen to
        self.hass.bus.async_fire(
            f"{DOMAIN}_open_panel",
            {"url": "/notify-manager"}
        )
        _LOGGER.info("Panel open button pressed - navigate to /notify-manager")


class NotifyManagerTestButton(ButtonEntity):
    """Button to send a test notification."""
    
    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the button."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_test_notification"
        self._attr_name = "Test-Benachrichtigung"
        self._attr_icon = "mdi:bell-ring-outline"
        
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Notify Manager",
            manufacturer="Custom Integration",
            model="Notification Manager",
            sw_version="1.2.3.3",
        )
    
    async def async_press(self) -> None:
        """Handle the button press."""
        await self.hass.services.async_call(
            DOMAIN,
            "send_notification",
            {
                "title": "🧪 Test-Benachrichtigung",
                "message": f"Dies ist eine Test-Nachricht vom Notify Manager.\n\nZeit: {self.hass.helpers.template.now().strftime('%H:%M:%S')}",
                "priority": "normal",
            },
        )
        _LOGGER.info("Test notification sent")


class NotifyManagerClearHistoryButton(ButtonEntity):
    """Button to clear notification history."""
    
    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the button."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_clear_history"
        self._attr_name = "Verlauf löschen"
        self._attr_icon = "mdi:notification-clear-all"
        
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Notify Manager",
            manufacturer="Custom Integration",
            model="Notification Manager",
            sw_version="1.2.3.3",
        )
    
    async def async_press(self) -> None:
        """Handle the button press."""
        # Clear history in domain data
        domain_data = self.hass.data.get(DOMAIN, {})
        for entry_id, entry_data in domain_data.items():
            if isinstance(entry_data, dict) and "notification_history" in entry_data:
                entry_data["notification_history"] = []
        
        _LOGGER.info("Notification history cleared")
