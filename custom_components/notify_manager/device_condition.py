"""Device conditions for Notify Manager integration.

Ermöglicht die Verwendung von Notify Manager Bedingungen in der Automations-UI.
"""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.components.device_automation import DEVICE_CONDITION_BASE_SCHEMA
from homeassistant.const import (
    CONF_CONDITION,
    CONF_DEVICE_ID,
    CONF_DOMAIN,
    CONF_TYPE,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import condition, config_validation as cv, device_registry as dr
from homeassistant.helpers.typing import ConfigType, TemplateVarsType

from .const import DOMAIN, DEFAULT_CATEGORIES

_LOGGER = logging.getLogger(__name__)

# All possible actions from templates and common use
KNOWN_ACTIONS = {
    "CONFIRM": "✅ Bestätigen",
    "DISMISS": "❌ Ablehnen",
    "YES": "👍 Ja",
    "NO": "👎 Nein",
    "ALARM_CONFIRM": "🚨 Alarm OK",
    "ALARM_SNOOZE": "⏰ Alarm Später",
    "ALARM_EMERGENCY": "🆘 Notfall",
    "DOOR_UNLOCK": "🔓 Tür öffnen",
    "DOOR_IGNORE": "🚪 Tür ignorieren",
    "DOOR_SPEAK": "🔊 Sprechen",
    "REPLY": "💬 Antwort",
}

# Condition types
CONDITION_TYPES = {
    "last_action_was": "Letzte Button-Aktion war",
    "category_enabled": "Kategorie ist aktiviert",
    "category_disabled": "Kategorie ist deaktiviert",
    "device_available": "Gerät ist verfügbar",
    "has_pending_action": "Hat ausstehende Aktion",
}

CONDITION_SCHEMA = DEVICE_CONDITION_BASE_SCHEMA.extend(
    {
        vol.Required(CONF_TYPE): vol.In(CONDITION_TYPES.keys()),
        vol.Optional("category"): vol.In(list(DEFAULT_CATEGORIES.keys())),
        vol.Optional("action"): cv.string,
        vol.Optional("device"): cv.string,
        vol.Optional("within_seconds", default=300): cv.positive_int,
    }
)


async def async_get_conditions(
    hass: HomeAssistant, device_id: str
) -> list[dict[str, Any]]:
    """Return a list of conditions for a device."""
    device_registry = dr.async_get(hass)
    device = device_registry.async_get(device_id)
    
    if not device:
        return []
    
    # Check if this is a Notify Manager device
    if not any(identifier[0] == DOMAIN for identifier in device.identifiers):
        return []
    
    conditions = []
    
    for condition_type in CONDITION_TYPES:
        conditions.append(
            {
                CONF_CONDITION: "device",
                CONF_DEVICE_ID: device_id,
                CONF_DOMAIN: DOMAIN,
                CONF_TYPE: condition_type,
            }
        )
    
    return conditions


async def async_validate_condition_config(
    hass: HomeAssistant, config: ConfigType
) -> ConfigType:
    """Validate config."""
    return CONDITION_SCHEMA(config)


@callback
def async_condition_from_config(
    hass: HomeAssistant, config: ConfigType
) -> condition.ConditionCheckerType:
    """Create a condition from config."""
    condition_type = config[CONF_TYPE]
    
    @callback
    def test_condition(
        hass: HomeAssistant, variables: TemplateVarsType = None
    ) -> bool:
        """Test the condition."""
        domain_data = hass.data.get(DOMAIN, {})
        
        if condition_type == "category_enabled":
            category = config.get("category")
            if not category:
                return True
            
            for entry_data in domain_data.values():
                if isinstance(entry_data, dict) and "categories" in entry_data:
                    categories = entry_data.get("categories", {})
                    cat_config = categories.get(category, {})
                    return cat_config.get("enabled", True)
            return True
        
        elif condition_type == "category_disabled":
            category = config.get("category")
            if not category:
                return False
            
            for entry_data in domain_data.values():
                if isinstance(entry_data, dict) and "categories" in entry_data:
                    categories = entry_data.get("categories", {})
                    cat_config = categories.get(category, {})
                    return not cat_config.get("enabled", True)
            return False
        
        elif condition_type == "device_available":
            device = config.get("device")
            if not device:
                return False
            
            notify_services = hass.services.async_services().get("notify", {})
            service_name = f"mobile_app_{device}"
            return service_name in notify_services
        
        elif condition_type == "last_action_was":
            action = config.get("action")
            within_seconds = config.get("within_seconds", 300)
            
            if not action:
                return False
            
            for entry_data in domain_data.values():
                if isinstance(entry_data, dict) and "pending_actions" in entry_data:
                    pending = entry_data.get("pending_actions", {})
                    if action in pending:
                        from datetime import datetime, timedelta
                        action_data = pending[action]
                        timestamp_str = action_data.get("timestamp")
                        if timestamp_str:
                            try:
                                timestamp = datetime.fromisoformat(timestamp_str)
                                if datetime.now() - timestamp < timedelta(seconds=within_seconds):
                                    return True
                            except (ValueError, TypeError):
                                pass
            return False
        
        elif condition_type == "has_pending_action":
            for entry_data in domain_data.values():
                if isinstance(entry_data, dict) and "pending_actions" in entry_data:
                    pending = entry_data.get("pending_actions", {})
                    if pending:
                        return True
            return False
        
        return False
    
    return test_condition


async def async_get_condition_capabilities(
    hass: HomeAssistant, config: ConfigType
) -> dict[str, vol.Schema]:
    """Return condition capabilities."""
    condition_type = config.get(CONF_TYPE)
    
    if condition_type in ["category_enabled", "category_disabled"]:
        return {
            "extra_fields": vol.Schema(
                {
                    vol.Required("category"): vol.In(list(DEFAULT_CATEGORIES.keys())),
                }
            )
        }
    
    elif condition_type == "device_available":
        # Get available devices
        devices = []
        for service in hass.services.async_services().get("notify", {}):
            if service.startswith("mobile_app_"):
                devices.append(service.replace("mobile_app_", ""))
        
        if devices:
            return {
                "extra_fields": vol.Schema(
                    {
                        vol.Required("device"): vol.In(devices),
                    }
                )
            }
        return {}
    
    elif condition_type == "last_action_was":
        # Provide dropdown with known actions
        return {
            "extra_fields": vol.Schema(
                {
                    vol.Required("action"): vol.In(list(KNOWN_ACTIONS.keys())),
                    vol.Optional("within_seconds", default=300): cv.positive_int,
                }
            )
        }
    
    return {}
