"""Triggers for Notify Manager integration.

Ermöglicht die Auswahl von Notify Manager Events als Auslöser in Automationen.
"""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.const import CONF_PLATFORM
from homeassistant.core import CALLBACK_TYPE, HassJob, HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.trigger import TriggerActionType, TriggerInfo
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, ACTION_TEMPLATES

_LOGGER = logging.getLogger(__name__)

# Trigger types
TRIGGER_ACTION_RECEIVED = "action_received"
TRIGGER_NOTIFICATION_SENT = "notification_sent"
TRIGGER_NOTIFICATION_CLEARED = "notification_cleared"

# Config keys
CONF_ACTION = "action"
CONF_ACTIONS = "actions"
CONF_DEVICE = "device"
CONF_CATEGORY = "category"
CONF_TEMPLATE = "action_template"

# Schema for action_received trigger
TRIGGER_ACTION_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_PLATFORM): DOMAIN,
        vol.Required("type"): vol.In([
            TRIGGER_ACTION_RECEIVED,
            TRIGGER_NOTIFICATION_SENT,
            TRIGGER_NOTIFICATION_CLEARED,
        ]),
        vol.Optional(CONF_ACTION): cv.string,
        vol.Optional(CONF_ACTIONS): vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(CONF_DEVICE): cv.string,
        vol.Optional(CONF_CATEGORY): cv.string,
        vol.Optional(CONF_TEMPLATE): vol.In(list(ACTION_TEMPLATES.keys())),
    }
)


async def async_validate_trigger_config(
    hass: HomeAssistant, config: ConfigType
) -> ConfigType:
    """Validate trigger config."""
    return TRIGGER_ACTION_SCHEMA(config)


async def async_get_triggers(hass: HomeAssistant) -> list[dict[str, Any]]:
    """Return a list of triggers for the UI."""
    return [
        {
            "platform": DOMAIN,
            "type": TRIGGER_ACTION_RECEIVED,
            "name": "Benachrichtigungs-Aktion empfangen",
            "description": "Wird ausgelöst wenn ein Button in einer Benachrichtigung gedrückt wird",
        },
        {
            "platform": DOMAIN,
            "type": TRIGGER_NOTIFICATION_SENT,
            "name": "Benachrichtigung gesendet",
            "description": "Wird ausgelöst wenn eine Benachrichtigung gesendet wurde",
        },
        {
            "platform": DOMAIN,
            "type": TRIGGER_NOTIFICATION_CLEARED,
            "name": "Benachrichtigung gelöscht",
            "description": "Wird ausgelöst wenn eine Benachrichtigung vom Benutzer gelöscht wurde",
        },
    ]


async def async_attach_trigger(
    hass: HomeAssistant,
    config: ConfigType,
    action: TriggerActionType,
    trigger_info: TriggerInfo,
) -> CALLBACK_TYPE:
    """Attach a trigger."""
    trigger_type = config["type"]
    trigger_data = {
        "platform": DOMAIN,
        "type": trigger_type,
    }
    
    job = HassJob(action, f"Notify Manager trigger {trigger_type}")
    
    @callback
    def handle_event(event):
        """Handle the event."""
        event_data = event.data
        
        # Filter by action if specified
        if CONF_ACTION in config:
            if event_data.get("action") != config[CONF_ACTION]:
                return
        
        # Filter by actions list if specified
        if CONF_ACTIONS in config:
            if event_data.get("action") not in config[CONF_ACTIONS]:
                return
        
        # Filter by device if specified
        if CONF_DEVICE in config:
            if event_data.get("device_id") != config[CONF_DEVICE]:
                return
        
        # Filter by category if specified
        if CONF_CATEGORY in config:
            if event_data.get("category") != config[CONF_CATEGORY]:
                return
        
        # Filter by template actions if specified
        if CONF_TEMPLATE in config:
            template_name = config[CONF_TEMPLATE]
            template_actions = [a["action"] for a in ACTION_TEMPLATES.get(template_name, [])]
            if event_data.get("action") not in template_actions:
                return
        
        # Build trigger data
        run_variables = {
            "trigger": {
                **trigger_data,
                "action": event_data.get("action"),
                "action_data": event_data,
                "device_id": event_data.get("device_id"),
                "title": event_data.get("title"),
                "message": event_data.get("message"),
                "category": event_data.get("category"),
                "tag": event_data.get("tag"),
                "reply_text": event_data.get("reply_text"),
            }
        }
        
        hass.async_run_hass_job(job, {"trigger": run_variables["trigger"]})
    
    # Determine which event to listen to
    if trigger_type == TRIGGER_ACTION_RECEIVED:
        event_type = f"{DOMAIN}_action_received"
    elif trigger_type == TRIGGER_NOTIFICATION_SENT:
        event_type = f"{DOMAIN}_notification_sent"
    elif trigger_type == TRIGGER_NOTIFICATION_CLEARED:
        event_type = f"{DOMAIN}_notification_cleared"
    else:
        event_type = f"{DOMAIN}_action_received"
    
    # Also listen to mobile_app events
    unsub_custom = hass.bus.async_listen(event_type, handle_event)
    unsub_mobile = hass.bus.async_listen("mobile_app_notification_action", handle_event)
    
    @callback
    def async_remove():
        """Remove trigger."""
        unsub_custom()
        unsub_mobile()
    
    return async_remove


# Device trigger schema for UI
TRIGGER_SCHEMA = vol.All(
    vol.Schema(
        {
            vol.Required(CONF_PLATFORM): DOMAIN,
            vol.Required("type"): vol.In([
                TRIGGER_ACTION_RECEIVED,
                TRIGGER_NOTIFICATION_SENT,
                TRIGGER_NOTIFICATION_CLEARED,
            ]),
            vol.Optional(CONF_ACTION): cv.string,
            vol.Optional(CONF_ACTIONS): vol.All(cv.ensure_list, [cv.string]),
            vol.Optional(CONF_DEVICE): cv.string,
            vol.Optional(CONF_CATEGORY): cv.string,
            vol.Optional(CONF_TEMPLATE): vol.In(list(ACTION_TEMPLATES.keys())),
        },
        extra=vol.ALLOW_EXTRA,
    ),
)
