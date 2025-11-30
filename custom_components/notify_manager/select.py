"""Select entities for Notify Manager integration.

Provides select entity for notification template selection in automation conditions.
"""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback, Event
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Notify Manager select entities."""
    entities = [
        NotifyManagerActiveTemplateSelect(hass, entry),
    ]

    async_add_entities(entities)


class NotifyManagerActiveTemplateSelect(SelectEntity):
    """Select entity showing the last active notification template.

    This entity:
    1. Automatically updates when a notification is sent from a template
    2. Can be used in automation conditions to check which template was last used
    3. Shows all user-created templates from the frontend as options
    4. Tracks button responses from notifications
    """

    _attr_has_entity_name = True

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the select entity."""
        self.hass = hass
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_active_template"
        self._attr_name = "Active Notification"
        self._attr_icon = "mdi:bell-check"
        self._last_action = None
        self._last_action_time = None
        self._last_reply_text = None

        # Will be populated from HA storage
        self._template_options = {"none": "No active notification"}
        self._attr_options = list(self._template_options.values())
        self._attr_current_option = self._template_options["none"]

    async def async_added_to_hass(self) -> None:
        """Register event listener when added to hass."""
        await super().async_added_to_hass()

        # Load templates from storage
        await self._update_template_options()

        @callback
        def handle_templates_updated(event: Event) -> None:
            """Handle when templates are saved - refresh options."""
            _LOGGER.debug("Templates updated, refreshing options")
            self.hass.async_create_task(self._update_template_options())
            self.async_write_ha_state()

        self.hass.bus.async_listen(f"{DOMAIN}_templates_saved", handle_templates_updated)

        @callback
        def handle_notification_sent(event: Event) -> None:
            """Handle when a notification is sent - track the template."""
            template_name = event.data.get("template_name")
            if template_name and template_name in self._template_options:
                self._attr_current_option = self._template_options.get(template_name, template_name)
                self.async_write_ha_state()

        @callback
        def handle_action(event: Event) -> None:
            """Handle notification action events."""
            action = event.data.get("action", "")
            self._last_action = action
            self._last_action_time = event.time_fired.isoformat()
            self._last_reply_text = event.data.get("reply_text")

            # Try to get template from event data or hass.data
            template_name = event.data.get("template_name")
            if not template_name:
                data = self.hass.data.get(DOMAIN, {}).get(self._entry.entry_id, {})
                last_sent = data.get("last_sent_notification", {})
                tag = event.data.get("tag")
                if last_sent.get("tag") == tag:
                    template_name = last_sent.get("template_name")

            if template_name:
                option = self._template_options.get(template_name, template_name)
                if option in self._attr_options:
                    self._attr_current_option = option
                    self.async_write_ha_state()

            _LOGGER.debug("Button action received: %s (template: %s)", action, template_name)

        self.hass.bus.async_listen("mobile_app_notification_action", handle_action)
        self.hass.bus.async_listen(f"{DOMAIN}_notification_sent", handle_notification_sent)

    async def _update_template_options(self) -> None:
        """Update options with user-created templates from storage."""
        self._template_options = {"none": "No active notification"}

        # Get templates from hass.data (loaded from persistent storage)
        data = self.hass.data.get(DOMAIN, {}).get(self._entry.entry_id, {})
        user_templates = data.get("user_templates", [])

        for template in user_templates:
            name = template.get("name", "")
            template_id = template.get("id", name)
            if name:
                self._template_options[template_id] = name

        self._attr_options = list(self._template_options.values())

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry.entry_id)},
            name="Notify Manager",
            manufacturer="Custom Integration",
            model="Notification Manager",
            sw_version="1.2.7.1",
        )

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        # Collect all action IDs from templates
        data = self.hass.data.get(DOMAIN, {}).get(self._entry.entry_id, {})
        user_templates = data.get("user_templates", [])
        all_actions = []
        for template in user_templates:
            for btn in template.get("buttons", []):
                action_id = btn.get("action", "")
                if action_id:
                    all_actions.append(f"{action_id} ({template.get('name', 'Unknown')})")

        return {
            "last_action": self._last_action,
            "last_action_time": self._last_action_time,
            "reply_text": self._last_reply_text,
            "available_templates": [k for k in self._template_options.keys() if k != "none"],
            "available_action_ids": all_actions,
        }

    async def async_select_option(self, option: str) -> None:
        """Change the selected option (for manual reset)."""
        self._attr_current_option = option
        self.async_write_ha_state()
