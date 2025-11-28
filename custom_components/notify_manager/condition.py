"""Conditions for Notify Manager integration.

Ermöglicht die Verwendung von Notify Manager Zuständen als Bedingungen in Automationen.
"""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.const import CONF_CONDITION
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.condition import ConditionCheckerType
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, DEFAULT_CATEGORIES

_LOGGER = logging.getLogger(__name__)

# Condition types
CONDITION_CATEGORY_ENABLED = "category_enabled"
CONDITION_DEVICE_AVAILABLE = "device_available"
CONDITION_LAST_ACTION = "last_action"

# Config keys
CONF_CATEGORY = "category"
CONF_DEVICE = "device"
CONF_ACTION = "action"
CONF_WITHIN_SECONDS = "within_seconds"


CONDITION_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_CONDITION): DOMAIN,
        vol.Required("type"): vol.In([
            CONDITION_CATEGORY_ENABLED,
            CONDITION_DEVICE_AVAILABLE,
            CONDITION_LAST_ACTION,
        ]),
        vol.Optional(CONF_CATEGORY): vol.In(list(DEFAULT_CATEGORIES.keys())),
        vol.Optional(CONF_DEVICE): cv.string,
        vol.Optional(CONF_ACTION): cv.string,
        vol.Optional(CONF_WITHIN_SECONDS, default=300): cv.positive_int,
    }
)


async def async_validate_condition_config(
    hass: HomeAssistant, config: ConfigType
) -> ConfigType:
    """Validate condition config."""
    return CONDITION_SCHEMA(config)


async def async_get_conditions(hass: HomeAssistant) -> list[dict[str, Any]]:
    """Return a list of conditions for the UI."""
    return [
        {
            "condition": DOMAIN,
            "type": CONDITION_CATEGORY_ENABLED,
            "name": "Kategorie aktiviert",
            "description": "Prüft ob eine Benachrichtigungs-Kategorie aktiviert ist",
        },
        {
            "condition": DOMAIN,
            "type": CONDITION_DEVICE_AVAILABLE,
            "name": "Gerät verfügbar",
            "description": "Prüft ob ein Benachrichtigungs-Gerät verfügbar ist",
        },
        {
            "condition": DOMAIN,
            "type": CONDITION_LAST_ACTION,
            "name": "Letzte Aktion war",
            "description": "Prüft ob die letzte Button-Aktion einem bestimmten Wert entspricht",
        },
    ]


@callback
def async_condition_from_config(
    hass: HomeAssistant, config: ConfigType
) -> ConditionCheckerType:
    """Create a condition from config."""
    condition_type = config["type"]
    
    @callback
    def check_condition(hass: HomeAssistant, variables: dict[str, Any] | None = None) -> bool:
        """Check the condition."""
        domain_data = hass.data.get(DOMAIN, {})
        
        if condition_type == CONDITION_CATEGORY_ENABLED:
            category = config.get(CONF_CATEGORY)
            if not category:
                return False
            
            # Find config entry data
            for entry_data in domain_data.values():
                if isinstance(entry_data, dict) and "categories" in entry_data:
                    categories = entry_data.get("categories", {})
                    cat_config = categories.get(category, {})
                    return cat_config.get("enabled", True)
            
            return True  # Default to enabled if not found
        
        elif condition_type == CONDITION_DEVICE_AVAILABLE:
            device = config.get(CONF_DEVICE)
            if not device:
                return False
            
            # Check if notify service exists
            notify_services = hass.services.async_services().get("notify", {})
            service_name = f"mobile_app_{device}"
            return service_name in notify_services
        
        elif condition_type == CONDITION_LAST_ACTION:
            action = config.get(CONF_ACTION)
            within_seconds = config.get(CONF_WITHIN_SECONDS, 300)
            
            if not action:
                return False
            
            # Check last action in domain data
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
        
        return False
    
    return check_condition
