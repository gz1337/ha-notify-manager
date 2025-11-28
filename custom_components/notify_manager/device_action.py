"""Device actions for Notify Manager integration.

Fügt Buttons und Aktionen auf der Geräte-Seite hinzu.
"""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.components.device_automation import DEVICE_ACTION_BASE_SCHEMA
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_TYPE,
)
from homeassistant.core import Context, HomeAssistant
from homeassistant.helpers import config_validation as cv, device_registry as dr

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Action types
ACTION_TYPES = {
    "open_panel": "Panel öffnen",
    "send_test": "Test-Benachrichtigung senden",
    "clear_history": "Verlauf löschen",
}

ACTION_SCHEMA = DEVICE_ACTION_BASE_SCHEMA.extend(
    {
        vol.Required(CONF_TYPE): vol.In(ACTION_TYPES.keys()),
    }
)


async def async_get_actions(
    hass: HomeAssistant, device_id: str
) -> list[dict[str, Any]]:
    """Return a list of actions for a device."""
    device_registry = dr.async_get(hass)
    device = device_registry.async_get(device_id)
    
    if not device:
        return []
    
    # Check if this is a Notify Manager device
    if not any(identifier[0] == DOMAIN for identifier in device.identifiers):
        return []
    
    actions = []
    
    for action_type, action_name in ACTION_TYPES.items():
        actions.append(
            {
                CONF_DOMAIN: DOMAIN,
                CONF_DEVICE_ID: device_id,
                CONF_TYPE: action_type,
            }
        )
    
    return actions


async def async_validate_action_config(
    hass: HomeAssistant, config: dict[str, Any]
) -> dict[str, Any]:
    """Validate config."""
    return ACTION_SCHEMA(config)


async def async_call_action_from_config(
    hass: HomeAssistant,
    config: dict[str, Any],
    variables: dict[str, Any],
    context: Context | None,
) -> None:
    """Execute a device action."""
    action_type = config[CONF_TYPE]
    
    if action_type == "open_panel":
        # This is handled by the frontend
        _LOGGER.info("Open panel action triggered")
        
    elif action_type == "send_test":
        # Send a test notification
        await hass.services.async_call(
            DOMAIN,
            "send_notification",
            {
                "title": "🧪 Test-Benachrichtigung",
                "message": "Dies ist eine Test-Nachricht vom Notify Manager.",
                "priority": "normal",
            },
            context=context,
        )
        
    elif action_type == "clear_history":
        # Clear notification history
        for entry_id, entry_data in hass.data.get(DOMAIN, {}).items():
            if isinstance(entry_data, dict) and "notification_history" in entry_data:
                entry_data["notification_history"] = []
        _LOGGER.info("Notification history cleared")
