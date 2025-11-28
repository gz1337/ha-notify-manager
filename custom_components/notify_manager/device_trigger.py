"""Device triggers for Notify Manager integration.

Diese Datei ermöglicht die Auswahl von Notify Manager Events als Auslöser 
in der Automations-UI unter "Gerät" -> Notify Manager.
"""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.components.device_automation import DEVICE_TRIGGER_BASE_SCHEMA
from homeassistant.components.homeassistant.triggers import event as event_trigger
from homeassistant.const import (
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_ENTITY_ID,
    CONF_PLATFORM,
    CONF_TYPE,
)
from homeassistant.core import CALLBACK_TYPE, HomeAssistant
from homeassistant.helpers import config_validation as cv, device_registry as dr
from homeassistant.helpers.trigger import TriggerActionType, TriggerInfo
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, ACTION_TEMPLATES, DEFAULT_CATEGORIES

_LOGGER = logging.getLogger(__name__)

# Trigger types
TRIGGER_TYPES = {
    "action_received": "Button gedrückt",
    "action_confirm": "Bestätigen gedrückt",
    "action_dismiss": "Ablehnen gedrückt",
    "action_yes": "Ja gedrückt",
    "action_no": "Nein gedrückt",
    "action_alarm_confirm": "Alarm bestätigt (OK)",
    "action_alarm_snooze": "Alarm verschoben",
    "action_alarm_emergency": "Notfall ausgelöst",
    "action_door_unlock": "Tür öffnen gedrückt",
    "action_door_ignore": "Tür ignorieren gedrückt",
    "action_reply": "Antwort gesendet",
    "notification_sent": "Benachrichtigung gesendet",
    "notification_cleared": "Benachrichtigung gelöscht",
}

# Map trigger types to action values
TRIGGER_ACTION_MAP = {
    "action_confirm": "CONFIRM",
    "action_dismiss": "DISMISS",
    "action_yes": "YES",
    "action_no": "NO",
    "action_alarm_confirm": "ALARM_CONFIRM",
    "action_alarm_snooze": "ALARM_SNOOZE",
    "action_alarm_emergency": "ALARM_EMERGENCY",
    "action_door_unlock": "DOOR_UNLOCK",
    "action_door_ignore": "DOOR_IGNORE",
    "action_reply": "REPLY",
}

TRIGGER_SCHEMA = DEVICE_TRIGGER_BASE_SCHEMA.extend(
    {
        vol.Required(CONF_TYPE): vol.In(TRIGGER_TYPES.keys()),
        vol.Optional("action"): cv.string,
        vol.Optional("category"): vol.In(list(DEFAULT_CATEGORIES.keys())),
    }
)


async def async_get_triggers(
    hass: HomeAssistant, device_id: str
) -> list[dict[str, Any]]:
    """Return a list of triggers for a device."""
    device_registry = dr.async_get(hass)
    device = device_registry.async_get(device_id)
    
    if not device:
        return []
    
    # Check if this is a Notify Manager device
    if not any(identifier[0] == DOMAIN for identifier in device.identifiers):
        return []
    
    triggers = []
    
    for trigger_type, trigger_name in TRIGGER_TYPES.items():
        triggers.append(
            {
                CONF_PLATFORM: "device",
                CONF_DEVICE_ID: device_id,
                CONF_DOMAIN: DOMAIN,
                CONF_TYPE: trigger_type,
            }
        )
    
    return triggers


async def async_validate_trigger_config(
    hass: HomeAssistant, config: ConfigType
) -> ConfigType:
    """Validate config."""
    return TRIGGER_SCHEMA(config)


async def async_attach_trigger(
    hass: HomeAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach a trigger."""
    trigger_type = config[CONF_TYPE]
    
    # Determine which events to listen to
    if trigger_type == "notification_sent":
        event_type = f"{DOMAIN}_notification_sent"
        event_data = {}
    elif trigger_type == "notification_cleared":
        event_type = f"{DOMAIN}_notification_cleared"
        event_data = {}
    elif trigger_type == "action_received":
        # Listen to any action
        event_type = "mobile_app_notification_action"
        event_data = {}
        if "action" in config:
            event_data["action"] = config["action"]
    else:
        # Specific action type
        event_type = "mobile_app_notification_action"
        event_data = {}
        if trigger_type in TRIGGER_ACTION_MAP:
            event_data["action"] = TRIGGER_ACTION_MAP[trigger_type]
    
    # Add category filter if specified
    if "category" in config:
        event_data["category"] = config["category"]
    
    event_config = {
        event_trigger.CONF_PLATFORM: "event",
        event_trigger.CONF_EVENT_TYPE: event_type,
    }
    
    if event_data:
        event_config[event_trigger.CONF_EVENT_DATA] = event_data
    
    event_config = event_trigger.TRIGGER_SCHEMA(event_config)
    
    return await event_trigger.async_attach_trigger(
        hass, event_config, action, trigger_info, platform_type="device"
    )


async def async_get_trigger_capabilities(
    hass: HomeAssistant, config: ConfigType
) -> dict[str, vol.Schema]:
    """Return trigger capabilities."""
    trigger_type = config.get(CONF_TYPE)
    
    # Base capabilities
    capabilities = {}
    
    # For action_received, allow custom action input
    if trigger_type == "action_received":
        capabilities["extra_fields"] = vol.Schema(
            {
                vol.Optional("action"): cv.string,
                vol.Optional("category"): vol.In(list(DEFAULT_CATEGORIES.keys())),
            }
        )
    elif trigger_type in ["notification_sent", "notification_cleared"]:
        capabilities["extra_fields"] = vol.Schema(
            {
                vol.Optional("category"): vol.In(list(DEFAULT_CATEGORIES.keys())),
            }
        )
    
    return capabilities
