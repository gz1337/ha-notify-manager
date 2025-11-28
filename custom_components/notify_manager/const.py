"""Constants for Notify Manager integration.

Diese Konstanten unterstützen alle Features der Home Assistant Companion App:
- iOS und Android Benachrichtigungen
- Actionable Notifications
- Kritische Benachrichtigungen
- Kamera-Integration
- Text-Input Antworten
"""

DOMAIN = "notify_manager"

# Config keys
CONF_DEVICES = "devices"
CONF_CATEGORIES = "categories"
CONF_DEFAULT_PRIORITY = "default_priority"
CONF_ENABLE_HISTORY = "enable_history"
CONF_CALLBACK_AUTOMATIONS = "callback_automations"
CONF_SHOW_SIDEBAR = "show_sidebar"

# Service names
SERVICE_SEND_NOTIFICATION = "send_notification"
SERVICE_SEND_ACTIONABLE = "send_actionable"
SERVICE_CLEAR_NOTIFICATIONS = "clear_notifications"
SERVICE_SEND_ALARM_CONFIRMATION = "send_alarm_confirmation"
SERVICE_SEND_WITH_IMAGE = "send_with_image"
SERVICE_SEND_TEXT_INPUT = "send_text_input"
SERVICE_UPDATE_NOTIFICATION = "update_notification"
SERVICE_SEND_TTS = "send_tts"
SERVICE_SEND_MAP = "send_map"
SERVICE_SEND_VIDEO = "send_video"
SERVICE_DEVICE_COMMAND = "device_command"
SERVICE_REQUEST_LOCATION = "request_location_update"

# Attribute names - Basic
ATTR_TITLE = "title"
ATTR_MESSAGE = "message"
ATTR_TARGET = "target"
ATTR_CATEGORY = "category"
ATTR_PRIORITY = "priority"
ATTR_DATA = "data"
ATTR_ACTIONS = "actions"
ATTR_TAG = "tag"
ATTR_GROUP = "group"
ATTR_SUBTITLE = "subtitle"
ATTR_SUBJECT = "subject"

# Attribute names - Companion App specific
ATTR_IMAGE = "image"
ATTR_CAMERA = "camera_entity"
ATTR_VIDEO = "video"
ATTR_AUDIO = "audio"
ATTR_ICON = "icon_url"
ATTR_BADGE = "badge"
ATTR_CHANNEL = "channel"
ATTR_IMPORTANCE = "importance"
ATTR_VISIBILITY = "visibility"
ATTR_VIBRATION = "vibration_pattern"
ATTR_LED_COLOR = "led_color"
ATTR_PERSISTENT = "persistent"
ATTR_STICKY = "sticky"
ATTR_TIMEOUT = "timeout"
ATTR_CLICKACTION = "clickAction"
ATTR_URL = "url"
ATTR_ALERT_ONCE = "alert_once"
ATTR_NOTIFICATION_ICON = "notification_icon"
ATTR_CAR_UI = "car_ui"

# TTS specific
ATTR_TTS_TEXT = "tts_text"
ATTR_MEDIA_STREAM = "media_stream"

# Map specific (iOS)
ATTR_LATITUDE = "latitude"
ATTR_LONGITUDE = "longitude"
ATTR_SECOND_LATITUDE = "second_latitude"
ATTR_SECOND_LONGITUDE = "second_longitude"
ATTR_SHOWS_LINE = "shows_line_between_points"
ATTR_SHOWS_COMPASS = "shows_compass"
ATTR_SHOWS_TRAFFIC = "shows_traffic"
ATTR_SHOWS_SCALE = "shows_scale"

# Progress/Chronometer (Android)
ATTR_PROGRESS = "progress"
ATTR_PROGRESS_MAX = "progress_max"
ATTR_CHRONOMETER = "chronometer"
ATTR_WHEN = "when"

# Device commands
ATTR_COMMAND = "command"

# Attribute names - Actions
ATTR_ACTION = "action"
ATTR_ACTION_TITLE = "title"
ATTR_ACTION_URI = "uri"
ATTR_CALLBACK_ACTION = "callback_action"
ATTR_INPUT_TEXT = "input_text"
ATTR_REPLY_PLACEHOLDER = "reply_placeholder"

# iOS specific
ATTR_PUSH = "push"
ATTR_SOUND = "sound"
ATTR_CRITICAL = "critical"
ATTR_VOLUME = "volume"
ATTR_PRESENTATION_OPTIONS = "presentation_options"
ATTR_INTERRUPTION_LEVEL = "interruption-level"
ATTR_THREAD_ID = "thread-id"

# Android specific
ATTR_TTL = "ttl"
ATTR_COLOR = "color"
ATTR_NOTIFICATION_ICON = "notification_icon"
ATTR_CHRONOMETER = "chronometer"
ATTR_WHEN = "when"

# Event types - für mobile_app_notification_action
EVENT_NOTIFICATION_ACTION = "mobile_app_notification_action"
EVENT_NOTIFICATION_CLEARED = "mobile_app_notification_cleared"

# Default categories with Companion App optimized settings
DEFAULT_CATEGORIES = {
    "alarm": {
        "name": "Alarm",
        "name_en": "Alarm",
        "icon": "mdi:shield-alert",
        "enabled": True,
        "priority": "critical",
        "sound": "alarm.caf",
        "channel": "alarm",
        "color": "#F44336",
        "interruption_level": "critical",
    },
    "security": {
        "name": "Sicherheit",
        "name_en": "Security",
        "icon": "mdi:shield-home",
        "enabled": True,
        "priority": "high",
        "sound": "default",
        "channel": "security",
        "color": "#FF5722",
        "interruption_level": "time-sensitive",
    },
    "doorbell": {
        "name": "Türklingel",
        "name_en": "Doorbell",
        "icon": "mdi:doorbell",
        "enabled": True,
        "priority": "high",
        "sound": "doorbell.caf",
        "channel": "doorbell",
        "color": "#FF9800",
        "interruption_level": "time-sensitive",
    },
    "motion": {
        "name": "Bewegung",
        "name_en": "Motion",
        "icon": "mdi:motion-sensor",
        "enabled": True,
        "priority": "normal",
        "sound": "default",
        "channel": "motion",
        "color": "#2196F3",
        "interruption_level": "active",
    },
    "climate": {
        "name": "Klima",
        "name_en": "Climate",
        "icon": "mdi:thermostat",
        "enabled": True,
        "priority": "normal",
        "sound": "default",
        "channel": "climate",
        "color": "#00BCD4",
        "interruption_level": "active",
    },
    "system": {
        "name": "System",
        "name_en": "System",
        "icon": "mdi:cog",
        "enabled": True,
        "priority": "low",
        "sound": "none",
        "channel": "system",
        "color": "#9E9E9E",
        "interruption_level": "passive",
    },
    "info": {
        "name": "Information",
        "name_en": "Information",
        "icon": "mdi:information",
        "enabled": True,
        "priority": "low",
        "sound": "none",
        "channel": "info",
        "color": "#4CAF50",
        "interruption_level": "passive",
    },
}

# Priority levels mapping to Companion App settings
PRIORITY_LEVELS = {
    "low": {
        "importance": "low",
        "interruption_level": "passive",
        "priority": "low",
    },
    "normal": {
        "importance": "default",
        "interruption_level": "active",
        "priority": "default",
    },
    "high": {
        "importance": "high",
        "interruption_level": "time-sensitive",
        "priority": "high",
    },
    "critical": {
        "importance": "high",
        "interruption_level": "critical",
        "priority": "high",
        "critical": True,
    },
}

# Predefined action templates for common use cases
ACTION_TEMPLATES = {
    "confirm_dismiss": [
        {"action": "CONFIRM", "title": "✅ Bestätigen", "icon": "sfsymbols:checkmark.circle"},
        {"action": "DISMISS", "title": "❌ Ablehnen", "icon": "sfsymbols:xmark.circle"},
    ],
    "alarm_simple": [
        {"action": "ALARM_CONFIRM", "title": "✅ Alles OK", "icon": "sfsymbols:checkmark.shield"},
        {"action": "ALARM_EMERGENCY", "title": "🆘 Notfall!", "icon": "sfsymbols:exclamationmark.triangle", "destructive": True},
    ],
    "alarm_response": [
        {"action": "ALARM_CONFIRM", "title": "✅ Alles OK", "icon": "sfsymbols:checkmark.shield"},
        {"action": "ALARM_SNOOZE", "title": "⏰ Später", "icon": "sfsymbols:clock"},
        {"action": "ALARM_EMERGENCY", "title": "🆘 Notfall!", "icon": "sfsymbols:exclamationmark.triangle", "destructive": True},
    ],
    "door_response": [
        {"action": "DOOR_UNLOCK", "title": "🔓 Öffnen", "icon": "sfsymbols:lock.open"},
        {"action": "DOOR_IGNORE", "title": "🚪 Ignorieren", "icon": "sfsymbols:hand.raised"},
        {"action": "DOOR_SPEAK", "title": "🔊 Sprechen", "icon": "sfsymbols:speaker.wave.2"},
    ],
    "yes_no": [
        {"action": "YES", "title": "👍 Ja", "icon": "sfsymbols:hand.thumbsup"},
        {"action": "NO", "title": "👎 Nein", "icon": "sfsymbols:hand.thumbsdown"},
    ],
    "reply": [
        {"action": "REPLY", "title": "💬 Antworten", "icon": "sfsymbols:arrowshape.turn.up.left", "behavior": "textInput", "textInputButtonTitle": "Senden", "textInputPlaceholder": "Nachricht eingeben..."},
    ],
}

# Default notification templates (synced with frontend)
DEFAULT_NOTIFICATION_TEMPLATES = {
    "🚪 Türklingel": {
        "id": "doorbell",
        "name": "🚪 Türklingel",
        "title": "Türklingel",
        "message": "Jemand ist an der Tür!",
        "type": "image",
        "priority": "high",
        "buttons": [
            {"action": "DOOR_UNLOCK", "title": "🔓 Öffnen"},
            {"action": "DOOR_IGNORE", "title": "Ignorieren"},
        ],
    },
    "🚨 Alarm": {
        "id": "alarm",
        "name": "🚨 Alarm",
        "title": "Alarm!",
        "message": "Bewegung erkannt",
        "type": "buttons",
        "priority": "critical",
        "buttons": [
            {"action": "ALARM_CONFIRM", "title": "✅ OK"},
            {"action": "ALARM_EMERGENCY", "title": "🆘 Notfall"},
        ],
    },
    "⏰ Erinnerung": {
        "id": "reminder",
        "name": "⏰ Erinnerung",
        "title": "Erinnerung",
        "message": "",
        "type": "simple",
        "priority": "normal",
        "buttons": [],
    },
    "📦 Paket": {
        "id": "package",
        "name": "📦 Paket",
        "title": "Paket angekommen",
        "message": "Ein Paket wurde geliefert!",
        "type": "buttons",
        "priority": "normal",
        "buttons": [
            {"action": "CONFIRM", "title": "✅ Gesehen"},
        ],
    },
    "🔔 Standard": {
        "id": "default",
        "name": "🔔 Standard",
        "title": "Benachrichtigung",
        "message": "",
        "type": "simple",
        "priority": "normal",
        "buttons": [],
    },
}

# Sound options for iOS
IOS_SOUNDS = [
    "default",
    "none",
    "US-EN-Alexa-Motion-Detected-Generic.wav",
    "US-EN-Alexa-Motion-At-Back-Door.wav",
    "US-EN-Alexa-Motion-At-Front-Door.wav",
    "US-EN-Daisy-Back-Door-Motion.wav",
    "US-EN-Daisy-Front-Door-Motion.wav",
    "US-EN-Morgan-Freeman-Back-Door-Motion.wav",
    "US-EN-Morgan-Freeman-Front-Door-Motion.wav",
]

# Android notification channels (created automatically)
ANDROID_CHANNELS = {
    "alarm": {"name": "Alarm", "importance": "high", "vibration": True, "sound": True},
    "security": {"name": "Sicherheit", "importance": "high", "vibration": True, "sound": True},
    "doorbell": {"name": "Türklingel", "importance": "high", "vibration": True, "sound": True},
    "motion": {"name": "Bewegung", "importance": "default", "vibration": False, "sound": True},
    "climate": {"name": "Klima", "importance": "default", "vibration": False, "sound": False},
    "system": {"name": "System", "importance": "low", "vibration": False, "sound": False},
    "info": {"name": "Information", "importance": "low", "vibration": False, "sound": False},
}
