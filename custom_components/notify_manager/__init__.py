"""Notify Manager - Comprehensive notification management for Home Assistant Companion App.

Diese Integration bietet eine vollständige Verwaltung für Mobile App Benachrichtigungen:
- Actionable Notifications mit Buttons
- Kritische Benachrichtigungen (durchbrechen Nicht-Stören)
- Bilder und Kamera-Snapshots
- Text-Input Antworten
- Callback-Handling für Button-Aktionen
- Kategorien-basierte Filterung
"""
from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import voluptuous as vol

from homeassistant.components import frontend
from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall, callback, Event
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN,
    CONF_DEVICES,
    CONF_CATEGORIES,
    CONF_DEFAULT_PRIORITY,
    CONF_SHOW_SIDEBAR,
    SERVICE_SEND_NOTIFICATION,
    SERVICE_SEND_ACTIONABLE,
    SERVICE_CLEAR_NOTIFICATIONS,
    SERVICE_SEND_ALARM_CONFIRMATION,
    SERVICE_SEND_WITH_IMAGE,
    SERVICE_SEND_TEXT_INPUT,
    ATTR_TITLE,
    ATTR_MESSAGE,
    ATTR_TARGET,
    ATTR_CATEGORY,
    ATTR_PRIORITY,
    ATTR_DATA,
    ATTR_ACTIONS,
    ATTR_TAG,
    ATTR_IMAGE,
    ATTR_CAMERA,
    ATTR_GROUP,
    ATTR_CHANNEL,
    ATTR_CLICKACTION,
    ATTR_PERSISTENT,
    ATTR_STICKY,
    ATTR_TIMEOUT,
    ATTR_COLOR,
    ATTR_SUBTITLE,
    ATTR_SUBJECT,
    ATTR_BADGE,
    ATTR_ICON,
    ATTR_VISIBILITY,
    ATTR_VIBRATION,
    ATTR_LED_COLOR,
    ATTR_ALERT_ONCE,
    ATTR_NOTIFICATION_ICON,
    ATTR_CAR_UI,
    ATTR_VIDEO,
    ATTR_AUDIO,
    EVENT_NOTIFICATION_ACTION,
    DEFAULT_CATEGORIES,
    PRIORITY_LEVELS,
    ACTION_TEMPLATES,
)
from .additional_services import (
    async_register_additional_services,
    async_unregister_additional_services,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.SWITCH, Platform.SELECT, Platform.BUTTON]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

# ============================================================================
# SERVICE SCHEMAS
# ============================================================================

# Schema für einzelne Aktion (Button)
ACTION_SCHEMA = vol.Schema(
    {
        vol.Required("action"): cv.string,
        vol.Required("title"): cv.string,
        vol.Optional("uri"): cv.string,
        vol.Optional("icon"): cv.string,
        vol.Optional("destructive"): cv.boolean,
        vol.Optional("authenticationRequired"): cv.boolean,
        vol.Optional("behavior"): cv.string,
        vol.Optional("textInputButtonTitle"): cv.string,
        vol.Optional("textInputPlaceholder"): cv.string,
    }
)

# Basis-Benachrichtigung
SEND_NOTIFICATION_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_TITLE): cv.string,
        vol.Required(ATTR_MESSAGE): cv.string,
        vol.Optional(ATTR_TARGET): vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(ATTR_CATEGORY): cv.string,
        vol.Optional(ATTR_PRIORITY, default="normal"): vol.In(["low", "normal", "high", "critical"]),
        vol.Optional(ATTR_TAG): cv.string,
        vol.Optional(ATTR_GROUP): cv.string,
        vol.Optional(ATTR_CHANNEL): cv.string,
        vol.Optional(ATTR_CLICKACTION): cv.string,
        vol.Optional(ATTR_DATA): dict,
    }
)

# Actionable Notification (mit Buttons)
SEND_ACTIONABLE_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_TITLE): cv.string,
        vol.Required(ATTR_MESSAGE): cv.string,
        vol.Required(ATTR_ACTIONS): vol.All(cv.ensure_list, [ACTION_SCHEMA]),
        vol.Optional(ATTR_TARGET): vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(ATTR_CATEGORY): cv.string,
        vol.Optional(ATTR_PRIORITY, default="high"): vol.In(["low", "normal", "high", "critical"]),
        vol.Optional(ATTR_TAG): cv.string,
        vol.Optional(ATTR_GROUP): cv.string,
        vol.Optional(ATTR_PERSISTENT): cv.boolean,
        vol.Optional(ATTR_STICKY): cv.boolean,
        vol.Optional(ATTR_TIMEOUT): cv.positive_int,
        vol.Optional(ATTR_CLICKACTION): cv.string,
        vol.Optional(ATTR_DATA): dict,
    }
)

# Benachrichtigung mit Bild oder Kamera
SEND_WITH_IMAGE_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_TITLE): cv.string,
        vol.Required(ATTR_MESSAGE): cv.string,
        vol.Exclusive(ATTR_IMAGE, "image_source"): cv.string,
        vol.Exclusive(ATTR_CAMERA, "image_source"): cv.entity_id,
        vol.Optional(ATTR_ACTIONS): vol.All(cv.ensure_list, [ACTION_SCHEMA]),
        vol.Optional(ATTR_TARGET): vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(ATTR_CATEGORY): cv.string,
        vol.Optional(ATTR_PRIORITY, default="normal"): vol.In(["low", "normal", "high", "critical"]),
        vol.Optional(ATTR_TAG): cv.string,
        vol.Optional(ATTR_DATA): dict,
    }
)

# Alarm-Bestätigung (vorgefertigte Buttons)
SEND_ALARM_CONFIRMATION_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_TITLE): cv.string,
        vol.Required(ATTR_MESSAGE): cv.string,
        vol.Optional(ATTR_TARGET): vol.All(cv.ensure_list, [cv.string]),
        vol.Optional("alarm_entity"): cv.entity_id,
        vol.Optional("template"): vol.In(["alarm_response", "confirm_dismiss", "door_response", "yes_no"]),
        vol.Optional(ATTR_TAG, default="alarm_confirmation"): cv.string,
        vol.Optional(ATTR_DATA): dict,
    }
)

# Text-Input Benachrichtigung
SEND_TEXT_INPUT_SCHEMA = vol.Schema(
    {
        vol.Required(ATTR_TITLE): cv.string,
        vol.Required(ATTR_MESSAGE): cv.string,
        vol.Optional("input_title", default="Antworten"): cv.string,
        vol.Optional("placeholder", default="Nachricht eingeben..."): cv.string,
        vol.Optional(ATTR_TARGET): vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(ATTR_TAG): cv.string,
        vol.Optional(ATTR_DATA): dict,
    }
)

# Benachrichtigungen löschen
CLEAR_NOTIFICATIONS_SCHEMA = vol.Schema(
    {
        vol.Optional(ATTR_TARGET): vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(ATTR_TAG): cv.string,
    }
)


# ============================================================================
# SETUP FUNCTIONS
# ============================================================================

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Notify Manager component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Notify Manager from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Store config entry data
    hass.data[DOMAIN][entry.entry_id] = {
        "config": entry.data,
        "devices": entry.data.get(CONF_DEVICES, []),
        "categories": entry.data.get(CONF_CATEGORIES, DEFAULT_CATEGORIES),
        "notification_history": [],
        "pending_actions": {},
    }
    
    # Register frontend panel (with sidebar option)
    show_sidebar = entry.data.get(CONF_SHOW_SIDEBAR, True)
    await _async_register_panel(hass, show_sidebar)
    
    # Register services
    await _async_register_services(hass, entry)
    
    # Register additional services (TTS, Maps, Commands)
    await async_register_additional_services(hass, entry)
    
    # Register event listener for notification actions
    await _async_register_action_listener(hass, entry)
    
    # Set up platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Register update listener
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    
    return True


async def _async_register_panel(hass: HomeAssistant, show_sidebar: bool = True) -> None:
    """Register the frontend panel."""
    frontend_path = Path(__file__).parent / "frontend"
    
    await hass.http.async_register_static_paths(
        [StaticPathConfig("/notify_manager_static", str(frontend_path), cache_headers=False)]
    )
    
    # Version for cache busting
    VERSION = "1.2.1"
    
    frontend.async_register_built_in_panel(
        hass,
        component_name="custom",
        sidebar_title="Notify Manager" if show_sidebar else None,
        sidebar_icon="mdi:bell-cog" if show_sidebar else None,
        frontend_url_path="notify-manager",
        config={
            "_panel_custom": {
                "name": "notify-manager-panel",
                "embed_iframe": False,
                "trust_external": False,
                "module_url": f"/notify_manager_static/notify-manager-panel.js?v={VERSION}",
            }
        },
        require_admin=False,
    )


async def _async_register_action_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Register listener for mobile_app_notification_action events."""
    
    @callback
    def handle_notification_action(event: Event) -> None:
        """Handle notification action events from Companion App."""
        action = event.data.get("action")
        action_data = event.data
        
        _LOGGER.debug("Received notification action: %s with data: %s", action, action_data)
        
        # Store action in pending actions for processing
        config_data = hass.data[DOMAIN].get(entry.entry_id, {})
        config_data.setdefault("pending_actions", {})[action] = {
            "data": action_data,
            "timestamp": datetime.now().isoformat(),
        }
        
        # Fire a custom event that automations can listen to
        hass.bus.async_fire(
            f"{DOMAIN}_action_received",
            {
                "action": action,
                "reply_text": action_data.get("reply_text"),
                "source_device": action_data.get("sourceDeviceID"),
                "tag": action_data.get("tag"),
                **action_data,
            },
        )
        
        # Add to history
        history_entry = {
            "type": "action_received",
            "action": action,
            "data": action_data,
            "timestamp": datetime.now().isoformat(),
        }
        config_data.setdefault("notification_history", []).append(history_entry)
        config_data["notification_history"] = config_data["notification_history"][-100:]
    
    # Listen for mobile app notification actions
    hass.bus.async_listen(EVENT_NOTIFICATION_ACTION, handle_notification_action)


# ============================================================================
# SERVICE HANDLERS
# ============================================================================

async def _async_register_services(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Register Notify Manager services."""
    
    def _build_notification_data(
        priority: str,
        category: str | None,
        tag: str | None,
        extra_data: dict | None,
        actions: list | None = None,
        image: str | None = None,
        video: str | None = None,
        audio: str | None = None,
        camera_entity: str | None = None,
        persistent: bool = False,
        sticky: bool = False,
        timeout: int | None = None,
        clickaction: str | None = None,
        group: str | None = None,
        channel: str | None = None,
        action_data: dict | None = None,
        # Neue Parameter für alle Companion App Features
        subtitle: str | None = None,
        subject: str | None = None,
        color: str | None = None,
        vibration_pattern: str | None = None,
        led_color: str | None = None,
        icon_url: str | None = None,
        notification_icon: str | None = None,
        visibility: str | None = None,
        alert_once: bool = False,
        car_ui: bool = False,
        badge: int | None = None,
        sound: str | None = None,
        presentation_options: list | None = None,
        # Progress & Chronometer
        progress: int | None = None,
        progress_max: int | None = None,
        progress_indeterminate: bool = False,
        chronometer: bool = False,
        when: int | None = None,
        when_relative: bool = False,
        # Attachment options (iOS)
        attachment_hide_thumbnail: bool = False,
        attachment_lazy: bool = False,
        attachment_content_type: str | None = None,
    ) -> dict:
        """Build notification data dict for Companion App.
        
        Supports ALL Companion App features:
        - iOS: interruption-level, critical sounds, SF Symbols, badges, presentation_options
        - Android: channels, importance, LED, vibration, progress bars, chronometer, car_ui
        - Both: actions, images, video, audio, tags, groups
        """
        data = {}
        config_data = hass.data[DOMAIN].get(entry.entry_id, {})
        categories = config_data.get("categories", DEFAULT_CATEGORIES)
        
        # Get priority settings
        priority_config = PRIORITY_LEVELS.get(priority, PRIORITY_LEVELS["normal"])
        
        # Get category settings if specified
        cat_config = categories.get(category, {}) if category else {}
        
        # =====================================================================
        # iOS Settings (push object)
        # =====================================================================
        push_data = {}
        
        # Sound configuration
        if priority == "critical" or priority_config.get("critical"):
            # Critical notification - overrides DND
            push_data["sound"] = {
                "name": sound or "default",
                "critical": 1,
                "volume": 1.0,
            }
        elif sound:
            if sound == "none":
                push_data["sound"] = "none"
            else:
                push_data["sound"] = sound
        elif cat_config.get("sound"):
            push_data["sound"] = cat_config["sound"]
        
        # Interruption level (iOS 15+)
        if priority == "critical":
            push_data["interruption-level"] = "critical"
        elif priority == "high":
            push_data["interruption-level"] = "time-sensitive"
        elif priority == "low":
            push_data["interruption-level"] = "passive"
        else:
            push_data["interruption-level"] = cat_config.get(
                "interruption_level", 
                priority_config.get("interruption_level", "active")
            )
        
        # Badge (iOS)
        if badge is not None:
            push_data["badge"] = badge
        
        # Presentation options (iOS) - how to display when app is foreground
        if presentation_options:
            data["presentation_options"] = presentation_options
        
        if push_data:
            data["push"] = push_data
        
        # Thread ID for iOS grouping
        if group:
            data["thread-id"] = group
        
        # Subtitle (iOS)
        if subtitle:
            data["subtitle"] = subtitle
        
        # =====================================================================
        # Android Settings
        # =====================================================================
        
        # Channel
        data["channel"] = channel or cat_config.get("channel", category or "default")
        
        # Importance
        data["importance"] = priority_config.get("importance", "default")
        
        # For critical/high on Android
        if priority in ["high", "critical"]:
            data["ttl"] = 0
            data["priority"] = "high"
        
        # Color (Android notification accent)
        if color:
            data["color"] = color
        elif cat_config.get("color"):
            data["color"] = cat_config["color"]
        
        # Subject (Android - for long text)
        if subject:
            data["subject"] = subject
        
        # Vibration Pattern (Android)
        if vibration_pattern:
            data["vibrationPattern"] = vibration_pattern
        
        # LED Color (Android)
        if led_color:
            data["ledColor"] = led_color
        
        # Icon URL (Android - custom notification icon)
        if icon_url:
            data["icon_url"] = icon_url
        
        # Notification Icon (Android - MDI icon in status bar)
        if notification_icon:
            data["notification_icon"] = notification_icon
        
        # Visibility / Lock Screen (Android)
        if visibility:
            data["visibility"] = visibility  # public, private, secret
        
        # Alert Once (Android)
        if alert_once:
            data["alert_once"] = True
        
        # Android Auto
        if car_ui:
            data["car_ui"] = True
        
        # Progress Bar (Android)
        if progress is not None:
            data["progress"] = progress
            data["progress_max"] = progress_max or 100
            if progress_indeterminate:
                data["progress_indeterminate"] = True
        
        # Chronometer / Timer (Android)
        if chronometer:
            data["chronometer"] = True
            if when is not None:
                data["when"] = when
            if when_relative:
                data["when_relative"] = True
        
        # =====================================================================
        # Common Settings (iOS & Android)
        # =====================================================================
        
        # Tag for replacing/grouping
        if tag:
            data["tag"] = tag
        
        # Group
        if group:
            data["group"] = group
        
        # Persistent notification
        if persistent:
            data["persistent"] = True
        
        # Sticky notification (Android)
        if sticky:
            data["sticky"] = True
        
        # Timeout (auto-dismiss)
        if timeout:
            data["timeout"] = timeout
        
        # Click action (URL when tapping notification)
        if clickaction:
            data["clickAction"] = clickaction  # Android
            data["url"] = clickaction  # iOS
        
        # Actions (buttons)
        if actions:
            data["actions"] = actions
        
        # Action data (returned with button clicks on iOS)
        if action_data:
            data["action_data"] = action_data
        
        # =====================================================================
        # Attachments (Image, Video, Audio)
        # =====================================================================
        
        # Image
        if image:
            data["image"] = image
        
        # Video (iOS primarily)
        if video:
            data["video"] = video
        
        # Audio (iOS primarily)
        if audio:
            data["audio"] = audio
        
        # Camera entity snapshot
        if camera_entity:
            data["entity_id"] = camera_entity
            # Also set image for Android compatibility
            data["image"] = f"/api/camera_proxy/{camera_entity}"
        
        # Attachment options (iOS)
        if attachment_hide_thumbnail or attachment_lazy or attachment_content_type:
            attachment = {}
            if attachment_hide_thumbnail:
                attachment["hide-thumbnail"] = True
            if attachment_lazy:
                attachment["lazy"] = True
            if attachment_content_type:
                attachment["content-type"] = attachment_content_type
            data["attachment"] = attachment
        
        # =====================================================================
        # Merge extra data (allows full customization)
        # =====================================================================
        if extra_data:
            for key, value in extra_data.items():
                if key in data and isinstance(data[key], dict) and isinstance(value, dict):
                    data[key].update(value)
                else:
                    data[key] = value
        
        return data
    
    async def _send_to_devices(
        title: str,
        message: str,
        targets: list[str],
        data: dict,
        category: str | None = None,
    ) -> None:
        """Send notification to specified devices."""
        config_data = hass.data[DOMAIN].get(entry.entry_id, {})
        categories = config_data.get("categories", DEFAULT_CATEGORIES)
        
        # Process targets - can be entity IDs or device names
        processed_targets = []
        if targets:
            for target in targets:
                if isinstance(target, str):
                    # Remove domain prefix if present (e.g., device_tracker.iphone -> iphone)
                    if "." in target:
                        # Entity ID format: domain.name
                        entity_id = target
                        # Try to find the corresponding mobile_app service
                        # Get the device name from the entity
                        device_name = target.split(".")[-1]
                        # Check if mobile_app service exists for this device
                        if f"mobile_app_{device_name}" in (hass.services.async_services().get("notify", {}) or {}):
                            processed_targets.append(device_name)
                        else:
                            # Try without mobile_app_ prefix check - maybe it matches
                            processed_targets.append(device_name)
                    else:
                        # Already a device name
                        processed_targets.append(target)
        
        devices = processed_targets if processed_targets else config_data.get("devices", [])
        
        # Check if category is enabled
        if category and category in categories:
            if not categories[category].get("enabled", True):
                _LOGGER.debug("Category %s is disabled, skipping notification", category)
                return
        
        for device in devices:
            service_name = f"mobile_app_{device}"
            try:
                await hass.services.async_call(
                    "notify",
                    service_name,
                    {
                        "title": title,
                        "message": message,
                        "data": data,
                    },
                    blocking=True,
                )
                _LOGGER.debug("Sent notification to %s", device)
            except Exception as err:
                _LOGGER.error("Failed to send notification to %s: %s", device, err)
        
        # Store in history
        history_entry = {
            "type": "notification_sent",
            "title": title,
            "message": message,
            "targets": devices,
            "category": category,
            "data": data,
            "timestamp": datetime.now().isoformat(),
        }
        config_data.setdefault("notification_history", []).append(history_entry)
        config_data["notification_history"] = config_data["notification_history"][-100:]
    
    # ========== SERVICE: send_notification ==========
    async def handle_send_notification(call: ServiceCall) -> None:
        """Handle send_notification service call."""
        data = _build_notification_data(
            priority=call.data.get(ATTR_PRIORITY, "normal"),
            category=call.data.get(ATTR_CATEGORY),
            tag=call.data.get(ATTR_TAG),
            extra_data=call.data.get(ATTR_DATA),
            group=call.data.get(ATTR_GROUP),
            channel=call.data.get(ATTR_CHANNEL),
            clickaction=call.data.get(ATTR_CLICKACTION),
        )
        
        await _send_to_devices(
            title=call.data[ATTR_TITLE],
            message=call.data[ATTR_MESSAGE],
            targets=call.data.get(ATTR_TARGET, []),
            data=data,
            category=call.data.get(ATTR_CATEGORY),
        )
    
    # ========== SERVICE: send_actionable ==========
    async def handle_send_actionable(call: ServiceCall) -> None:
        """Handle send_actionable service call - notification with buttons."""
        actions = call.data[ATTR_ACTIONS]
        
        data = _build_notification_data(
            priority=call.data.get(ATTR_PRIORITY, "high"),
            category=call.data.get(ATTR_CATEGORY),
            tag=call.data.get(ATTR_TAG),
            extra_data=call.data.get(ATTR_DATA),
            actions=actions,
            persistent=call.data.get(ATTR_PERSISTENT, True),
            sticky=call.data.get(ATTR_STICKY, True),
            timeout=call.data.get(ATTR_TIMEOUT),
            clickaction=call.data.get(ATTR_CLICKACTION),
            group=call.data.get(ATTR_GROUP),
        )
        
        await _send_to_devices(
            title=call.data[ATTR_TITLE],
            message=call.data[ATTR_MESSAGE],
            targets=call.data.get(ATTR_TARGET, []),
            data=data,
            category=call.data.get(ATTR_CATEGORY),
        )
    
    # ========== SERVICE: send_with_image ==========
    async def handle_send_with_image(call: ServiceCall) -> None:
        """Handle send_with_image service call - notification with image or camera snapshot."""
        data = _build_notification_data(
            priority=call.data.get(ATTR_PRIORITY, "normal"),
            category=call.data.get(ATTR_CATEGORY),
            tag=call.data.get(ATTR_TAG),
            extra_data=call.data.get(ATTR_DATA),
            actions=call.data.get(ATTR_ACTIONS),
            image=call.data.get(ATTR_IMAGE),
            camera_entity=call.data.get(ATTR_CAMERA),
        )
        
        await _send_to_devices(
            title=call.data[ATTR_TITLE],
            message=call.data[ATTR_MESSAGE],
            targets=call.data.get(ATTR_TARGET, []),
            data=data,
            category=call.data.get(ATTR_CATEGORY),
        )
    
    # ========== SERVICE: send_alarm_confirmation ==========
    async def handle_send_alarm_confirmation(call: ServiceCall) -> None:
        """Handle send_alarm_confirmation - preconfigured alarm notification with buttons."""
        template = call.data.get("template", "alarm_response")
        actions = ACTION_TEMPLATES.get(template, ACTION_TEMPLATES["alarm_response"])
        
        data = _build_notification_data(
            priority="critical",
            category="alarm",
            tag=call.data.get(ATTR_TAG, "alarm_confirmation"),
            extra_data=call.data.get(ATTR_DATA),
            actions=actions,
            persistent=True,
            sticky=True,
        )
        
        # Add alarm entity if specified
        alarm_entity = call.data.get("alarm_entity")
        if alarm_entity:
            data["entity_id"] = alarm_entity
            data["clickAction"] = f"entityId:{alarm_entity}"
        
        await _send_to_devices(
            title=call.data[ATTR_TITLE],
            message=call.data[ATTR_MESSAGE],
            targets=call.data.get(ATTR_TARGET, []),
            data=data,
            category="alarm",
        )
    
    # ========== SERVICE: send_text_input ==========
    async def handle_send_text_input(call: ServiceCall) -> None:
        """Handle send_text_input - notification with text reply option."""
        actions = [
            {
                "action": "REPLY",
                "title": call.data.get("input_title", "Antworten"),
                "behavior": "textInput",
                "textInputButtonTitle": "Senden",
                "textInputPlaceholder": call.data.get("placeholder", "Nachricht eingeben..."),
            }
        ]
        
        data = _build_notification_data(
            priority="normal",
            category=call.data.get(ATTR_CATEGORY, "info"),
            tag=call.data.get(ATTR_TAG),
            extra_data=call.data.get(ATTR_DATA),
            actions=actions,
            persistent=True,
        )
        
        await _send_to_devices(
            title=call.data[ATTR_TITLE],
            message=call.data[ATTR_MESSAGE],
            targets=call.data.get(ATTR_TARGET, []),
            data=data,
            category=call.data.get(ATTR_CATEGORY),
        )
    
    # ========== SERVICE: clear_notifications ==========
    async def handle_clear_notifications(call: ServiceCall) -> None:
        """Handle clear_notifications service call."""
        targets = call.data.get(ATTR_TARGET, [])
        tag = call.data.get(ATTR_TAG)
        
        config_data = hass.data[DOMAIN].get(entry.entry_id, {})
        devices = targets if targets else config_data.get("devices", [])
        
        for device in devices:
            service_name = f"mobile_app_{device}"
            try:
                clear_data = {}
                if tag:
                    clear_data["tag"] = tag
                
                await hass.services.async_call(
                    "notify",
                    service_name,
                    {
                        "message": "clear_notification",
                        "data": clear_data,
                    },
                    blocking=True,
                )
                _LOGGER.debug("Cleared notifications for %s", device)
            except Exception as err:
                _LOGGER.error("Failed to clear notifications for %s: %s", device, err)
    
    # Register all services
    hass.services.async_register(
        DOMAIN, SERVICE_SEND_NOTIFICATION, handle_send_notification, schema=SEND_NOTIFICATION_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_SEND_ACTIONABLE, handle_send_actionable, schema=SEND_ACTIONABLE_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_SEND_WITH_IMAGE, handle_send_with_image, schema=SEND_WITH_IMAGE_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_SEND_ALARM_CONFIRMATION, handle_send_alarm_confirmation, schema=SEND_ALARM_CONFIRMATION_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_SEND_TEXT_INPUT, handle_send_text_input, schema=SEND_TEXT_INPUT_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, SERVICE_CLEAR_NOTIFICATIONS, handle_clear_notifications, schema=CLEAR_NOTIFICATIONS_SCHEMA
    )


# ============================================================================
# UNLOAD / RELOAD
# ============================================================================

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
        
        if not hass.data[DOMAIN]:
            hass.services.async_remove(DOMAIN, SERVICE_SEND_NOTIFICATION)
            hass.services.async_remove(DOMAIN, SERVICE_SEND_ACTIONABLE)
            hass.services.async_remove(DOMAIN, SERVICE_SEND_WITH_IMAGE)
            hass.services.async_remove(DOMAIN, SERVICE_SEND_ALARM_CONFIRMATION)
            hass.services.async_remove(DOMAIN, SERVICE_SEND_TEXT_INPUT)
            hass.services.async_remove(DOMAIN, SERVICE_CLEAR_NOTIFICATIONS)
            await async_unregister_additional_services(hass)
    
    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
