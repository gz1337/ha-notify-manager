"""Additional services for Notify Manager - Complete Companion App Feature Support.

This module implements ALL remaining Companion App notification features:
- TTS (Text-to-Speech)
- Maps with pins (iOS)
- Video/Audio attachments
- Device Commands (Android)
- Progress bars
- Chronometer/Timer
- Location requests
- iOS-specific: Badge, Widgets, Complications
- Android-specific: LED, Vibration, Screen control
"""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import (
    DOMAIN,
    CONF_DEVICES,
    ATTR_TITLE,
    ATTR_MESSAGE,
    ATTR_TARGET,
    ATTR_TAG,
    ATTR_DATA,
)

_LOGGER = logging.getLogger(__name__)


async def async_register_additional_services(hass: HomeAssistant, entry) -> None:
    """Register all additional Companion App services."""
    
    async def _send_to_devices(message: str, data: dict, targets: list[str] | None = None, title: str | None = None) -> None:
        """Send notification/command to specified devices."""
        config_data = hass.data[DOMAIN].get(entry.entry_id, {})
        devices = targets if targets else config_data.get("devices", [])
        
        for device in devices:
            service_name = f"mobile_app_{device}"
            try:
                payload = {"message": message, "data": data}
                if title:
                    payload["title"] = title
                await hass.services.async_call("notify", service_name, payload, blocking=True)
                _LOGGER.debug("Sent to %s: %s", device, message[:50])
            except Exception as err:
                _LOGGER.error("Failed to send to %s: %s", device, err)
    
    # =========================================================================
    # TEXT-TO-SPEECH (Android)
    # =========================================================================
    async def handle_send_tts(call: ServiceCall) -> None:
        """Send TTS notification - speaks text on Android device."""
        data = {
            "tts_text": call.data["tts_text"],
            "media_stream": call.data.get("media_stream", "music_stream"),
        }
        # Add any extra data
        if call.data.get(ATTR_DATA):
            data.update(call.data[ATTR_DATA])
        
        await _send_to_devices("TTS", data, call.data.get(ATTR_TARGET))
    
    hass.services.async_register(
        DOMAIN, "send_tts",
        handle_send_tts,
        schema=vol.Schema({
            vol.Required("tts_text"): cv.string,
            vol.Optional("media_stream", default="music_stream"): vol.In([
                "music_stream", "alarm_stream", "alarm_stream_max"
            ]),
            vol.Optional(ATTR_TARGET): vol.All(cv.ensure_list, [cv.string]),
            vol.Optional(ATTR_DATA): dict,
        })
    )
    
    # =========================================================================
    # MAP WITH PIN (iOS)
    # =========================================================================
    async def handle_send_map(call: ServiceCall) -> None:
        """Send notification with map and location pin (iOS)."""
        action_data = {
            "latitude": str(call.data["latitude"]),
            "longitude": str(call.data["longitude"]),
        }
        
        # Second pin
        if call.data.get("second_latitude"):
            action_data["second_latitude"] = str(call.data["second_latitude"])
            action_data["second_longitude"] = str(call.data.get("second_longitude", ""))
        
        # Map options
        for opt in ["shows_line_between_points", "shows_compass", "shows_traffic", 
                    "shows_scale", "shows_points_of_interest", "shows_user_location",
                    "latitude_delta", "longitude_delta"]:
            if call.data.get(opt) is not None:
                action_data[opt] = call.data[opt]
        
        data = {"action_data": action_data}
        if call.data.get(ATTR_TAG):
            data["tag"] = call.data[ATTR_TAG]
        
        await _send_to_devices(
            call.data[ATTR_MESSAGE], data, 
            call.data.get(ATTR_TARGET),
            call.data.get(ATTR_TITLE)
        )
    
    hass.services.async_register(
        DOMAIN, "send_map",
        handle_send_map,
        schema=vol.Schema({
            vol.Required(ATTR_MESSAGE): cv.string,
            vol.Required("latitude"): cv.string,
            vol.Required("longitude"): cv.string,
            vol.Optional(ATTR_TITLE): cv.string,
            vol.Optional(ATTR_TARGET): vol.All(cv.ensure_list, [cv.string]),
            vol.Optional("second_latitude"): cv.string,
            vol.Optional("second_longitude"): cv.string,
            vol.Optional("shows_line_between_points"): cv.boolean,
            vol.Optional("shows_compass"): cv.boolean,
            vol.Optional("shows_traffic"): cv.boolean,
            vol.Optional("shows_scale"): cv.boolean,
            vol.Optional("shows_points_of_interest"): cv.boolean,
            vol.Optional("shows_user_location"): cv.boolean,
            vol.Optional("latitude_delta"): cv.string,
            vol.Optional("longitude_delta"): cv.string,
            vol.Optional(ATTR_TAG): cv.string,
        })
    )
    
    # =========================================================================
    # VIDEO/AUDIO ATTACHMENT
    # =========================================================================
    async def handle_send_media(call: ServiceCall) -> None:
        """Send notification with video or audio attachment."""
        data = {}
        
        if call.data.get("video"):
            data["video"] = call.data["video"]
        if call.data.get("audio"):
            data["audio"] = call.data["audio"]
        if call.data.get("image"):
            data["image"] = call.data["image"]
        if call.data.get(ATTR_TAG):
            data["tag"] = call.data[ATTR_TAG]
        
        # Attachment options
        attachment = {}
        if call.data.get("hide_thumbnail"):
            attachment["hide-thumbnail"] = True
        if call.data.get("lazy"):
            attachment["lazy"] = True
        if call.data.get("content_type"):
            attachment["content-type"] = call.data["content_type"]
        if attachment:
            data["attachment"] = attachment
        
        await _send_to_devices(
            call.data[ATTR_MESSAGE], data,
            call.data.get(ATTR_TARGET),
            call.data.get(ATTR_TITLE)
        )
    
    hass.services.async_register(
        DOMAIN, "send_media",
        handle_send_media,
        schema=vol.Schema({
            vol.Required(ATTR_TITLE): cv.string,
            vol.Required(ATTR_MESSAGE): cv.string,
            vol.Optional("video"): cv.string,
            vol.Optional("audio"): cv.string,
            vol.Optional("image"): cv.string,
            vol.Optional("hide_thumbnail"): cv.boolean,
            vol.Optional("lazy"): cv.boolean,
            vol.Optional("content_type"): cv.string,
            vol.Optional(ATTR_TARGET): vol.All(cv.ensure_list, [cv.string]),
            vol.Optional(ATTR_TAG): cv.string,
        })
    )
    
    # =========================================================================
    # PROGRESS BAR (Android)
    # =========================================================================
    async def handle_send_progress(call: ServiceCall) -> None:
        """Send notification with progress bar (Android)."""
        data = {
            "tag": call.data[ATTR_TAG],
            "progress": call.data["progress"],
            "progress_max": call.data.get("progress_max", 100),
        }
        if call.data.get("progress_indeterminate"):
            data["progress_indeterminate"] = True
        
        await _send_to_devices(
            call.data[ATTR_MESSAGE], data,
            call.data.get(ATTR_TARGET),
            call.data.get(ATTR_TITLE)
        )
    
    hass.services.async_register(
        DOMAIN, "send_progress",
        handle_send_progress,
        schema=vol.Schema({
            vol.Required(ATTR_TITLE): cv.string,
            vol.Required(ATTR_MESSAGE): cv.string,
            vol.Required("progress"): vol.All(vol.Coerce(int), vol.Range(min=-1, max=100)),
            vol.Optional("progress_max", default=100): vol.Coerce(int),
            vol.Optional("progress_indeterminate"): cv.boolean,
            vol.Required(ATTR_TAG): cv.string,
            vol.Optional(ATTR_TARGET): vol.All(cv.ensure_list, [cv.string]),
        })
    )
    
    # =========================================================================
    # CHRONOMETER / TIMER (Android)
    # =========================================================================
    async def handle_send_chronometer(call: ServiceCall) -> None:
        """Send notification with chronometer/timer (Android)."""
        data = {
            "tag": call.data[ATTR_TAG],
            "chronometer": True,
            "when": call.data["when"],
            "when_relative": call.data.get("when_relative", True),
        }
        if call.data.get("timeout"):
            data["timeout"] = call.data["timeout"]
        
        await _send_to_devices(
            call.data[ATTR_MESSAGE], data,
            call.data.get(ATTR_TARGET),
            call.data.get(ATTR_TITLE)
        )
    
    hass.services.async_register(
        DOMAIN, "send_chronometer",
        handle_send_chronometer,
        schema=vol.Schema({
            vol.Required(ATTR_TITLE): cv.string,
            vol.Required(ATTR_MESSAGE): cv.string,
            vol.Required("when"): vol.Coerce(int),
            vol.Optional("when_relative", default=True): cv.boolean,
            vol.Optional("timeout"): vol.Coerce(int),
            vol.Required(ATTR_TAG): cv.string,
            vol.Optional(ATTR_TARGET): vol.All(cv.ensure_list, [cv.string]),
        })
    )
    
    # =========================================================================
    # DEVICE COMMANDS (Android)
    # =========================================================================
    async def handle_device_command(call: ServiceCall) -> None:
        """Send device command to Android device."""
        command = call.data["command"]
        data = call.data.get(ATTR_DATA, {})
        
        await _send_to_devices(command, data, call.data.get(ATTR_TARGET))
    
    DEVICE_COMMANDS = [
        "command_activity", "command_app_lock", "command_auto_screen_brightness",
        "command_bluetooth", "command_ble_transmitter", "command_beacon_monitor",
        "command_broadcast_intent", "command_dnd", "command_flashlight",
        "command_high_accuracy_mode", "command_launch_app", "command_media",
        "command_ringer_mode", "command_screen_brightness_level",
        "command_screen_off_timeout", "command_screen_on", "command_stop_tts",
        "command_persistent_connection", "command_update_sensors",
        "command_volume_level", "command_webview", "remove_channel",
    ]
    
    hass.services.async_register(
        DOMAIN, "device_command",
        handle_device_command,
        schema=vol.Schema({
            vol.Required("command"): vol.In(DEVICE_COMMANDS),
            vol.Optional(ATTR_TARGET): vol.All(cv.ensure_list, [cv.string]),
            vol.Optional(ATTR_DATA): dict,
        })
    )
    
    # =========================================================================
    # REQUEST LOCATION UPDATE
    # =========================================================================
    async def handle_request_location(call: ServiceCall) -> None:
        """Request location update from device."""
        await _send_to_devices("request_location_update", {}, call.data.get(ATTR_TARGET))
    
    hass.services.async_register(
        DOMAIN, "request_location_update",
        handle_request_location,
        schema=vol.Schema({
            vol.Optional(ATTR_TARGET): vol.All(cv.ensure_list, [cv.string]),
        })
    )
    
    # =========================================================================
    # UPDATE WIDGETS (iOS)
    # =========================================================================
    async def handle_update_widgets(call: ServiceCall) -> None:
        """Request widget update on iOS device."""
        await _send_to_devices("update_widgets", {}, call.data.get(ATTR_TARGET))
    
    hass.services.async_register(
        DOMAIN, "update_widgets",
        handle_update_widgets,
        schema=vol.Schema({
            vol.Optional(ATTR_TARGET): vol.All(cv.ensure_list, [cv.string]),
        })
    )
    
    # =========================================================================
    # UPDATE COMPLICATIONS (iOS - Apple Watch)
    # =========================================================================
    async def handle_update_complications(call: ServiceCall) -> None:
        """Request complication update on Apple Watch."""
        await _send_to_devices("update_complications", {}, call.data.get(ATTR_TARGET))
    
    hass.services.async_register(
        DOMAIN, "update_complications",
        handle_update_complications,
        schema=vol.Schema({
            vol.Optional(ATTR_TARGET): vol.All(cv.ensure_list, [cv.string]),
        })
    )
    
    # =========================================================================
    # CLEAR BADGE (iOS)
    # =========================================================================
    async def handle_clear_badge(call: ServiceCall) -> None:
        """Clear app badge on iOS device."""
        await _send_to_devices("clear_badge", {}, call.data.get(ATTR_TARGET))
    
    hass.services.async_register(
        DOMAIN, "clear_badge",
        handle_clear_badge,
        schema=vol.Schema({
            vol.Optional(ATTR_TARGET): vol.All(cv.ensure_list, [cv.string]),
        })
    )
    
    # =========================================================================
    # SET BADGE (iOS)
    # =========================================================================
    async def handle_set_badge(call: ServiceCall) -> None:
        """Set app badge number on iOS device."""
        data = {"push": {"badge": call.data["badge"]}}
        # Silent notification to just update badge
        await _send_to_devices("delete_alert", data, call.data.get(ATTR_TARGET))
    
    hass.services.async_register(
        DOMAIN, "set_badge",
        handle_set_badge,
        schema=vol.Schema({
            vol.Required("badge"): vol.Coerce(int),
            vol.Optional(ATTR_TARGET): vol.All(cv.ensure_list, [cv.string]),
        })
    )
    
    # =========================================================================
    # SEND WITH ALL OPTIONS (Advanced)
    # =========================================================================
    async def handle_send_advanced(call: ServiceCall) -> None:
        """Send notification with full control over all options."""
        data = {}
        
        # iOS push options
        push = {}
        if call.data.get("sound"):
            if call.data.get("critical"):
                push["sound"] = {"name": call.data["sound"], "critical": 1, "volume": call.data.get("volume", 1.0)}
            else:
                push["sound"] = call.data["sound"]
        if call.data.get("badge") is not None:
            push["badge"] = call.data["badge"]
        if call.data.get("interruption_level"):
            push["interruption-level"] = call.data["interruption_level"]
        if push:
            data["push"] = push
        
        # Presentation options (iOS)
        if call.data.get("presentation_options"):
            data["presentation_options"] = call.data["presentation_options"]
        
        # Thread/Group
        if call.data.get("group"):
            data["group"] = call.data["group"]
            data["thread-id"] = call.data["group"]
        
        # Subtitle (iOS) / Subject (Android)
        if call.data.get("subtitle"):
            data["subtitle"] = call.data["subtitle"]
        if call.data.get("subject"):
            data["subject"] = call.data["subject"]
        
        # Android channel options
        if call.data.get("channel"):
            data["channel"] = call.data["channel"]
        if call.data.get("importance"):
            data["importance"] = call.data["importance"]
        if call.data.get("vibration_pattern"):
            data["vibrationPattern"] = call.data["vibration_pattern"]
        if call.data.get("led_color"):
            data["ledColor"] = call.data["led_color"]
        if call.data.get("color"):
            data["color"] = call.data["color"]
        
        # Visibility
        if call.data.get("visibility"):
            data["visibility"] = call.data["visibility"]
        
        # Icon options
        if call.data.get("icon_url"):
            data["icon_url"] = call.data["icon_url"]
        if call.data.get("notification_icon"):
            data["notification_icon"] = call.data["notification_icon"]
        
        # Behavior options
        if call.data.get("tag"):
            data["tag"] = call.data["tag"]
        if call.data.get("sticky"):
            data["sticky"] = True
        if call.data.get("persistent"):
            data["persistent"] = True
        if call.data.get("alert_once"):
            data["alert_once"] = True
        if call.data.get("timeout"):
            data["timeout"] = call.data["timeout"]
        if call.data.get("car_ui"):
            data["car_ui"] = True
        
        # Click action
        if call.data.get("click_action"):
            data["clickAction"] = call.data["click_action"]
            data["url"] = call.data["click_action"]
        
        # Attachments
        if call.data.get("image"):
            data["image"] = call.data["image"]
        if call.data.get("video"):
            data["video"] = call.data["video"]
        if call.data.get("audio"):
            data["audio"] = call.data["audio"]
        if call.data.get("camera_entity"):
            data["entity_id"] = call.data["camera_entity"]
            data["image"] = f"/api/camera_proxy/{call.data['camera_entity']}"
        
        # Actions (buttons)
        if call.data.get("actions"):
            data["actions"] = call.data["actions"]
        
        # Action data
        if call.data.get("action_data"):
            data["action_data"] = call.data["action_data"]
        
        # Extra data merge
        if call.data.get(ATTR_DATA):
            data.update(call.data[ATTR_DATA])
        
        await _send_to_devices(
            call.data[ATTR_MESSAGE], data,
            call.data.get(ATTR_TARGET),
            call.data.get(ATTR_TITLE)
        )
    
    hass.services.async_register(
        DOMAIN, "send_advanced",
        handle_send_advanced,
        schema=vol.Schema({
            vol.Required(ATTR_TITLE): cv.string,
            vol.Required(ATTR_MESSAGE): cv.string,
            vol.Optional(ATTR_TARGET): vol.All(cv.ensure_list, [cv.string]),
            # iOS
            vol.Optional("sound"): cv.string,
            vol.Optional("critical"): cv.boolean,
            vol.Optional("volume"): vol.Coerce(float),
            vol.Optional("badge"): vol.Coerce(int),
            vol.Optional("interruption_level"): vol.In(["passive", "active", "time-sensitive", "critical"]),
            vol.Optional("presentation_options"): vol.All(cv.ensure_list, [cv.string]),
            vol.Optional("subtitle"): cv.string,
            # Android
            vol.Optional("subject"): cv.string,
            vol.Optional("channel"): cv.string,
            vol.Optional("importance"): vol.In(["min", "low", "default", "high", "max"]),
            vol.Optional("vibration_pattern"): cv.string,
            vol.Optional("led_color"): cv.string,
            vol.Optional("color"): cv.string,
            vol.Optional("icon_url"): cv.string,
            vol.Optional("notification_icon"): cv.string,
            vol.Optional("visibility"): vol.In(["public", "private", "secret"]),
            vol.Optional("car_ui"): cv.boolean,
            # Common
            vol.Optional("group"): cv.string,
            vol.Optional("tag"): cv.string,
            vol.Optional("sticky"): cv.boolean,
            vol.Optional("persistent"): cv.boolean,
            vol.Optional("alert_once"): cv.boolean,
            vol.Optional("timeout"): vol.Coerce(int),
            vol.Optional("click_action"): cv.string,
            # Attachments
            vol.Optional("image"): cv.string,
            vol.Optional("video"): cv.string,
            vol.Optional("audio"): cv.string,
            vol.Optional("camera_entity"): cv.string,
            # Actions
            vol.Optional("actions"): list,
            vol.Optional("action_data"): dict,
            vol.Optional(ATTR_DATA): dict,
        })
    )


async def async_unregister_additional_services(hass: HomeAssistant) -> None:
    """Unregister additional services."""
    services = [
        "send_tts", "send_map", "send_media", "send_progress", "send_chronometer",
        "device_command", "request_location_update", "update_widgets",
        "update_complications", "clear_badge", "set_badge", "send_advanced",
    ]
    for service in services:
        try:
            hass.services.async_remove(DOMAIN, service)
        except Exception:
            pass
