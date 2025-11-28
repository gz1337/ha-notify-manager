"""Select entities for Notify Manager integration.

Bietet Select-Entities für:
- Action Template Auswahl
- Standard-Priorität
- Standard-Kategorie
"""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    ACTION_TEMPLATES,
    DEFAULT_CATEGORIES,
    PRIORITY_LEVELS,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Notify Manager select entities."""
    entities = [
        NotifyManagerActionTemplateSelect(hass, entry),
        NotifyManagerPrioritySelect(hass, entry),
        NotifyManagerCategorySelect(hass, entry),
    ]
    
    async_add_entities(entities)


class NotifyManagerActionTemplateSelect(SelectEntity):
    """Select entity for choosing action templates."""
    
    _attr_has_entity_name = True
    _attr_translation_key = "action_template"
    
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the select entity."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_action_template"
        self._attr_name = "Aktions-Vorlage"
        self._current_option = "none"
        
        # Build options from ACTION_TEMPLATES
        self._template_labels = {
            "none": "Keine Vorlage",
            "confirm_dismiss": "✅ Bestätigen / Ablehnen",
            "alarm_response": "🚨 Alarm-Antwort (OK/Später/Notfall)",
            "door_response": "🚪 Tür-Antwort (Öffnen/Ignorieren/Sprechen)",
            "yes_no": "👍 Ja / Nein",
            "reply": "💬 Antworten (mit Texteingabe)",
        }
        
        self._attr_options = list(self._template_labels.values())
        self._attr_current_option = self._template_labels["none"]
    
    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name="Notify Manager",
            manufacturer="Custom Integration",
            model="Notification Manager",
            sw_version="1.2.0",
        )
    
    @property
    def icon(self) -> str:
        """Return icon."""
        return "mdi:gesture-tap-button"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        template_key = self._get_template_key(self._attr_current_option)
        actions = ACTION_TEMPLATES.get(template_key, [])
        
        return {
            "template_key": template_key,
            "actions": actions,
            "action_count": len(actions),
            "action_ids": [a.get("action") for a in actions],
        }
    
    def _get_template_key(self, label: str) -> str:
        """Get template key from label."""
        for key, value in self._template_labels.items():
            if value == label:
                return key
        return "none"
    
    def _get_template_label(self, key: str) -> str:
        """Get label from template key."""
        return self._template_labels.get(key, self._template_labels["none"])
    
    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option
        self._current_option = self._get_template_key(option)
        
        # Store in hass.data for use by services
        self.hass.data[DOMAIN].setdefault("selected_template", {})
        self.hass.data[DOMAIN]["selected_template"] = {
            "key": self._current_option,
            "actions": ACTION_TEMPLATES.get(self._current_option, []),
        }
        
        self.async_write_ha_state()


class NotifyManagerPrioritySelect(SelectEntity):
    """Select entity for default priority."""
    
    _attr_has_entity_name = True
    _attr_translation_key = "default_priority"
    
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the select entity."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_default_priority"
        self._attr_name = "Standard-Priorität"
        
        self._priority_labels = {
            "low": "🔇 Niedrig (Leise)",
            "normal": "📱 Normal",
            "high": "🔔 Hoch (Wichtig)",
            "critical": "🚨 Kritisch (Durchbricht Nicht-Stören)",
        }
        
        self._attr_options = list(self._priority_labels.values())
        
        # Get current from config
        current_priority = entry.data.get("default_priority", "normal")
        self._attr_current_option = self._priority_labels.get(current_priority, self._priority_labels["normal"])
    
    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name="Notify Manager",
            manufacturer="Custom Integration",
            model="Notification Manager",
            sw_version="1.2.0",
        )
    
    @property
    def icon(self) -> str:
        """Return icon."""
        if "Kritisch" in str(self._attr_current_option):
            return "mdi:alert-circle"
        elif "Hoch" in str(self._attr_current_option):
            return "mdi:bell-ring"
        elif "Niedrig" in str(self._attr_current_option):
            return "mdi:bell-sleep"
        return "mdi:bell"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        priority_key = self._get_priority_key(self._attr_current_option)
        priority_config = PRIORITY_LEVELS.get(priority_key, {})
        
        return {
            "priority_key": priority_key,
            "importance": priority_config.get("importance"),
            "interruption_level": priority_config.get("interruption_level"),
            "is_critical": priority_config.get("critical", False),
        }
    
    def _get_priority_key(self, label: str) -> str:
        """Get priority key from label."""
        for key, value in self._priority_labels.items():
            if value == label:
                return key
        return "normal"
    
    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option
        priority_key = self._get_priority_key(option)
        
        # Store in hass.data
        self.hass.data[DOMAIN].setdefault("default_priority", "normal")
        self.hass.data[DOMAIN]["default_priority"] = priority_key
        
        self.async_write_ha_state()


class NotifyManagerCategorySelect(SelectEntity):
    """Select entity for default category."""
    
    _attr_has_entity_name = True
    _attr_translation_key = "default_category"
    
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the select entity."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_default_category"
        self._attr_name = "Standard-Kategorie"
        
        # Build from DEFAULT_CATEGORIES
        self._category_labels = {
            "none": "Keine Kategorie",
        }
        for cat_id, cat_config in DEFAULT_CATEGORIES.items():
            icon = cat_config.get("icon", "mdi:bell").replace("mdi:", "")
            name = cat_config.get("name", cat_id.title())
            self._category_labels[cat_id] = f"{name}"
        
        self._attr_options = list(self._category_labels.values())
        self._attr_current_option = self._category_labels["none"]
    
    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name="Notify Manager",
            manufacturer="Custom Integration",
            model="Notification Manager",
            sw_version="1.2.0",
        )
    
    @property
    def icon(self) -> str:
        """Return icon."""
        category_key = self._get_category_key(self._attr_current_option)
        if category_key in DEFAULT_CATEGORIES:
            return DEFAULT_CATEGORIES[category_key].get("icon", "mdi:tag")
        return "mdi:tag"
    
    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        category_key = self._get_category_key(self._attr_current_option)
        category_config = DEFAULT_CATEGORIES.get(category_key, {})
        
        return {
            "category_key": category_key,
            "priority": category_config.get("priority"),
            "sound": category_config.get("sound"),
            "channel": category_config.get("channel"),
            "color": category_config.get("color"),
        }
    
    def _get_category_key(self, label: str) -> str:
        """Get category key from label."""
        for key, value in self._category_labels.items():
            if value == label:
                return key
        return "none"
    
    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        self._attr_current_option = option
        category_key = self._get_category_key(option)
        
        # Store in hass.data
        self.hass.data[DOMAIN].setdefault("default_category", "none")
        self.hass.data[DOMAIN]["default_category"] = category_key
        
        self.async_write_ha_state()
