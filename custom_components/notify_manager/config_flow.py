"""Config flow for Notify Manager integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector

from .const import (
    DOMAIN,
    CONF_DEVICES,
    CONF_CATEGORIES,
    CONF_DEFAULT_PRIORITY,
    CONF_ENABLE_HISTORY,
    CONF_SHOW_SIDEBAR,
    DEFAULT_CATEGORIES,
    PRIORITY_LEVELS,
)

_LOGGER = logging.getLogger(__name__)


def _get_mobile_app_devices(hass: HomeAssistant) -> list[str]:
    """Get list of available mobile app devices."""
    devices = []
    for service in hass.services.async_services().get("notify", {}):
        if service.startswith("mobile_app_"):
            device_name = service.replace("mobile_app_", "")
            devices.append(device_name)
    return devices


class NotifyManagerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Notify Manager."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._devices: list[str] = []
        self._selected_devices: list[str] = []
        self._categories: dict = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        # Check if already configured
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        errors: dict[str, str] = {}

        # Get available mobile app devices
        self._devices = _get_mobile_app_devices(self.hass)

        if not self._devices:
            return self.async_abort(
                reason="no_devices",
                description_placeholders={
                    "info": "Keine Mobile App Geräte gefunden. Bitte richte zuerst die Home Assistant Companion App ein."
                },
            )

        if user_input is not None:
            self._selected_devices = user_input.get(CONF_DEVICES, [])
            
            if not self._selected_devices:
                errors["base"] = "no_devices_selected"
            else:
                return await self.async_step_categories()

        # Build device options
        device_options = [
            selector.SelectOptionDict(value=device, label=device.replace("_", " ").title())
            for device in self._devices
        ]

        data_schema = vol.Schema(
            {
                vol.Required(CONF_DEVICES, default=self._devices): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=device_options,
                        multiple=True,
                        mode=selector.SelectSelectorMode.LIST,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                "device_count": str(len(self._devices)),
            },
        )

    async def async_step_categories(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Configure notification categories."""
        if user_input is not None:
            # Build categories from input
            categories = {}
            for cat_id, cat_default in DEFAULT_CATEGORIES.items():
                categories[cat_id] = {
                    **cat_default,
                    "enabled": user_input.get(f"cat_{cat_id}", True),
                }
            
            self._categories = categories
            return await self.async_step_settings()

        # Build schema for category toggles
        schema_dict = {}
        for cat_id, cat_config in DEFAULT_CATEGORIES.items():
            schema_dict[vol.Optional(f"cat_{cat_id}", default=True)] = selector.BooleanSelector()

        return self.async_show_form(
            step_id="categories",
            data_schema=vol.Schema(schema_dict),
            description_placeholders={
                "categories": ", ".join(
                    cat["name"] for cat in DEFAULT_CATEGORIES.values()
                )
            },
        )

    async def async_step_settings(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Configure general settings."""
        if user_input is not None:
            # Create the config entry
            return self.async_create_entry(
                title="Notify Manager",
                data={
                    CONF_DEVICES: self._selected_devices,
                    CONF_CATEGORIES: self._categories,
                    CONF_DEFAULT_PRIORITY: user_input.get(CONF_DEFAULT_PRIORITY, "normal"),
                    CONF_ENABLE_HISTORY: user_input.get(CONF_ENABLE_HISTORY, True),
                    CONF_SHOW_SIDEBAR: user_input.get(CONF_SHOW_SIDEBAR, True),
                },
            )

        priority_options = [
            selector.SelectOptionDict(value=p, label=p.title())
            for p in PRIORITY_LEVELS
        ]

        data_schema = vol.Schema(
            {
                vol.Optional(CONF_DEFAULT_PRIORITY, default="normal"): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=priority_options,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
                vol.Optional(CONF_ENABLE_HISTORY, default=True): selector.BooleanSelector(),
                vol.Optional(CONF_SHOW_SIDEBAR, default=True): selector.BooleanSelector(),
            }
        )

        return self.async_show_form(
            step_id="settings",
            data_schema=data_schema,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> NotifyManagerOptionsFlow:
        """Get the options flow for this handler."""
        return NotifyManagerOptionsFlow(config_entry)


class NotifyManagerOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Notify Manager."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options - show menu."""
        return self.async_show_menu(
            step_id="init",
            menu_options=["devices", "categories", "settings", "open_panel"],
        )

    async def async_step_open_panel(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Redirect to panel - this is handled via frontend."""
        # This step just shows info, the actual navigation is done in the frontend
        return self.async_abort(reason="panel_opened")

    async def async_step_devices(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Configure devices."""
        errors: dict[str, str] = {}
        
        available_devices = _get_mobile_app_devices(self.hass)
        current_devices = self._config_entry.data.get(CONF_DEVICES, [])

        if user_input is not None:
            selected_devices = user_input.get(CONF_DEVICES, [])
            if not selected_devices:
                errors["base"] = "no_devices_selected"
            else:
                # Update config entry
                new_data = {**self._config_entry.data, CONF_DEVICES: selected_devices}
                self.hass.config_entries.async_update_entry(
                    self._config_entry, data=new_data
                )
                return self.async_create_entry(title="", data={})

        device_options = [
            selector.SelectOptionDict(value=device, label=device.replace("_", " ").title())
            for device in available_devices
        ]

        data_schema = vol.Schema(
            {
                vol.Required(CONF_DEVICES, default=current_devices): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=device_options,
                        multiple=True,
                        mode=selector.SelectSelectorMode.LIST,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="devices",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_categories(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Configure categories."""
        current_categories = self._config_entry.data.get(CONF_CATEGORIES, DEFAULT_CATEGORIES)

        if user_input is not None:
            categories = {}
            for cat_id, cat_default in DEFAULT_CATEGORIES.items():
                current_cat = current_categories.get(cat_id, cat_default)
                categories[cat_id] = {
                    **current_cat,
                    "enabled": user_input.get(f"cat_{cat_id}", True),
                    "priority": user_input.get(f"priority_{cat_id}", current_cat.get("priority", "normal")),
                }

            new_data = {**self._config_entry.data, CONF_CATEGORIES: categories}
            self.hass.config_entries.async_update_entry(
                self._config_entry, data=new_data
            )
            return self.async_create_entry(title="", data={})

        schema_dict = {}
        priority_options = [
            selector.SelectOptionDict(value=p, label=p.title())
            for p in PRIORITY_LEVELS
        ]

        for cat_id, cat_config in DEFAULT_CATEGORIES.items():
            current_cat = current_categories.get(cat_id, cat_config)
            schema_dict[vol.Optional(f"cat_{cat_id}", default=current_cat.get("enabled", True))] = selector.BooleanSelector()
            schema_dict[vol.Optional(f"priority_{cat_id}", default=current_cat.get("priority", "normal"))] = selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=priority_options,
                    mode=selector.SelectSelectorMode.DROPDOWN,
                )
            )

        return self.async_show_form(
            step_id="categories",
            data_schema=vol.Schema(schema_dict),
        )

    async def async_step_settings(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Configure general settings."""
        current_show_sidebar = self._config_entry.data.get(CONF_SHOW_SIDEBAR, True)
        current_history = self._config_entry.data.get(CONF_ENABLE_HISTORY, True)
        current_priority = self._config_entry.data.get(CONF_DEFAULT_PRIORITY, "normal")

        if user_input is not None:
            new_data = {
                **self._config_entry.data,
                CONF_SHOW_SIDEBAR: user_input.get(CONF_SHOW_SIDEBAR, True),
                CONF_ENABLE_HISTORY: user_input.get(CONF_ENABLE_HISTORY, True),
                CONF_DEFAULT_PRIORITY: user_input.get(CONF_DEFAULT_PRIORITY, "normal"),
            }
            self.hass.config_entries.async_update_entry(
                self._config_entry, data=new_data
            )
            # Trigger reload to apply sidebar change
            await self.hass.config_entries.async_reload(self._config_entry.entry_id)
            return self.async_create_entry(title="", data={})

        priority_options = [
            selector.SelectOptionDict(value=p, label=p.title())
            for p in PRIORITY_LEVELS
        ]

        data_schema = vol.Schema(
            {
                vol.Optional(CONF_SHOW_SIDEBAR, default=current_show_sidebar): selector.BooleanSelector(),
                vol.Optional(CONF_ENABLE_HISTORY, default=current_history): selector.BooleanSelector(),
                vol.Optional(CONF_DEFAULT_PRIORITY, default=current_priority): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=priority_options,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        )

        return self.async_show_form(
            step_id="settings",
            data_schema=data_schema,
        )
