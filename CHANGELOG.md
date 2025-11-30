# Changelog

All notable changes to Notify Manager will be documented in this file.

## [1.2.7.1] - 2025-11-30

### Changed
- **Frontend "Send" Tab**: "Save as Template" button now beside "Send Notification" button
- **Frontend "Templates" Tab**: Now uses same form layout as "Send" tab
  - Full notification editor for creating/editing templates
  - Shows saved templates list above editor
- **Simplified `send_from_template` Service**: Now only has template_name field
  - All other options (recipients, title, message) managed in Notify Manager Panel
  - No more mock data - only real user templates

### Fixed
- **Template Sync**: Select entity now auto-refreshes when templates are saved
- **Action IDs in Attributes**: Select entity now shows `available_action_ids` in state attributes
  - Helps debug which action IDs are available for automations

### Technical
- Added `notify_manager_templates_saved` event when templates are saved
- Select entity listens for template changes and refreshes options
- Version 1.2.7.1 across all files

---

## [1.2.7.0] - 2025-11-30

### Added
- **Device Type Management**: Set iOS or Android per device in frontend
  - Platform-specific notification options shown based on target devices
  - Stored in localStorage for persistence

- **ALL Companion App Notification Features** in Frontend:
  - Android: channel, color, ledColor, vibrationPattern, notificationIcon, iconUrl, sticky, persistent, alertOnce, timeout, visibility, carUi, chronometer, importance
  - iOS: sound, badge, interruptionLevel, critical, criticalVolume
  - Notification types: simple, buttons, image, media, tts (Android), map (iOS), progress (Android)
  - Dashboard dropdown for click actions (shows all Lovelace dashboards/views)

- **Dynamic Device Condition Actions**: Condition options now load from user-created templates
  - `async_get_condition_capabilities()` dynamically fetches action IDs from user templates
  - Shows action ID with template name label (e.g., "Test (Template Name)")
  - No more hardcoded options

### Changed
- **Simplified send_advanced Service**: Now only has Template, Device/Group, Title, Message
  - No more mock data or excessive options
  - Use templates for all advanced settings

### Technical
- Updated `device_condition.py` with `_get_user_templates()`, `_get_all_action_ids()`, `_get_all_template_names()`
- Complete frontend rewrite with platform detection via `_getTargetPlatforms()`
- Version 1.2.7.0 across all files

---

## [1.2.6.0] - 2025-11-30

### Changed
- **Simplified Device Page**: Device page now only shows Panel button and Sidebar toggle
  - Removed: Action templates, Button responses, Category switches
  - Cleaner device integration page with only essential controls

- **Removed Categories Tab**: Frontend panel reduced from 5 tabs to 4
  - Tabs: Send, Devices/Groups, Templates, Help
  - Categories were rarely used and added unnecessary complexity

- **Auto Language Detection**: Frontend automatically detects user's language
  - Supports German (DE) and English (EN)
  - Uses Home Assistant's language setting with browser fallback
  - All UI text now properly translated

- **Dashboard Dropdown**: "On click open" field improved
  - Shows all available Lovelace dashboards and their views
  - Organized with optgroups for better navigation
  - No more manual URL typing required

- **Simplified Device Conditions**: For automation conditions
  - Only shows user-created notification templates
  - Removed category-based switches from conditions
  - Tracks button responses by template for better automation logic

- **Groups Sync**: Real synchronization between frontend and backend
  - Groups created in panel are synced to HA services
  - Removed hardcoded mock groups from services.yaml
  - Dynamic group resolution in all notification services

### Technical
- Updated version strings to 1.2.6.0 across all files
- Cleaned up deprecated entity code
- Improved WebSocket communication for dashboard loading
- Added `_syncGroupsToHA()` method for real-time group synchronization

---

## [1.2.5.0] - 2025-11-29

### Added
- Device Conditions: Template filter for "Last Button Action"
- Groups in Services: Saved groups available in all notification services
- Buy me a coffee button in panel header

### Fixed
- Duplicate `async_setup_entry` in sensor.py
- Duplicate code in select.py

---

## [1.2.3.6] - Previous

### Added
- Template association for button responses
- New "Send to Group" service
- New "Last Template" select entity for conditions
- Persistent group storage in HA Storage

---

## [1.2.3.4] - Previous

### Changed
- Button Response select shows individual buttons as options

---

## [1.2.3.3] - Previous

### Added
- "Last Button" sensor
- Persistent template storage
- WebSocket API

---

## [1.2.3] - Previous

### Added
- Button editor with individual fields
- `send_from_template` service

---

## [1.2.0] - Previous

### Added
- Device Triggers, Conditions and Actions

---

## [1.1.0] - Previous

### Added
- 18 Services
- Frontend Panel
