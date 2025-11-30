"""Sensor platform for Notify Manager."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback, Event
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# All known button actions for state options
KNOWN_BUTTON_ACTIONS = [
    "CONFIRM",
    "DISMISS", 
    "YES",
    "NO",
    "ALARM_CONFIRM",
    "ALARM_SNOOZE",
    "ALARM_EMERGENCY",
    "DOOR_UNLOCK",
    "DOOR_IGNORE",
    "DOOR_SPEAK",
    "REPLY",
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Notify Manager sensors."""
    sensors = [
        NotifyManagerStatsSensor(hass, entry, "notifications_sent", "Gesendete Benachrichtigungen"),
        NotifyManagerStatsSensor(hass, entry, "notifications_today", "Benachrichtigungen heute"),
        NotifyManagerCategorySensor(hass, entry),
        NotifyManagerLastActionSensor(hass, entry),
    ]
    async_add_entities(sensors)


class NotifyManagerLastActionSensor(SensorEntity):
    """Sensor tracking the last clicked button action."""

    _attr_has_entity_name = True

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._entry = entry
        self._attr_name = "Letzter Button"
        self._attr_unique_id = f"{entry.entry_id}_last_action"
        self._attr_icon = "mdi:gesture-tap-button"
        self._state = "none"
        self._last_data = {}
        
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Notify Manager",
            manufacturer="Custom Integration",
            model="Notification Manager",
            sw_version="1.2.3.2",
            configuration_url="/notify-manager",
        )

    async def async_added_to_hass(self) -> None:
        """Register event listener when added to hass."""
        await super().async_added_to_hass()
        
        @callback
        def handle_action(event: Event) -> None:
            """Handle notification action events."""
            action = event.data.get("action", "")
            if action:
                self._state = action
                self._last_data = {
                    "action": action,
                    "timestamp": datetime.now().isoformat(),
                    "reply_text": event.data.get("reply_text"),
                    "event_data": dict(event.data),
                }
                # Store in hass.data for conditions
                data = self.hass.data.get(DOMAIN, {}).get(self._entry.entry_id, {})
                data["last_action"] = self._last_data
                self.async_write_ha_state()
                _LOGGER.debug("Button action received: %s", action)
        
        # Listen to mobile app notification actions
        self.hass.bus.async_listen("mobile_app_notification_action", handle_action)

    @property
    def native_value(self) -> str:
        """Return the last action."""
        return self._state

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        return {
            "last_action_time": self._last_data.get("timestamp"),
            "reply_text": self._last_data.get("reply_text"),
            "known_actions": KNOWN_BUTTON_ACTIONS,
        }


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Notify Manager sensors."""
    sensors = [
        NotifyManagerStatsSensor(hass, entry, "notifications_sent", "Gesendete Benachrichtigungen"),
        NotifyManagerStatsSensor(hass, entry, "notifications_today", "Benachrichtigungen heute"),
        NotifyManagerCategorySensor(hass, entry),
    ]
    async_add_entities(sensors)


class NotifyManagerStatsSensor(SensorEntity):
    """Sensor for notification statistics."""

    _attr_has_entity_name = True
    _attr_state_class = SensorStateClass.TOTAL_INCREASING

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        sensor_type: str,
        name: str,
    ) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._entry = entry
        self._sensor_type = sensor_type
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{sensor_type}"
        self._attr_native_value = 0
        self._attr_icon = "mdi:bell-badge"
        
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Notify Manager",
            manufacturer="Custom Integration",
            model="Notification Manager",
            sw_version="1.2.3.2",
            configuration_url="/notify-manager",
        )

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        data = self.hass.data.get(DOMAIN, {}).get(self._entry.entry_id, {})
        history = data.get("notification_history", [])
        
        if self._sensor_type == "notifications_sent":
            return len(history)
        elif self._sensor_type == "notifications_today":
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_timestamp = today_start.timestamp()
            return sum(1 for h in history if h.get("timestamp", 0) >= today_timestamp)
        
        return 0

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        data = self.hass.data.get(DOMAIN, {}).get(self._entry.entry_id, {})
        history = data.get("notification_history", [])
        
        if not history:
            return {}
        
        # Get last notification
        last = history[-1] if history else None
        
        return {
            "last_notification_title": last.get("title") if last else None,
            "last_notification_time": last.get("timestamp") if last else None,
            "configured_devices": len(data.get("devices", [])),
        }


class NotifyManagerCategorySensor(SensorEntity):
    """Sensor showing active categories."""

    _attr_has_entity_name = True

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self._entry = entry
        self._attr_name = "Aktive Kategorien"
        self._attr_unique_id = f"{entry.entry_id}_active_categories"
        self._attr_icon = "mdi:tag-multiple"
        
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Notify Manager",
            manufacturer="Custom Integration",
            model="Notification Manager",
            sw_version="1.2.3.2",
            configuration_url="/notify-manager",
        )

    @property
    def native_value(self) -> int:
        """Return count of active categories."""
        data = self.hass.data.get(DOMAIN, {}).get(self._entry.entry_id, {})
        categories = data.get("config", {}).get("categories", {})
        return sum(1 for cat in categories.values() if cat.get("enabled", True))

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return category details."""
        data = self.hass.data.get(DOMAIN, {}).get(self._entry.entry_id, {})
        categories = data.get("config", {}).get("categories", {})
        
        enabled = []
        disabled = []
        
        for cat_id, cat_config in categories.items():
            if cat_config.get("enabled", True):
                enabled.append(cat_config.get("name", cat_id))
            else:
                disabled.append(cat_config.get("name", cat_id))
        
        return {
            "enabled_categories": enabled,
            "disabled_categories": disabled,
            "total_categories": len(categories),
        }
