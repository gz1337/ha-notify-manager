"""Switch platform for Notify Manager."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, CONF_CATEGORIES, CONF_SHOW_SIDEBAR, DEFAULT_CATEGORIES

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Notify Manager switches."""
    categories = entry.data.get(CONF_CATEGORIES, DEFAULT_CATEGORIES)
    
    switches = [
        NotifyCategorySwitch(hass, entry, cat_id, cat_config)
        for cat_id, cat_config in categories.items()
    ]
    
    # Add master switch
    switches.append(NotifyMasterSwitch(hass, entry))
    
    # Add sidebar switch
    switches.append(NotifySidebarSwitch(hass, entry))
    
    async_add_entities(switches)


class NotifyCategorySwitch(SwitchEntity):
    """Switch to enable/disable a notification category."""

    _attr_has_entity_name = True

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        category_id: str,
        category_config: dict,
    ) -> None:
        """Initialize the switch."""
        self.hass = hass
        self._entry = entry
        self._category_id = category_id
        self._category_config = category_config
        
        self._attr_name = f"Kategorie: {category_config.get('name', category_id)}"
        self._attr_unique_id = f"{entry.entry_id}_cat_{category_id}"
        self._attr_icon = category_config.get("icon", "mdi:bell")
        
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Notify Manager",
            manufacturer="Custom Integration",
            model="Notification Manager",
            sw_version="1.2.0",
        )

    @property
    def is_on(self) -> bool:
        """Return true if category is enabled."""
        data = self.hass.data.get(DOMAIN, {}).get(self._entry.entry_id, {})
        categories = data.get("config", {}).get("categories", {})
        category = categories.get(self._category_id, {})
        return category.get("enabled", True)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Enable the category."""
        await self._set_category_state(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Disable the category."""
        await self._set_category_state(False)

    async def _set_category_state(self, enabled: bool) -> None:
        """Set the category enabled state."""
        data = self.hass.data.get(DOMAIN, {}).get(self._entry.entry_id, {})
        categories = data.get("config", {}).get("categories", {})
        
        if self._category_id in categories:
            categories[self._category_id]["enabled"] = enabled
            
            # Update config entry
            new_data = {**self._entry.data}
            new_data[CONF_CATEGORIES] = categories
            self.hass.config_entries.async_update_entry(self._entry, data=new_data)
            
            self.async_write_ha_state()
            _LOGGER.debug("Category %s set to %s", self._category_id, enabled)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra attributes."""
        data = self.hass.data.get(DOMAIN, {}).get(self._entry.entry_id, {})
        categories = data.get("config", {}).get("categories", {})
        category = categories.get(self._category_id, {})
        
        return {
            "category_id": self._category_id,
            "priority": category.get("priority", "normal"),
            "icon": category.get("icon"),
        }


class NotifyMasterSwitch(SwitchEntity):
    """Master switch to enable/disable all notifications."""

    _attr_has_entity_name = True
    _attr_name = "Alle Benachrichtigungen"
    _attr_icon = "mdi:bell-ring"

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the master switch."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_master"
        
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Notify Manager",
            manufacturer="Custom Integration",
            model="Notification Manager",
            sw_version="1.2.0",
        )

    @property
    def is_on(self) -> bool:
        """Return true if any category is enabled."""
        data = self.hass.data.get(DOMAIN, {}).get(self._entry.entry_id, {})
        categories = data.get("config", {}).get("categories", {})
        return any(cat.get("enabled", True) for cat in categories.values())

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Enable all categories."""
        await self._set_all_categories(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Disable all categories."""
        await self._set_all_categories(False)

    async def _set_all_categories(self, enabled: bool) -> None:
        """Set all categories to enabled/disabled."""
        data = self.hass.data.get(DOMAIN, {}).get(self._entry.entry_id, {})
        categories = data.get("config", {}).get("categories", {})
        
        for cat_id in categories:
            categories[cat_id]["enabled"] = enabled
        
        # Update config entry
        new_data = {**self._entry.data}
        new_data[CONF_CATEGORIES] = categories
        self.hass.config_entries.async_update_entry(self._entry, data=new_data)
        
        self.async_write_ha_state()
        _LOGGER.debug("All categories set to %s", enabled)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra attributes."""
        data = self.hass.data.get(DOMAIN, {}).get(self._entry.entry_id, {})
        categories = data.get("config", {}).get("categories", {})
        
        enabled_count = sum(1 for cat in categories.values() if cat.get("enabled", True))
        
        return {
            "enabled_categories": enabled_count,
            "total_categories": len(categories),
        }


class NotifySidebarSwitch(SwitchEntity):
    """Switch to show/hide Notify Manager in sidebar."""

    _attr_has_entity_name = True
    _attr_name = "In Sidebar anzeigen"
    _attr_icon = "mdi:dock-left"
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sidebar switch."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_sidebar"
        
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Notify Manager",
            manufacturer="Custom Integration",
            model="Notification Manager",
            sw_version="1.2.0",
            configuration_url="/notify-manager",
        )

    @property
    def is_on(self) -> bool:
        """Return true if sidebar is enabled."""
        return self._entry.data.get(CONF_SHOW_SIDEBAR, True)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Show in sidebar."""
        await self._set_sidebar_state(True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Hide from sidebar."""
        await self._set_sidebar_state(False)

    async def _set_sidebar_state(self, show: bool) -> None:
        """Set the sidebar visibility state."""
        # Update config entry
        new_data = {**self._entry.data}
        new_data[CONF_SHOW_SIDEBAR] = show
        self.hass.config_entries.async_update_entry(self._entry, data=new_data)
        
        # Reload to apply sidebar change
        await self.hass.config_entries.async_reload(self._entry.entry_id)
        
        self.async_write_ha_state()
        _LOGGER.info("Sidebar visibility set to %s", show)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra attributes."""
        return {
            "panel_url": "/notify-manager",
            "note": "Änderung erfordert Neuladen der Integration",
        }
