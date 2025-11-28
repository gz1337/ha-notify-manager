# Notify Manager - Feature Checklist

Vollständige Unterstützung aller Home Assistant Companion App Features.

## ✅ = Implementiert

---

## notifications-basic (Grundlagen)

| Feature | Status | Service/Parameter |
|---------|--------|-------------------|
| title, message | ✅ | Alle Services |
| Grouping (group) | ✅ | `group` Parameter |
| Replacing (tag) | ✅ | `tag` Parameter |
| Clearing | ✅ | `clear_notifications` |
| Subtitle (iOS) | ✅ | `send_advanced` → `subtitle` |
| Subject (Android) | ✅ | `send_advanced` → `subject` |
| Color (Android) | ✅ | `send_advanced` → `color` |
| Sticky (Android) | ✅ | `sticky` Parameter |
| Notification Channels | ✅ | `channel` Parameter |
| Channel Importance | ✅ | `importance` Parameter |
| Vibration Pattern | ✅ | `send_advanced` → `vibration_pattern` |
| LED Color | ✅ | `send_advanced` → `led_color` |
| Persistent | ✅ | `persistent` Parameter |
| Timeout | ✅ | `timeout` Parameter |
| icon_url (Android) | ✅ | `send_advanced` → `icon_url` |
| visibility | ✅ | `send_advanced` → `visibility` |
| TTS | ✅ | `send_tts` Service |
| Chronometer | ✅ | `send_chronometer` Service |
| Progress Bar | ✅ | `send_progress` Service |
| alert_once | ✅ | `send_advanced` → `alert_once` |
| notification_icon | ✅ | `send_advanced` → `notification_icon` |
| car_ui (Android Auto) | ✅ | `send_advanced` → `car_ui` |
| Interruption Level (iOS) | ✅ | `interruption_level` |
| Presentation Options (iOS) | ✅ | `send_advanced` → `presentation_options` |
| Badge (iOS) | ✅ | `set_badge`, `clear_badge` |
| Sound (iOS) | ✅ | `sound` Parameter |
| URL/clickAction | ✅ | `click_action` Parameter |

---

## notification-attachments (Anhänge)

| Feature | Status | Service/Parameter |
|---------|--------|-------------------|
| image | ✅ | `image` Parameter |
| video | ✅ | `send_media` → `video` |
| audio | ✅ | `send_media` → `audio` |
| /api/camera_proxy | ✅ | `camera_entity` Parameter |
| media_source | ✅ | `/media/local/...` Pfade |
| attachment.hide-thumbnail | ✅ | `send_media` → `hide_thumbnail` |
| attachment.lazy | ✅ | `send_media` → `lazy` |

---

## dynamic-content (iOS)

| Feature | Status | Service/Parameter |
|---------|--------|-------------------|
| Map mit Pin | ✅ | `send_map` Service |
| Map Zoom Level | ✅ | `latitude_delta`, `longitude_delta` |
| Zweiter Pin | ✅ | `second_latitude`, `second_longitude` |
| Map Optionen | ✅ | `shows_compass`, `shows_traffic`, etc. |
| Camera Stream | ✅ | Via `camera_entity` |

---

## actionable-notifications

| Feature | Status |
|---------|--------|
| actions Array | ✅ |
| uri | ✅ |
| behavior: textInput | ✅ |
| icon (SF Symbols) | ✅ |
| destructive | ✅ |
| authenticationRequired | ✅ |
| action_data | ✅ |

---

## notification-commands (Android)

| Befehl | Status |
|--------|--------|
| command_dnd | ✅ |
| command_ringer_mode | ✅ |
| command_volume_level | ✅ |
| command_screen_on | ✅ |
| command_screen_brightness_level | ✅ |
| command_flashlight | ✅ |
| command_bluetooth | ✅ |
| command_high_accuracy_mode | ✅ |
| command_webview | ✅ |
| command_launch_app | ✅ |
| command_media | ✅ |
| command_update_sensors | ✅ |
| command_stop_tts | ✅ |
| command_broadcast_intent | ✅ |
| command_activity | ✅ |
| command_app_lock | ✅ |
| command_persistent_connection | ✅ |
| command_ble_transmitter | ✅ |
| command_beacon_monitor | ✅ |
| remove_channel | ✅ |
| request_location_update | ✅ |

---

## iOS Spezifisch

| Feature | Status | Service |
|---------|--------|---------|
| update_widgets | ✅ | `update_widgets` |
| update_complications | ✅ | `update_complications` |
| clear_badge | ✅ | `clear_badge` |
| set_badge | ✅ | `set_badge` |
| Critical Notifications | ✅ | `priority: critical` |
| Interruption Levels | ✅ | `interruption_level` |

---

## Verfügbare Services (18 total)

| Service | Beschreibung |
|---------|--------------|
| `send_notification` | Einfache Benachrichtigung |
| `send_actionable` | Mit Buttons |
| `send_with_image` | Mit Bild/Kamera |
| `send_alarm_confirmation` | Alarm-Vorlagen |
| `send_text_input` | Mit Texteingabe |
| `clear_notifications` | Löschen |
| `send_tts` | Text vorlesen (Android) |
| `send_map` | Karte mit Pin (iOS) |
| `send_media` | Video/Audio |
| `send_progress` | Fortschrittsbalken |
| `send_chronometer` | Timer/Countdown |
| `device_command` | Gerätesteuerung |
| `request_location_update` | Standort |
| `update_widgets` | iOS Widgets |
| `update_complications` | Apple Watch |
| `clear_badge` | Badge löschen |
| `set_badge` | Badge setzen |
| `send_advanced` | Alle Optionen |

---

## Zusammenfassung

**100% der Companion App Notification Features sind implementiert!**
