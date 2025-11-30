/**
 * Notify Manager Panel - Complete Notification Management
 * Version 1.2.7.1
 *
 * Features:
 * - ALL Home Assistant Companion App notification features
 * - Device type management (iOS/Android)
 * - Automatic language detection (DE/EN)
 * - Template and group management
 * - Dashboard/page selection for click actions
 */

import {
  LitElement,
  html,
  css,
} from "https://unpkg.com/lit-element@2.5.1/lit-element.js?module";

// Translations
const TRANSLATIONS = {
  en: {
    title: "Notify Manager",
    devices: "Devices",
    services: "Services",
    send: "Send",
    devicesGroups: "Devices & Groups",
    templates: "Templates",
    help: "Help",
    // Send tab
    quickNotification: "Quick Notification",
    useTemplate: "Use Template",
    recipients: "Recipients",
    allDevices: "All Devices",
    notificationType: "Notification Type",
    simple: "Simple",
    withButtons: "With Buttons",
    withCamera: "With Camera",
    withMedia: "With Media",
    tts: "TTS",
    map: "Map",
    progress: "Progress",
    title_field: "Title",
    subtitle: "Subtitle",
    message: "Message",
    textToRead: "Text to read",
    // Priority & Importance
    priority: "Priority",
    importance: "Importance",
    low: "Low",
    normal: "Normal",
    high: "High",
    critical: "Critical",
    min: "Min",
    max: "Max",
    default: "Default",
    // Camera & Media
    camera: "Camera",
    selectCamera: "-- Select Camera --",
    imageUrl: "Image URL",
    videoUrl: "Video URL",
    audioUrl: "Audio URL (iOS)",
    // Actions/Buttons
    buttonTemplate: "Button Template",
    none: "None",
    confirmReject: "Confirm/Reject",
    yesNo: "Yes/No",
    alarm: "Alarm",
    door: "Door",
    reply: "Reply",
    buttons: "Buttons",
    maxButtons: "Max 3 buttons on Android",
    actionId: "Action ID",
    buttonText: "Button Text",
    addButton: "+ Add Button",
    // Button options
    uri: "URI (optional)",
    destructive: "Destructive",
    authRequired: "Auth Required (iOS)",
    // Click Action
    clickAction: "On Click Open",
    selectDashboard: "-- Select Dashboard/View --",
    customUrl: "Or enter custom URL...",
    // Android Options
    androidOptions: "Android Options",
    channel: "Channel",
    color: "Color",
    ledColor: "LED Color",
    vibrationPattern: "Vibration Pattern",
    notificationIcon: "Icon (mdi:name)",
    iconUrl: "Icon URL",
    sticky: "Sticky",
    persistent: "Persistent",
    alertOnce: "Alert Once",
    timeout: "Timeout (seconds)",
    visibility: "Visibility",
    public: "Public",
    private: "Private",
    secret: "Secret",
    carUi: "Car UI",
    // iOS Options
    iosOptions: "iOS Options",
    sound: "Sound",
    badge: "Badge",
    interruptionLevel: "Interruption Level",
    passive: "Passive",
    active: "Active",
    timeSensitive: "Time Sensitive",
    criticalLevel: "Critical",
    // Progress
    progressValue: "Progress Value",
    progressMax: "Progress Max",
    indeterminate: "Indeterminate",
    // Chronometer
    chronometerValue: "Chronometer",
    countDown: "Count Down",
    // Map
    latitude: "Latitude",
    longitude: "Longitude",
    secondPinLat: "2nd Pin Latitude",
    secondPinLng: "2nd Pin Longitude",
    showCompass: "Show Compass",
    showTraffic: "Show Traffic",
    showScale: "Show Scale",
    // Critical
    criticalAlert: "Critical Alert (iOS)",
    criticalVolume: "Critical Volume",
    // Attachment Options
    attachmentOptions: "Attachment Options",
    hideThumbnail: "Hide Thumbnail",
    lazyLoad: "Lazy Load (iOS)",
    contentType: "Content Type",
    // Group & Tag
    grouping: "Grouping",
    group: "Group",
    tag: "Tag",
    // Preview & Actions
    preview: "Preview",
    saveAsTemplate: "Save as Template",
    sendNotification: "Send Notification",
    sending: "Sending...",
    sent: "Notification sent!",
    error: "Error",
    // Devices tab
    statistics: "Statistics",
    groups: "Groups",
    deviceGroups: "Device Groups",
    newGroup: "+ New Group",
    clickToAddRemove: "Click on a group to add/remove devices.",
    noGroups: "No groups created yet.",
    connectedDevices: "Connected Devices",
    deviceType: "Device Type",
    ios: "iOS",
    android: "Android",
    setDeviceType: "Set device type to enable platform-specific options",
    clickDevicesFor: "Click devices for",
    inGroup: "in group",
    clickToToggle: "Click to add/remove",
    selectGroupAbove: "Select a group above to add/remove devices.",
    noDevices: "No Companion App devices found.",
    rename: "Rename",
    // Templates tab
    manageTemplates: "Manage Templates",
    createTemplate: "Create Template",
    editTemplate: "Edit Template",
    newTemplate: "+ New Template",
    type: "Type",
    use: "Use",
    noTemplates: "No custom templates created yet.",
    createFirst: "Create first template",
    savedTemplates: "Saved Templates",
    templateEditor: "Template Editor",
    // Help tab
    helpTitle: "Help & Documentation",
    quickStart: "Quick Start",
    quickStartText: "1. Set device types in Devices tab\n2. Create groups for easy targeting\n3. Send notifications or create templates",
    iosFeatures: "iOS Features",
    iosFeaturesText: "Critical alerts, badges, sounds, interruption levels, Apple Watch complications",
    androidFeatures: "Android Features",
    androidFeaturesText: "Channels, LED colors, vibration patterns, TTS, progress bars, chronometer, persistent notifications",
    buttonReaction: "React to Buttons",
    availableServices: "Available Services",
    // Modals
    newTemplateTitle: "New Template",
    templateName: "Template Name",
    cancel: "Cancel",
    save: "Save",
    editGroup: "Edit Group",
    newGroupTitle: "New Group",
    groupName: "Group Name",
    selectDevices: "Select devices",
    selectAtLeastOne: "Please select at least one device",
    enterName: "Please enter a name",
    deleteConfirm: "Really delete?",
    templateSaved: "Template saved!",
    showAdvanced: "Show Advanced Options",
    hideAdvanced: "Hide Advanced Options",
    reset: "Reset",
  },
  de: {
    title: "Notify Manager",
    devices: "Geräte",
    services: "Services",
    send: "Senden",
    devicesGroups: "Geräte & Gruppen",
    templates: "Vorlagen",
    help: "Hilfe",
    quickNotification: "Schnell-Benachrichtigung",
    useTemplate: "Vorlage verwenden",
    recipients: "Empfänger",
    allDevices: "Alle Geräte",
    notificationType: "Benachrichtigungstyp",
    simple: "Einfach",
    withButtons: "Mit Buttons",
    withCamera: "Mit Kamera",
    withMedia: "Mit Medien",
    tts: "TTS",
    map: "Karte",
    progress: "Fortschritt",
    title_field: "Titel",
    subtitle: "Untertitel",
    message: "Nachricht",
    textToRead: "Text zum Vorlesen",
    priority: "Priorität",
    importance: "Wichtigkeit",
    low: "Niedrig",
    normal: "Normal",
    high: "Hoch",
    critical: "Kritisch",
    min: "Min",
    max: "Max",
    default: "Standard",
    camera: "Kamera",
    selectCamera: "-- Kamera wählen --",
    imageUrl: "Bild-URL",
    videoUrl: "Video-URL",
    audioUrl: "Audio-URL (iOS)",
    buttonTemplate: "Button-Vorlage",
    none: "Keine",
    confirmReject: "Bestätigen/Ablehnen",
    yesNo: "Ja/Nein",
    alarm: "Alarm",
    door: "Tür",
    reply: "Antwort",
    buttons: "Buttons",
    maxButtons: "Max 3 Buttons auf Android",
    actionId: "Action ID",
    buttonText: "Button Text",
    addButton: "+ Button hinzufügen",
    uri: "URI (optional)",
    destructive: "Destruktiv",
    authRequired: "Auth erforderlich (iOS)",
    clickAction: "Bei Klick öffnen",
    selectDashboard: "-- Dashboard/View wählen --",
    customUrl: "Oder eigene URL eingeben...",
    androidOptions: "Android Optionen",
    channel: "Kanal",
    color: "Farbe",
    ledColor: "LED Farbe",
    vibrationPattern: "Vibrationsmuster",
    notificationIcon: "Icon (mdi:name)",
    iconUrl: "Icon URL",
    sticky: "Sticky",
    persistent: "Persistent",
    alertOnce: "Nur einmal Ton",
    timeout: "Timeout (Sekunden)",
    visibility: "Sichtbarkeit",
    public: "Öffentlich",
    private: "Privat",
    secret: "Geheim",
    carUi: "Auto UI",
    iosOptions: "iOS Optionen",
    sound: "Ton",
    badge: "Badge",
    interruptionLevel: "Unterbrechungslevel",
    passive: "Passiv",
    active: "Aktiv",
    timeSensitive: "Zeitkritisch",
    criticalLevel: "Kritisch",
    progressValue: "Fortschrittswert",
    progressMax: "Fortschritt Max",
    indeterminate: "Unbestimmt",
    chronometerValue: "Chronometer",
    countDown: "Countdown",
    latitude: "Breitengrad",
    longitude: "Längengrad",
    secondPinLat: "2. Pin Breitengrad",
    secondPinLng: "2. Pin Längengrad",
    showCompass: "Kompass zeigen",
    showTraffic: "Verkehr zeigen",
    showScale: "Skala zeigen",
    criticalAlert: "Kritischer Alarm (iOS)",
    criticalVolume: "Kritische Lautstärke",
    attachmentOptions: "Anhang-Optionen",
    hideThumbnail: "Vorschau ausblenden",
    lazyLoad: "Lazy Load (iOS)",
    contentType: "Content-Type",
    grouping: "Gruppierung",
    group: "Gruppe",
    tag: "Tag",
    preview: "Vorschau",
    saveAsTemplate: "Als Vorlage speichern",
    sendNotification: "Benachrichtigung senden",
    sending: "Sende...",
    sent: "Benachrichtigung gesendet!",
    error: "Fehler",
    statistics: "Statistiken",
    groups: "Gruppen",
    deviceGroups: "Gerätegruppen",
    newGroup: "+ Neue Gruppe",
    clickToAddRemove: "Klicke auf eine Gruppe, um Geräte hinzuzufügen.",
    noGroups: "Noch keine Gruppen erstellt.",
    connectedDevices: "Verbundene Geräte",
    deviceType: "Gerätetyp",
    ios: "iOS",
    android: "Android",
    setDeviceType: "Gerätetyp setzen für plattformspezifische Optionen",
    clickDevicesFor: "Klicke Geräte für",
    inGroup: "in Gruppe",
    clickToToggle: "Klicke zum Hinzufügen/Entfernen",
    selectGroupAbove: "Wähle oben eine Gruppe aus.",
    noDevices: "Keine Companion App Geräte gefunden.",
    rename: "Umbenennen",
    manageTemplates: "Vorlagen verwalten",
    createTemplate: "Vorlage erstellen",
    editTemplate: "Vorlage bearbeiten",
    newTemplate: "+ Neue Vorlage",
    type: "Typ",
    use: "Verwenden",
    noTemplates: "Noch keine Vorlagen erstellt.",
    createFirst: "Erste Vorlage erstellen",
    savedTemplates: "Gespeicherte Vorlagen",
    templateEditor: "Vorlagen-Editor",
    helpTitle: "Hilfe & Dokumentation",
    quickStart: "Schnellstart",
    quickStartText: "1. Gerätetypen im Geräte-Tab setzen\n2. Gruppen erstellen\n3. Benachrichtigungen senden oder Vorlagen erstellen",
    iosFeatures: "iOS Features",
    iosFeaturesText: "Kritische Alarme, Badges, Töne, Unterbrechungslevel, Apple Watch",
    androidFeatures: "Android Features",
    androidFeaturesText: "Kanäle, LED-Farben, Vibrationsmuster, TTS, Fortschrittsbalken, Chronometer",
    buttonReaction: "Auf Buttons reagieren",
    availableServices: "Verfügbare Services",
    newTemplateTitle: "Neue Vorlage",
    templateName: "Vorlagen-Name",
    cancel: "Abbrechen",
    save: "Speichern",
    editGroup: "Gruppe bearbeiten",
    newGroupTitle: "Neue Gruppe",
    groupName: "Gruppen-Name",
    selectDevices: "Geräte auswählen",
    selectAtLeastOne: "Mindestens ein Gerät auswählen",
    enterName: "Bitte Namen eingeben",
    deleteConfirm: "Wirklich löschen?",
    templateSaved: "Vorlage gespeichert!",
    showAdvanced: "Erweiterte Optionen zeigen",
    hideAdvanced: "Erweiterte Optionen ausblenden",
    reset: "Zurücksetzen",
  }
};

class NotifyManagerPanel extends LitElement {
  static get properties() {
    return {
      hass: { type: Object },
      narrow: { type: Boolean },
      _tab: { type: String },
      _loading: { type: Boolean },
      _success: { type: String },
      _lang: { type: String },
      _showAdvanced: { type: Boolean },
      // Form state
      _title: { type: String },
      _subtitle: { type: String },
      _message: { type: String },
      _type: { type: String },
      _priority: { type: String },
      _buttons: { type: Array },
      _selectedDevices: { type: Array },
      _selectedGroup: { type: String },
      // Media
      _camera: { type: String },
      _imageUrl: { type: String },
      _videoUrl: { type: String },
      _audioUrl: { type: String },
      // Click action
      _clickAction: { type: String },
      // Android options
      _channel: { type: String },
      _color: { type: String },
      _ledColor: { type: String },
      _vibrationPattern: { type: String },
      _notificationIcon: { type: String },
      _iconUrl: { type: String },
      _sticky: { type: Boolean },
      _persistent: { type: Boolean },
      _alertOnce: { type: Boolean },
      _timeout: { type: Number },
      _visibility: { type: String },
      _carUi: { type: Boolean },
      _importance: { type: String },
      // iOS options
      _sound: { type: String },
      _badge: { type: Number },
      _interruptionLevel: { type: String },
      _critical: { type: Boolean },
      _criticalVolume: { type: Number },
      // Progress
      _progress: { type: Number },
      _progressMax: { type: Number },
      _progressIndeterminate: { type: Boolean },
      // Chronometer
      _chronometer: { type: Boolean },
      _chronometerCountDown: { type: Boolean },
      // Map
      _latitude: { type: String },
      _longitude: { type: String },
      _secondPinLat: { type: String },
      _secondPinLng: { type: String },
      // TTS
      _ttsText: { type: String },
      _mediaStream: { type: String },
      // Group & Tag
      _group: { type: String },
      _tag: { type: String },
      // Attachment options
      _hideThumbnail: { type: Boolean },
      _lazyLoad: { type: Boolean },
      _contentType: { type: String },
      // Data
      _templates: { type: Array },
      _groups: { type: Array },
      _deviceTypes: { type: Object },
      _dashboards: { type: Array },
      // Edit mode
      _editingTemplate: { type: Object },
      _editingGroup: { type: Object },
      _activeGroupId: { type: String },
      // Template tab state
      _templateEditMode: { type: Boolean },
      _templateFormId: { type: String },
      _templateFormName: { type: String },
    };
  }

  constructor() {
    super();
    this._tab = "send";
    this._loading = false;
    this._success = "";
    this._lang = "en";
    this._showAdvanced = false;
    // Reset form
    this._resetForm();
    // Data
    this._templates = [];
    this._groups = [];
    this._deviceTypes = {}; // { device_name: 'ios' | 'android' }
    this._dashboards = [];
    this._editingTemplate = null;
    this._editingGroup = null;
    this._activeGroupId = null;
    this._templatesLoaded = false;
    // Template editor
    this._templateEditMode = false;
    this._templateFormId = '';
    this._templateFormName = '';
  }

  _resetForm() {
    this._title = "";
    this._subtitle = "";
    this._message = "";
    this._type = "simple";
    this._priority = "normal";
    this._buttons = [];
    this._selectedDevices = [];
    this._selectedGroup = "";
    this._camera = "";
    this._imageUrl = "";
    this._videoUrl = "";
    this._audioUrl = "";
    this._clickAction = "";
    this._channel = "";
    this._color = "";
    this._ledColor = "";
    this._vibrationPattern = "";
    this._notificationIcon = "";
    this._iconUrl = "";
    this._sticky = false;
    this._persistent = false;
    this._alertOnce = false;
    this._timeout = 0;
    this._visibility = "public";
    this._carUi = false;
    this._importance = "default";
    this._sound = "";
    this._badge = 0;
    this._interruptionLevel = "active";
    this._critical = false;
    this._criticalVolume = 1.0;
    this._progress = 0;
    this._progressMax = 100;
    this._progressIndeterminate = false;
    this._chronometer = false;
    this._chronometerCountDown = false;
    this._latitude = "";
    this._longitude = "";
    this._secondPinLat = "";
    this._secondPinLng = "";
    this._ttsText = "";
    this._mediaStream = "music_stream";
    this._group = "";
    this._tag = "";
    this._hideThumbnail = false;
    this._lazyLoad = false;
    this._contentType = "";
    // Template editor
    this._templateFormId = '';
    this._templateFormName = '';
  }

  t(key) {
    return TRANSLATIONS[this._lang]?.[key] || TRANSLATIONS.en[key] || key;
  }

  async connectedCallback() {
    super.connectedCallback();
    this._detectLanguage();
    await this._loadData();
    await this._loadDashboards();
  }

  _detectLanguage() {
    const haLang = this.hass?.language || navigator.language || "en";
    this._lang = haLang.startsWith("de") ? "de" : "en";
  }

  async _loadData() {
    if (!this.hass || this._templatesLoaded) return;

    try {
      // Load templates from HA
      const response = await this.hass.callWS({ type: "notify_manager/get_templates" });
      if (response?.templates?.length) {
        this._templates = response.templates;
        this._templatesLoaded = true;
      }
    } catch (e) {
      // Fallback to localStorage
      const stored = localStorage.getItem("notify_manager_templates");
      if (stored) {
        try { this._templates = JSON.parse(stored); } catch {}
      }
    }

    // Load groups from localStorage
    try {
      const storedGroups = localStorage.getItem("notify_manager_groups");
      if (storedGroups) {
        this._groups = JSON.parse(storedGroups);
        await this._syncGroupsToHA();
      }
    } catch {}

    // Load device types from localStorage
    try {
      const storedTypes = localStorage.getItem("notify_manager_device_types");
      if (storedTypes) {
        this._deviceTypes = JSON.parse(storedTypes);
      }
    } catch {}
  }

  async _loadDashboards() {
    if (!this.hass) return;
    try {
      const dashboards = await this.hass.callWS({ type: "lovelace/dashboards" });
      this._dashboards = dashboards || [];
      for (const dashboard of this._dashboards) {
        try {
          const config = await this.hass.callWS({
            type: "lovelace/config",
            url_path: dashboard.url_path || null
          });
          dashboard.views = config?.views || [];
        } catch { dashboard.views = []; }
      }
    } catch { this._dashboards = []; }
  }

  _saveToStorage(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      if (key === "notify_manager_templates") this._syncTemplatesToHA();
      else if (key === "notify_manager_groups") this._syncGroupsToHA();
    } catch (e) { console.error("Storage error:", e); }
  }

  async _syncTemplatesToHA() {
    if (this.hass && this._templates) {
      try {
        await this.hass.callService("notify_manager", "save_templates", { templates: this._templates });
      } catch {}
    }
  }

  async _syncGroupsToHA() {
    if (this.hass && this._groups) {
      try {
        await this.hass.callService("notify_manager", "save_groups", { groups: this._groups });
      } catch {}
    }
  }

  _setDeviceType(device, type) {
    this._deviceTypes = { ...this._deviceTypes, [device]: type };
    this._saveToStorage("notify_manager_device_types", this._deviceTypes);
  }

  _getDeviceType(device) {
    // Check stored type first
    if (this._deviceTypes[device]) return this._deviceTypes[device];
    // Auto-detect from name
    const lower = device.toLowerCase();
    if (lower.includes('iphone') || lower.includes('ipad') || lower.includes('mac')) return 'ios';
    if (lower.includes('pixel') || lower.includes('samsung') || lower.includes('android')) return 'android';
    return null;
  }

  _getTargetPlatforms() {
    // Determine which platforms are targeted
    let targets = [];
    if (this._selectedGroup) {
      const group = this._groups.find(g => g.id === this._selectedGroup);
      if (group) targets = group.devices || [];
    } else if (this._selectedDevices.length) {
      targets = this._selectedDevices;
    } else {
      targets = this._getDevices();
    }

    const platforms = new Set();
    for (const device of targets) {
      const type = this._getDeviceType(device);
      if (type) platforms.add(type);
      else { platforms.add('ios'); platforms.add('android'); } // Unknown = show both
    }
    return platforms;
  }

  static get styles() {
    return css`
      :host {
        display: block;
        padding: 16px;
        max-width: 1200px;
        margin: 0 auto;
        --accent: var(--primary-color, #03a9f4);
        --card-bg: var(--ha-card-background, var(--card-background-color, #fff));
        --text: var(--primary-text-color, #212121);
        --text2: var(--secondary-text-color, #727272);
        --border: var(--divider-color, #e0e0e0);
        --success: #4caf50;
        --error: #f44336;
        --ios-color: #007aff;
        --android-color: #3ddc84;
      }

      .header {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 20px;
        padding: 16px;
        background: linear-gradient(135deg, var(--accent), #0288d1);
        border-radius: 16px;
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        flex-wrap: wrap;
      }
      .header-logo { width: 64px; height: 64px; border-radius: 12px; background: white; padding: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.2); }
      .header-title { font-size: 26px; font-weight: 600; margin: 0 0 4px 0; }
      .header-version { font-size: 13px; opacity: 0.9; }
      .header-spacer { flex: 1; }
      .bmc-button { display: flex; align-items: center; text-decoration: none; transition: transform 0.2s; }
      .bmc-button:hover { transform: scale(1.05); }
      .bmc-button img { border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.2); }

      .tabs { display: flex; gap: 4px; margin-bottom: 16px; border-bottom: 1px solid var(--border); padding-bottom: 8px; flex-wrap: wrap; }
      .tab { padding: 10px 16px; background: none; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; font-weight: 500; color: var(--text2); transition: all 0.2s; }
      .tab:hover { background: rgba(0,0,0,0.05); color: var(--text); }
      .tab.active { background: var(--accent); color: white; }

      .card { background: var(--card-bg); border-radius: 12px; padding: 20px; box-shadow: var(--ha-card-box-shadow, 0 2px 8px rgba(0,0,0,0.1)); margin-bottom: 16px; }
      .card-title { font-size: 16px; font-weight: 600; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; justify-content: space-between; color: var(--text); flex-wrap: wrap; }

      .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; margin-bottom: 16px; }
      .stat-card { background: linear-gradient(135deg, rgba(3,169,244,0.1), rgba(3,169,244,0.05)); border-radius: 12px; padding: 16px; text-align: center; border: 1px solid rgba(3,169,244,0.2); }
      .stat-value { font-size: 28px; font-weight: 700; color: var(--accent); }
      .stat-label { font-size: 11px; color: var(--text2); margin-top: 4px; }

      .form-group { margin-bottom: 14px; }
      .form-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; }
      label { display: block; font-size: 12px; font-weight: 500; color: var(--text2); margin-bottom: 5px; }
      input, textarea, select { width: 100%; padding: 9px 11px; border: 1px solid var(--border); border-radius: 8px; font-size: 13px; background: var(--card-bg); color: var(--text); box-sizing: border-box; font-family: inherit; }
      input:focus, textarea:focus, select:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 2px rgba(3,169,244,0.2); }
      textarea { resize: vertical; min-height: 70px; }
      input[type="checkbox"] { width: auto; margin-right: 6px; }
      input[type="color"] { padding: 2px; height: 36px; }
      input[type="number"] { width: 100px; }

      .checkbox-row { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; margin: 8px 0; }
      .checkbox-item { display: flex; align-items: center; font-size: 13px; color: var(--text); }

      .type-selector, .device-selector { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 6px; }
      .type-btn, .device-chip { padding: 9px 13px; border: 2px solid var(--border); border-radius: 10px; background: var(--card-bg); cursor: pointer; font-size: 12px; font-weight: 500; color: var(--text); transition: all 0.2s; display: flex; align-items: center; gap: 5px; }
      .type-btn:hover, .device-chip:hover { border-color: var(--accent); }
      .type-btn.active, .device-chip.selected { border-color: var(--accent); background: var(--accent); color: white; }
      .device-chip.group { border-style: dashed; }
      .device-chip.group.selected { border-style: solid; }
      .device-chip .type-badge { font-size: 9px; padding: 2px 5px; border-radius: 4px; margin-left: 4px; }
      .device-chip .type-badge.ios { background: var(--ios-color); color: white; }
      .device-chip .type-badge.android { background: var(--android-color); color: white; }

      .section-toggle { background: none; border: 1px solid var(--border); padding: 8px 14px; border-radius: 8px; cursor: pointer; font-size: 12px; color: var(--text2); margin-bottom: 12px; }
      .section-toggle:hover { border-color: var(--accent); color: var(--accent); }

      .platform-section { background: rgba(0,0,0,0.02); border-radius: 10px; padding: 14px; margin-bottom: 12px; border: 1px solid var(--border); }
      .platform-section.ios { border-left: 3px solid var(--ios-color); }
      .platform-section.android { border-left: 3px solid var(--android-color); }
      .platform-section h4 { margin: 0 0 10px 0; font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 6px; }
      .platform-section h4 .badge { font-size: 10px; padding: 2px 6px; border-radius: 4px; color: white; }
      .platform-section h4 .badge.ios { background: var(--ios-color); }
      .platform-section h4 .badge.android { background: var(--android-color); }

      .button-list { display: flex; flex-direction: column; gap: 8px; }
      .button-item { display: grid; grid-template-columns: 1fr 1fr 1fr auto; gap: 8px; align-items: center; background: rgba(0,0,0,0.02); padding: 10px; border-radius: 8px; }
      .button-item.compact { grid-template-columns: 1fr 1fr auto; }
      @media (max-width: 600px) { .button-item { grid-template-columns: 1fr; } }
      .button-options { display: flex; gap: 10px; flex-wrap: wrap; font-size: 11px; margin-top: 6px; }

      .btn { padding: 8px 14px; border: none; border-radius: 8px; cursor: pointer; font-size: 13px; font-weight: 500; transition: all 0.2s; display: inline-flex; align-items: center; gap: 5px; }
      .btn:hover { opacity: 0.85; transform: translateY(-1px); }
      .btn-primary { background: var(--accent); color: white; }
      .btn-success { background: var(--success); color: white; }
      .btn-danger { background: var(--error); color: white; }
      .btn-outline { background: transparent; border: 1px solid var(--border); color: var(--text); }
      .btn-small { padding: 5px 10px; font-size: 11px; }
      .btn-icon { width: 32px; height: 32px; padding: 0; justify-content: center; border-radius: 50%; }

      .action-buttons { display: flex; gap: 10px; margin-top: 14px; flex-wrap: wrap; }
      .send-btn { flex: 1; min-width: 200px; padding: 14px; background: linear-gradient(135deg, var(--accent), #0288d1); color: white; border: none; border-radius: 10px; font-size: 15px; font-weight: 600; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; gap: 8px; box-shadow: 0 4px 12px rgba(3,169,244,0.3); }
      .send-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(3,169,244,0.4); }
      .send-btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; box-shadow: none; }
      .save-template-btn { flex: 1; min-width: 200px; padding: 14px; background: linear-gradient(135deg, var(--success), #388e3c); color: white; border: none; border-radius: 10px; font-size: 15px; font-weight: 600; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; gap: 8px; box-shadow: 0 4px 12px rgba(76,175,80,0.3); }
      .save-template-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(76,175,80,0.4); }

      .success-msg { background: rgba(76,175,80,0.1); color: var(--success); padding: 12px; border-radius: 8px; margin-top: 12px; text-align: center; font-weight: 500; }
      .error-msg { background: rgba(244,67,54,0.1); color: var(--error); padding: 12px; border-radius: 8px; margin-top: 12px; text-align: center; font-weight: 500; }

      .preview { background: #1a1a1a; border-radius: 12px; padding: 14px; color: white; margin-top: 14px; }
      .preview-title { font-size: 11px; color: #888; margin-bottom: 8px; }
      .preview-notification { background: #2d2d2d; border-radius: 10px; padding: 12px; }
      .preview-header { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
      .preview-icon { width: 18px; height: 18px; background: var(--accent); border-radius: 4px; }
      .preview-app { font-size: 10px; color: #888; }
      .preview-t { font-weight: 600; font-size: 13px; }
      .preview-m { font-size: 12px; color: #ccc; margin-top: 4px; }
      .preview-buttons { display: flex; gap: 6px; margin-top: 10px; padding-top: 10px; border-top: 1px solid #444; }
      .preview-btn { flex: 1; padding: 7px; background: #444; border-radius: 6px; text-align: center; font-size: 11px; color: white; }

      .template-grid, .group-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; }
      .template-card, .group-card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 10px; padding: 14px; cursor: pointer; transition: all 0.2s; }
      .template-card:hover, .group-card:hover { border-color: var(--accent); box-shadow: 0 4px 12px rgba(0,0,0,0.1); transform: translateY(-2px); }
      .group-card.active-group { border-color: var(--accent); background: linear-gradient(135deg, rgba(3,169,244,0.15), rgba(3,169,244,0.05)); box-shadow: 0 0 0 2px var(--accent); }
      .template-name, .group-name { font-weight: 600; font-size: 14px; margin-bottom: 4px; }
      .template-preview, .group-info { font-size: 11px; color: var(--text2); }
      .template-actions, .group-actions { display: flex; gap: 6px; margin-top: 8px; }

      .device-card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 10px; padding: 12px; display: flex; align-items: center; gap: 10px; justify-content: space-between; flex-wrap: wrap; }
      .device-card .name { font-weight: 500; display: flex; align-items: center; gap: 6px; }
      .device-card .type-btns { display: flex; gap: 4px; }
      .device-card .type-btn { padding: 4px 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 11px; cursor: pointer; transition: all 0.2s; }
      .device-card .type-btn:hover { border-color: var(--accent); }
      .device-card .type-btn.active.ios { background: var(--ios-color); color: white; border-color: var(--ios-color); }
      .device-card .type-btn.active.android { background: var(--android-color); color: white; border-color: var(--android-color); }

      .modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
      .modal { background: var(--card-bg); border-radius: 16px; padding: 24px; max-width: 600px; width: 90%; max-height: 85vh; overflow-y: auto; }
      .modal-title { font-size: 18px; font-weight: 600; margin-bottom: 16px; }
      .modal-actions { display: flex; gap: 8px; justify-content: flex-end; margin-top: 20px; }

      .empty-state { text-align: center; padding: 40px; color: var(--text2); }
      .empty-state-icon { font-size: 48px; margin-bottom: 16px; }

      .help-section { margin-bottom: 18px; }
      .help-section h3 { font-size: 14px; margin: 0 0 8px 0; color: var(--text); }
      .help-section p, .help-section li { font-size: 12px; color: var(--text2); line-height: 1.5; }
      .help-section code { background: rgba(0,0,0,0.05); padding: 2px 5px; border-radius: 4px; font-family: monospace; font-size: 11px; }
      .help-section pre { background: rgba(0,0,0,0.05); padding: 10px; border-radius: 8px; overflow-x: auto; font-size: 10px; font-family: monospace; }

      .template-name-input { margin-bottom: 16px; padding: 12px; background: rgba(76,175,80,0.1); border-radius: 10px; border: 2px solid var(--success); }
      .template-name-input label { color: var(--success); font-weight: 600; }
    `;
  }

  render() {
    return html`
      <div class="header">
        <img src="/notify_manager_static/images/logo.png" alt="Logo" class="header-logo">
        <div>
          <h1 class="header-title">${this.t('title')}</h1>
          <div class="header-version">v1.2.7.1 • ${this._getDevices().length} ${this.t('devices')} • ${this._getServiceCount()} ${this.t('services')}</div>
        </div>
        <div class="header-spacer"></div>
        <a href="https://www.buymeacoffee.com/edflock" target="_blank" rel="noopener noreferrer" class="bmc-button">
          <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 36px;">
        </a>
      </div>

      <div class="tabs">
        <button class="tab ${this._tab === 'send' ? 'active' : ''}" @click=${() => this._tab = 'send'}>📤 ${this.t('send')}</button>
        <button class="tab ${this._tab === 'devices' ? 'active' : ''}" @click=${() => this._tab = 'devices'}>📱 ${this.t('devicesGroups')}</button>
        <button class="tab ${this._tab === 'templates' ? 'active' : ''}" @click=${() => this._tab = 'templates'}>📋 ${this.t('templates')}</button>
        <button class="tab ${this._tab === 'help' ? 'active' : ''}" @click=${() => this._tab = 'help'}>❓ ${this.t('help')}</button>
      </div>

      ${this._tab === 'send' ? this._renderSendTab() : ''}
      ${this._tab === 'devices' ? this._renderDevicesTab() : ''}
      ${this._tab === 'templates' ? this._renderTemplatesTab() : ''}
      ${this._tab === 'help' ? this._renderHelpTab() : ''}

      ${this._editingGroup ? this._renderGroupModal() : ''}
    `;
  }

  _renderSendTab() {
    const devices = this._getDevices();
    const cameras = Object.keys(this.hass?.states || {}).filter(e => e.startsWith('camera.'));
    const platforms = this._getTargetPlatforms();
    const showIos = platforms.has('ios');
    const showAndroid = platforms.has('android');

    return html`
      <div class="card">
        <div class="card-title">📨 ${this.t('quickNotification')}</div>

        <!-- Templates -->
        ${this._templates.length ? html`
          <div class="form-group">
            <label>${this.t('useTemplate')}</label>
            <div class="type-selector">
              ${this._templates.map(t => html`
                <div class="type-btn" @click=${() => this._applyTemplate(t)}>${t.name}</div>
              `)}
            </div>
          </div>
        ` : ''}

        <!-- Recipients -->
        <div class="form-group">
          <label>${this.t('recipients')}</label>
          <div class="device-selector">
            <div class="device-chip ${this._selectedDevices.length === 0 && !this._selectedGroup ? 'selected' : ''}"
                 @click=${() => { this._selectedDevices = []; this._selectedGroup = ''; }}>
              📱 ${this.t('allDevices')}
            </div>
            ${this._groups.map(g => html`
              <div class="device-chip group ${this._selectedGroup === g.id ? 'selected' : ''}"
                   @click=${() => { this._selectedGroup = g.id; this._selectedDevices = []; }}>
                👥 ${g.name}
              </div>
            `)}
            ${devices.map(d => html`
              <div class="device-chip ${this._selectedDevices.includes(d) ? 'selected' : ''}"
                   @click=${() => this._toggleDevice(d)}>
                ${this._getDeviceType(d) === 'ios' ? '📱' : this._getDeviceType(d) === 'android' ? '🤖' : '📱'} ${d}
                ${this._getDeviceType(d) ? html`<span class="type-badge ${this._getDeviceType(d)}">${this._getDeviceType(d).toUpperCase()}</span>` : ''}
              </div>
            `)}
          </div>
        </div>

        ${this._renderNotificationForm(cameras, showIos, showAndroid, false)}

        <!-- Action Buttons -->
        <div class="action-buttons">
          <button class="send-btn" @click=${this._send} ?disabled=${this._loading || !this._message}>
            ${this._loading ? `⏳ ${this.t('sending')}` : `📤 ${this.t('sendNotification')}`}
          </button>
          <button class="save-template-btn" @click=${this._saveAsTemplate}>
            💾 ${this.t('saveAsTemplate')}
          </button>
        </div>
        ${this._success ? html`<div class="${this._success.startsWith('❌') ? 'error-msg' : 'success-msg'}">${this._success}</div>` : ''}
      </div>
    `;
  }

  _renderNotificationForm(cameras, showIos, showAndroid, isTemplateMode) {
    return html`
      <!-- Type -->
      <div class="form-group">
        <label>${this.t('notificationType')}</label>
        <div class="type-selector">
          <button class="type-btn ${this._type === 'simple' ? 'active' : ''}" @click=${() => this._type = 'simple'}>📱 ${this.t('simple')}</button>
          <button class="type-btn ${this._type === 'buttons' ? 'active' : ''}" @click=${() => this._type = 'buttons'}>🔘 ${this.t('withButtons')}</button>
          <button class="type-btn ${this._type === 'image' ? 'active' : ''}" @click=${() => this._type = 'image'}>📷 ${this.t('withCamera')}</button>
          <button class="type-btn ${this._type === 'media' ? 'active' : ''}" @click=${() => this._type = 'media'}>🎬 ${this.t('withMedia')}</button>
          ${showAndroid ? html`<button class="type-btn ${this._type === 'tts' ? 'active' : ''}" @click=${() => this._type = 'tts'}>🔊 ${this.t('tts')}</button>` : ''}
          ${showIos ? html`<button class="type-btn ${this._type === 'map' ? 'active' : ''}" @click=${() => this._type = 'map'}>🗺️ ${this.t('map')}</button>` : ''}
          ${showAndroid ? html`<button class="type-btn ${this._type === 'progress' ? 'active' : ''}" @click=${() => this._type = 'progress'}>📊 ${this.t('progress')}</button>` : ''}
        </div>
      </div>

      <!-- Basic Fields -->
      <div class="form-row">
        <div class="form-group">
          <label>${this.t('title_field')}</label>
          <input type="text" .value=${this._title} @input=${(e) => this._title = e.target.value} placeholder="Home Assistant">
        </div>
        <div class="form-group">
          <label>${this.t('subtitle')}</label>
          <input type="text" .value=${this._subtitle} @input=${(e) => this._subtitle = e.target.value} placeholder="${this.t('subtitle')}">
        </div>
      </div>

      <div class="form-group">
        <label>${this._type === 'tts' ? this.t('textToRead') : this.t('message')}</label>
        <textarea .value=${this._message} @input=${(e) => this._message = e.target.value}
                  placeholder="${this._type === 'tts' ? this.t('textToRead') : this.t('message')}..."></textarea>
      </div>

      <!-- Type-specific fields -->
      ${this._type === 'image' ? html`
        <div class="form-row">
          <div class="form-group">
            <label>${this.t('camera')}</label>
            <select .value=${this._camera} @change=${(e) => this._camera = e.target.value}>
              <option value="">${this.t('selectCamera')}</option>
              ${cameras.map(c => html`<option value="${c}">${this.hass.states[c]?.attributes?.friendly_name || c}</option>`)}
            </select>
          </div>
          <div class="form-group">
            <label>${this.t('imageUrl')}</label>
            <input type="text" .value=${this._imageUrl} @input=${(e) => this._imageUrl = e.target.value} placeholder="/local/image.jpg">
          </div>
        </div>
      ` : ''}

      ${this._type === 'media' ? html`
        <div class="form-row">
          <div class="form-group">
            <label>${this.t('imageUrl')}</label>
            <input type="text" .value=${this._imageUrl} @input=${(e) => this._imageUrl = e.target.value} placeholder="/local/image.jpg">
          </div>
          <div class="form-group">
            <label>${this.t('videoUrl')}</label>
            <input type="text" .value=${this._videoUrl} @input=${(e) => this._videoUrl = e.target.value} placeholder="/media/local/video.mp4">
          </div>
          ${showIos ? html`
            <div class="form-group">
              <label>${this.t('audioUrl')}</label>
              <input type="text" .value=${this._audioUrl} @input=${(e) => this._audioUrl = e.target.value} placeholder="/media/local/audio.mp3">
            </div>
          ` : ''}
        </div>
      ` : ''}

      ${this._type === 'buttons' ? this._renderButtonsSection() : ''}

      ${this._type === 'tts' && showAndroid ? html`
        <div class="form-row">
          <div class="form-group">
            <label>Media Stream</label>
            <select .value=${this._mediaStream} @change=${(e) => this._mediaStream = e.target.value}>
              <option value="music_stream">Music</option>
              <option value="alarm_stream">Alarm</option>
              <option value="alarm_stream_max">Alarm Max Volume</option>
            </select>
          </div>
        </div>
      ` : ''}

      ${this._type === 'map' && showIos ? html`
        <div class="form-row">
          <div class="form-group">
            <label>${this.t('latitude')}</label>
            <input type="text" .value=${this._latitude} @input=${(e) => this._latitude = e.target.value} placeholder="52.5200">
          </div>
          <div class="form-group">
            <label>${this.t('longitude')}</label>
            <input type="text" .value=${this._longitude} @input=${(e) => this._longitude = e.target.value} placeholder="13.4050">
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>${this.t('secondPinLat')}</label>
            <input type="text" .value=${this._secondPinLat} @input=${(e) => this._secondPinLat = e.target.value}>
          </div>
          <div class="form-group">
            <label>${this.t('secondPinLng')}</label>
            <input type="text" .value=${this._secondPinLng} @input=${(e) => this._secondPinLng = e.target.value}>
          </div>
        </div>
      ` : ''}

      ${this._type === 'progress' && showAndroid ? html`
        <div class="form-row">
          <div class="form-group">
            <label>${this.t('progressValue')}</label>
            <input type="number" min="0" max="100" .value=${this._progress} @input=${(e) => this._progress = parseInt(e.target.value) || 0}>
          </div>
          <div class="form-group">
            <label>${this.t('progressMax')}</label>
            <input type="number" min="1" .value=${this._progressMax} @input=${(e) => this._progressMax = parseInt(e.target.value) || 100}>
          </div>
        </div>
        <div class="checkbox-row">
          <label class="checkbox-item"><input type="checkbox" .checked=${this._progressIndeterminate} @change=${(e) => this._progressIndeterminate = e.target.checked}> ${this.t('indeterminate')}</label>
        </div>
      ` : ''}

      <!-- Click Action -->
      <div class="form-group">
        <label>${this.t('clickAction')}</label>
        <select .value=${this._clickAction} @change=${(e) => this._clickAction = e.target.value}>
          <option value="">${this.t('selectDashboard')}</option>
          ${this._dashboards.map(d => html`
            <optgroup label="${d.title || d.url_path || 'Default'}">
              ${d.url_path ? html`<option value="/lovelace-${d.url_path}">${d.title || d.url_path}</option>` : html`<option value="/lovelace">Default</option>`}
              ${(d.views || []).map(v => html`
                <option value="${d.url_path ? `/lovelace-${d.url_path}/${v.path || v.title}` : `/lovelace/${v.path || v.title}`}">└ ${v.title || v.path}</option>
              `)}
            </optgroup>
          `)}
        </select>
        <input type="text" style="margin-top: 6px;" placeholder="${this.t('customUrl')}"
               .value=${this._clickAction.startsWith('/lovelace') ? '' : this._clickAction}
               @input=${(e) => this._clickAction = e.target.value}>
      </div>

      <!-- Advanced Options Toggle -->
      <button class="section-toggle" @click=${() => this._showAdvanced = !this._showAdvanced}>
        ${this._showAdvanced ? '▼ ' + this.t('hideAdvanced') : '▶ ' + this.t('showAdvanced')}
      </button>

      ${this._showAdvanced ? this._renderAdvancedOptions(showIos, showAndroid) : ''}

      <!-- Preview -->
      <div class="preview">
        <div class="preview-title">📱 ${this.t('preview')}</div>
        <div class="preview-notification">
          <div class="preview-header">
            <div class="preview-icon"></div>
            <span class="preview-app">HOME ASSISTANT</span>
          </div>
          <div class="preview-t">${this._title || this.t('title_field')}</div>
          ${this._subtitle ? html`<div style="font-size: 12px; color: #aaa;">${this._subtitle}</div>` : ''}
          <div class="preview-m">${this._message || this.t('message') + '...'}</div>
          ${this._type === 'buttons' && this._buttons.length ? html`
            <div class="preview-buttons">
              ${this._buttons.slice(0, 3).map(b => html`<div class="preview-btn">${b.title || 'Button'}</div>`)}
            </div>
          ` : ''}
          ${this._type === 'progress' ? html`
            <div style="background: #444; height: 4px; border-radius: 2px; margin-top: 10px;">
              <div style="background: var(--accent); height: 100%; width: ${this._progressIndeterminate ? '50%' : (this._progress / this._progressMax * 100) + '%'}; border-radius: 2px;"></div>
            </div>
          ` : ''}
        </div>
      </div>

      <!-- Reset Button -->
      <div style="margin-top: 10px;">
        <button class="btn btn-outline" @click=${() => this._resetForm()}>🔄 ${this.t('reset')}</button>
      </div>
    `;
  }

  _renderButtonsSection() {
    return html`
      <div class="form-group">
        <label>${this.t('buttonTemplate')}</label>
        <div class="type-selector" style="margin-bottom: 10px;">
          <div class="type-btn ${this._buttons.length === 0 ? 'active' : ''}" @click=${() => this._buttons = []}>${this.t('none')}</div>
          <div class="type-btn" @click=${() => this._applyButtonTemplate('confirm_dismiss')}>✅ ${this.t('confirmReject')}</div>
          <div class="type-btn" @click=${() => this._applyButtonTemplate('yes_no')}>👍 ${this.t('yesNo')}</div>
          <div class="type-btn" @click=${() => this._applyButtonTemplate('alarm_response')}>🚨 ${this.t('alarm')}</div>
          <div class="type-btn" @click=${() => this._applyButtonTemplate('door_response')}>🚪 ${this.t('door')}</div>
          <div class="type-btn" @click=${() => this._applyButtonTemplate('reply')}>💬 ${this.t('reply')}</div>
        </div>
        <label>${this.t('buttons')} <span style="font-weight: normal; color: var(--text2);">(${this.t('maxButtons')})</span></label>
        <div class="button-list">
          ${this._buttons.map((btn, i) => html`
            <div class="button-item">
              <input type="text" placeholder="${this.t('actionId')}" .value=${btn.action} @input=${(e) => this._updateButton(i, 'action', e.target.value)}>
              <input type="text" placeholder="${this.t('buttonText')}" .value=${btn.title} @input=${(e) => this._updateButton(i, 'title', e.target.value)}>
              <input type="text" placeholder="${this.t('uri')}" .value=${btn.uri || ''} @input=${(e) => this._updateButton(i, 'uri', e.target.value)}>
              <button class="btn btn-danger btn-icon" @click=${() => this._removeButton(i)}>✕</button>
            </div>
            <div class="button-options">
              <label class="checkbox-item"><input type="checkbox" .checked=${btn.destructive || false} @change=${(e) => this._updateButton(i, 'destructive', e.target.checked)}> ${this.t('destructive')}</label>
              <label class="checkbox-item"><input type="checkbox" .checked=${btn.authenticationRequired || false} @change=${(e) => this._updateButton(i, 'authenticationRequired', e.target.checked)}> ${this.t('authRequired')}</label>
            </div>
          `)}
          <button class="btn btn-success btn-small" @click=${this._addButton} ?disabled=${this._buttons.length >= 3}>${this.t('addButton')}</button>
        </div>
      </div>
    `;
  }

  _renderAdvancedOptions(showIos, showAndroid) {
    return html`
      <!-- Grouping -->
      <div class="form-row">
        <div class="form-group">
          <label>${this.t('group')}</label>
          <input type="text" .value=${this._group} @input=${(e) => this._group = e.target.value} placeholder="my_group">
        </div>
        <div class="form-group">
          <label>${this.t('tag')}</label>
          <input type="text" .value=${this._tag} @input=${(e) => this._tag = e.target.value} placeholder="notification_tag">
        </div>
      </div>

      ${showAndroid ? html`
        <div class="platform-section android">
          <h4><span class="badge android">ANDROID</span> ${this.t('androidOptions')}</h4>
          <div class="form-row">
            <div class="form-group">
              <label>${this.t('channel')}</label>
              <input type="text" .value=${this._channel} @input=${(e) => this._channel = e.target.value} placeholder="alerts">
            </div>
            <div class="form-group">
              <label>${this.t('importance')}</label>
              <select .value=${this._importance} @change=${(e) => this._importance = e.target.value}>
                <option value="default">${this.t('default')}</option>
                <option value="low">${this.t('low')}</option>
                <option value="high">${this.t('high')}</option>
                <option value="max">${this.t('max')}</option>
                <option value="min">${this.t('min')}</option>
              </select>
            </div>
            <div class="form-group">
              <label>${this.t('color')}</label>
              <input type="color" .value=${this._color || '#03a9f4'} @input=${(e) => this._color = e.target.value}>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>${this.t('notificationIcon')}</label>
              <input type="text" .value=${this._notificationIcon} @input=${(e) => this._notificationIcon = e.target.value} placeholder="mdi:bell">
            </div>
            <div class="form-group">
              <label>${this.t('iconUrl')}</label>
              <input type="text" .value=${this._iconUrl} @input=${(e) => this._iconUrl = e.target.value} placeholder="https://...">
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>${this.t('ledColor')}</label>
              <input type="text" .value=${this._ledColor} @input=${(e) => this._ledColor = e.target.value} placeholder="red">
            </div>
            <div class="form-group">
              <label>${this.t('vibrationPattern')}</label>
              <input type="text" .value=${this._vibrationPattern} @input=${(e) => this._vibrationPattern = e.target.value} placeholder="100, 1000, 100">
            </div>
            <div class="form-group">
              <label>${this.t('timeout')}</label>
              <input type="number" min="0" .value=${this._timeout} @input=${(e) => this._timeout = parseInt(e.target.value) || 0}>
            </div>
          </div>
          <div class="form-group">
            <label>${this.t('visibility')}</label>
            <select .value=${this._visibility} @change=${(e) => this._visibility = e.target.value}>
              <option value="public">${this.t('public')}</option>
              <option value="private">${this.t('private')}</option>
              <option value="secret">${this.t('secret')}</option>
            </select>
          </div>
          <div class="checkbox-row">
            <label class="checkbox-item"><input type="checkbox" .checked=${this._sticky} @change=${(e) => this._sticky = e.target.checked}> ${this.t('sticky')}</label>
            <label class="checkbox-item"><input type="checkbox" .checked=${this._persistent} @change=${(e) => this._persistent = e.target.checked}> ${this.t('persistent')}</label>
            <label class="checkbox-item"><input type="checkbox" .checked=${this._alertOnce} @change=${(e) => this._alertOnce = e.target.checked}> ${this.t('alertOnce')}</label>
            <label class="checkbox-item"><input type="checkbox" .checked=${this._carUi} @change=${(e) => this._carUi = e.target.checked}> ${this.t('carUi')}</label>
            <label class="checkbox-item"><input type="checkbox" .checked=${this._chronometer} @change=${(e) => this._chronometer = e.target.checked}> ${this.t('chronometerValue')}</label>
          </div>
        </div>
      ` : ''}

      ${showIos ? html`
        <div class="platform-section ios">
          <h4><span class="badge ios">iOS</span> ${this.t('iosOptions')}</h4>
          <div class="form-row">
            <div class="form-group">
              <label>${this.t('sound')}</label>
              <input type="text" .value=${this._sound} @input=${(e) => this._sound = e.target.value} placeholder="default">
            </div>
            <div class="form-group">
              <label>${this.t('badge')}</label>
              <input type="number" min="0" .value=${this._badge} @input=${(e) => this._badge = parseInt(e.target.value) || 0}>
            </div>
            <div class="form-group">
              <label>${this.t('interruptionLevel')}</label>
              <select .value=${this._interruptionLevel} @change=${(e) => this._interruptionLevel = e.target.value}>
                <option value="passive">${this.t('passive')}</option>
                <option value="active">${this.t('active')}</option>
                <option value="time-sensitive">${this.t('timeSensitive')}</option>
                <option value="critical">${this.t('criticalLevel')}</option>
              </select>
            </div>
          </div>
          <div class="checkbox-row">
            <label class="checkbox-item"><input type="checkbox" .checked=${this._critical} @change=${(e) => this._critical = e.target.checked}> ${this.t('criticalAlert')}</label>
          </div>
          ${this._critical ? html`
            <div class="form-group">
              <label>${this.t('criticalVolume')} (0.0 - 1.0)</label>
              <input type="number" min="0" max="1" step="0.1" .value=${this._criticalVolume} @input=${(e) => this._criticalVolume = parseFloat(e.target.value) || 1.0}>
            </div>
          ` : ''}
        </div>
      ` : ''}

      <!-- Attachment Options -->
      ${(this._type === 'image' || this._type === 'media') ? html`
        <div class="platform-section">
          <h4>📎 ${this.t('attachmentOptions')}</h4>
          <div class="checkbox-row">
            <label class="checkbox-item"><input type="checkbox" .checked=${this._hideThumbnail} @change=${(e) => this._hideThumbnail = e.target.checked}> ${this.t('hideThumbnail')}</label>
            ${showIos ? html`<label class="checkbox-item"><input type="checkbox" .checked=${this._lazyLoad} @change=${(e) => this._lazyLoad = e.target.checked}> ${this.t('lazyLoad')}</label>` : ''}
          </div>
          <div class="form-group">
            <label>${this.t('contentType')}</label>
            <input type="text" .value=${this._contentType} @input=${(e) => this._contentType = e.target.value} placeholder="image/jpeg">
          </div>
        </div>
      ` : ''}
    `;
  }

  _renderDevicesTab() {
    const devices = this._getDevices();
    const activeGroup = this._activeGroupId ? this._groups.find(g => g.id === this._activeGroupId) : null;

    return html`
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">${devices.length}</div>
          <div class="stat-label">${this.t('devices')}</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${this._groups.length}</div>
          <div class="stat-label">${this.t('groups')}</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${this._getServiceCount()}</div>
          <div class="stat-label">${this.t('services')}</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${devices.filter(d => this._getDeviceType(d) === 'ios').length}</div>
          <div class="stat-label">iOS</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${devices.filter(d => this._getDeviceType(d) === 'android').length}</div>
          <div class="stat-label">Android</div>
        </div>
      </div>

      <!-- Device Types -->
      <div class="card">
        <div class="card-title">📱 ${this.t('connectedDevices')} - ${this.t('deviceType')}</div>
        <p style="color: var(--text2); font-size: 12px; margin-bottom: 12px;">${this.t('setDeviceType')}</p>
        <div style="display: flex; flex-direction: column; gap: 8px;">
          ${devices.map(d => html`
            <div class="device-card">
              <div class="name">
                ${this._getDeviceType(d) === 'ios' ? '📱' : this._getDeviceType(d) === 'android' ? '🤖' : '❓'}
                ${d}
              </div>
              <div class="type-btns">
                <button class="type-btn ${this._getDeviceType(d) === 'ios' ? 'active ios' : ''}" @click=${() => this._setDeviceType(d, 'ios')}>iOS</button>
                <button class="type-btn ${this._getDeviceType(d) === 'android' ? 'active android' : ''}" @click=${() => this._setDeviceType(d, 'android')}>Android</button>
              </div>
            </div>
          `)}
          ${!devices.length ? html`<p style="color: var(--text2);">${this.t('noDevices')}</p>` : ''}
        </div>
      </div>

      <!-- Groups -->
      <div class="card">
        <div class="card-title">
          <span>👥 ${this.t('deviceGroups')}</span>
          <button class="btn btn-primary btn-small" @click=${() => this._editingGroup = { id: '', name: '', devices: [] }}>${this.t('newGroup')}</button>
        </div>
        <p style="color: var(--text2); font-size: 12px; margin-bottom: 12px;">${this.t('clickToAddRemove')}</p>

        ${this._groups.length ? html`
          <div class="group-grid" style="margin-bottom: 16px;">
            ${this._groups.map(g => html`
              <div class="group-card ${this._activeGroupId === g.id ? 'active-group' : ''}"
                   @click=${() => this._activeGroupId = this._activeGroupId === g.id ? null : g.id}>
                <div class="group-name">👥 ${g.name}</div>
                <div class="group-info">${g.devices?.length || 0} ${this.t('devices')}</div>
                <div class="group-actions" @click=${(e) => e.stopPropagation()}>
                  <button class="btn btn-outline btn-small" @click=${() => this._editingGroup = {...g, devices: [...(g.devices || [])]}}}>✏️</button>
                  <button class="btn btn-danger btn-small" @click=${() => this._deleteGroup(g.id)}>🗑️</button>
                </div>
              </div>
            `)}
          </div>

          ${activeGroup ? html`
            <div style="background: rgba(3,169,244,0.1); padding: 12px; border-radius: 8px;">
              <p style="color: var(--accent); font-size: 13px; margin: 0 0 10px 0;">
                <strong>${this.t('clickDevicesFor')} "${activeGroup.name}":</strong>
              </p>
              <div class="device-selector">
                ${devices.map(d => {
                  const isInGroup = (activeGroup.devices || []).includes(d);
                  return html`
                    <div class="device-chip ${isInGroup ? 'selected' : ''}"
                         @click=${() => this._toggleDeviceInGroup(d, activeGroup.id)}>
                      ${this._getDeviceType(d) === 'ios' ? '📱' : '🤖'} ${d} ${isInGroup ? '✓' : ''}
                    </div>
                  `;
                })}
              </div>
            </div>
          ` : ''}
        ` : html`
          <div class="empty-state">
            <div class="empty-state-icon">👥</div>
            <p>${this.t('noGroups')}</p>
          </div>
        `}
      </div>
    `;
  }

  _renderTemplatesTab() {
    const devices = this._getDevices();
    const cameras = Object.keys(this.hass?.states || {}).filter(e => e.startsWith('camera.'));
    const platforms = this._getTargetPlatforms();
    const showIos = platforms.has('ios');
    const showAndroid = platforms.has('android');

    return html`
      <!-- Saved Templates -->
      ${this._templates.length ? html`
        <div class="card">
          <div class="card-title">📋 ${this.t('savedTemplates')}</div>
          <div class="template-grid">
            ${this._templates.map(t => html`
              <div class="template-card">
                <div class="template-name">${t.name}</div>
                <div class="template-preview">${t.title}: ${t.message?.substring(0, 30)}${t.message?.length > 30 ? '...' : ''}</div>
                <div class="template-preview">${this.t('type')}: ${t.type} | ${t.buttons?.length || 0} buttons</div>
                <div class="template-actions">
                  <button class="btn btn-primary btn-small" @click=${() => { this._loadTemplateForEdit(t); }}>${this.t('editTemplate')}</button>
                  <button class="btn btn-outline btn-small" @click=${() => { this._applyTemplate(t); this._tab = 'send'; }}>${this.t('use')}</button>
                  <button class="btn btn-danger btn-small" @click=${() => this._deleteTemplate(t.id)}>🗑️</button>
                </div>
              </div>
            `)}
          </div>
        </div>
      ` : ''}

      <!-- Template Editor - Same as Send Tab -->
      <div class="card">
        <div class="card-title">
          ${this._templateFormId ? `✏️ ${this.t('editTemplate')}` : `📝 ${this.t('createTemplate')}`}
        </div>

        <!-- Template Name Input (highlighted) -->
        <div class="template-name-input">
          <label>📋 ${this.t('templateName')} *</label>
          <input type="text" .value=${this._templateFormName}
                 @input=${(e) => this._templateFormName = e.target.value}
                 placeholder="🚪 Türklingel, 🚨 Alarm, etc.">
        </div>

        ${this._renderNotificationForm(cameras, showIos, showAndroid, true)}

        <!-- Action Buttons -->
        <div class="action-buttons">
          <button class="save-template-btn" @click=${this._saveTemplateFromEditor} ?disabled=${!this._templateFormName}>
            💾 ${this._templateFormId ? this.t('save') : this.t('saveAsTemplate')}
          </button>
          ${this._templateFormId ? html`
            <button class="btn btn-outline" style="padding: 14px;" @click=${() => { this._resetForm(); this._templateFormId = ''; this._templateFormName = ''; }}>
              ❌ ${this.t('cancel')}
            </button>
          ` : ''}
        </div>
        ${this._success ? html`<div class="${this._success.startsWith('❌') ? 'error-msg' : 'success-msg'}">${this._success}</div>` : ''}
      </div>
    `;
  }

  _renderHelpTab() {
    return html`
      <div class="card">
        <div class="card-title">❓ ${this.t('helpTitle')}</div>

        <div class="help-section">
          <h3>🚀 ${this.t('quickStart')}</h3>
          <p>${this.t('quickStartText').split('\n').map(line => html`${line}<br>`)}</p>
        </div>

        <div class="help-section">
          <h3>📱 ${this.t('iosFeatures')}</h3>
          <p>${this.t('iosFeaturesText')}</p>
          <ul>
            <li><code>critical: true</code> - Override DND</li>
            <li><code>badge: 5</code> - App icon badge</li>
            <li><code>sound: "default"</code> - Custom sounds</li>
            <li><code>interruption-level</code> - passive, active, time-sensitive, critical</li>
          </ul>
        </div>

        <div class="help-section">
          <h3>🤖 ${this.t('androidFeatures')}</h3>
          <p>${this.t('androidFeaturesText')}</p>
          <ul>
            <li><code>channel: "alerts"</code> - Notification channels</li>
            <li><code>color: "#FF0000"</code> - Notification color</li>
            <li><code>ledColor: "red"</code> - LED color</li>
            <li><code>vibrationPattern: "100, 1000, 100"</code></li>
            <li><code>sticky: true</code> - Cannot dismiss</li>
            <li><code>persistent: true</code> - Stays until cleared</li>
            <li><code>chronometer: true</code> - Timer display</li>
            <li><code>message: TTS</code> with <code>tts_text</code> - Text-to-speech</li>
          </ul>
        </div>

        <div class="help-section">
          <h3>🔄 ${this.t('buttonReaction')}</h3>
          <pre>trigger:
  - platform: event
    event_type: mobile_app_notification_action
    event_data:
      action: "YOUR_ACTION_ID"
action:
  - service: notify.notify
    data:
      message: "Button pressed!"</pre>
        </div>

        <div class="help-section">
          <h3>📲 ${this.t('availableServices')}</h3>
          <ul>
            <li><code>send_notification</code> - Simple notification</li>
            <li><code>send_actionable</code> - With buttons</li>
            <li><code>send_with_image</code> - With camera/image</li>
            <li><code>send_tts</code> - Text-to-speech (Android)</li>
            <li><code>send_map</code> - Map with pin (iOS)</li>
            <li><code>send_progress</code> - Progress bar (Android)</li>
            <li><code>send_chronometer</code> - Timer (Android)</li>
            <li><code>send_from_template</code> - From template</li>
            <li><code>send_to_group</code> - Send to device group</li>
            <li><code>device_command</code> - Device commands (Android)</li>
          </ul>
        </div>
      </div>
    `;
  }

  _renderGroupModal() {
    const g = this._editingGroup;
    const devices = this._getDevices();

    return html`
      <div class="modal-overlay" @click=${(e) => { if(e.target === e.currentTarget) this._editingGroup = null; }}>
        <div class="modal">
          <div class="modal-title">${g.id ? `✏️ ${this.t('editGroup')}` : `👥 ${this.t('newGroupTitle')}`}</div>

          <div class="form-group">
            <label>${this.t('groupName')}</label>
            <input type="text" .value=${g.name} @input=${(e) => g.name = e.target.value} placeholder="Family">
          </div>

          <div class="form-group">
            <label>${this.t('selectDevices')}</label>
            <div class="device-selector">
              ${devices.map(d => html`
                <div class="device-chip ${(g.devices || []).includes(d) ? 'selected' : ''}"
                     @click=${() => {
                       g.devices = g.devices || [];
                       if(g.devices.includes(d)) g.devices = g.devices.filter(x => x !== d);
                       else g.devices = [...g.devices, d];
                       this.requestUpdate();
                     }}>
                  ${this._getDeviceType(d) === 'ios' ? '📱' : '🤖'} ${d}
                </div>
              `)}
            </div>
          </div>

          <div class="modal-actions">
            <button class="btn btn-outline" @click=${() => this._editingGroup = null}>${this.t('cancel')}</button>
            <button class="btn btn-primary" @click=${() => this._saveGroup(g)}>💾 ${this.t('save')}</button>
          </div>
        </div>
      </div>
    `;
  }

  // Helpers
  _getDevices() {
    return Object.keys(this.hass?.services?.notify || {})
      .filter(s => s.startsWith('mobile_app_'))
      .map(s => s.replace('mobile_app_', ''));
  }

  _getServiceCount() {
    return Object.keys(this.hass?.services?.notify_manager || {}).length;
  }

  _toggleDevice(device) {
    this._selectedGroup = '';
    if (this._selectedDevices.includes(device)) {
      this._selectedDevices = this._selectedDevices.filter(d => d !== device);
    } else {
      this._selectedDevices = [...this._selectedDevices, device];
    }
  }

  _toggleDeviceInGroup(device, groupId) {
    const group = this._groups.find(g => g.id === groupId);
    if (!group) return;
    group.devices = group.devices || [];
    if (group.devices.includes(device)) {
      group.devices = group.devices.filter(d => d !== device);
    } else {
      group.devices = [...group.devices, device];
    }
    this._groups = [...this._groups];
    this._saveToStorage("notify_manager_groups", this._groups);
    this.requestUpdate();
  }

  _applyTemplate(t) {
    this._title = t.title || '';
    this._message = t.message || '';
    this._type = t.type || 'simple';
    this._priority = t.priority || 'normal';
    this._buttons = [...(t.buttons || [])];
    // Load additional template settings if available
    if (t.channel) this._channel = t.channel;
    if (t.color) this._color = t.color;
    if (t.sound) this._sound = t.sound;
    if (t.clickAction) this._clickAction = t.clickAction;
  }

  _loadTemplateForEdit(t) {
    this._templateFormId = t.id;
    this._templateFormName = t.name;
    this._applyTemplate(t);
  }

  _applyButtonTemplate(templateName) {
    const templates = {
      confirm_dismiss: [{ action: 'CONFIRM', title: '✅ Confirm' }, { action: 'DISMISS', title: '❌ Dismiss' }],
      yes_no: [{ action: 'YES', title: '👍 Yes' }, { action: 'NO', title: '👎 No' }],
      alarm_response: [{ action: 'ALARM_OK', title: '✅ OK' }, { action: 'ALARM_SNOOZE', title: '⏰ Later' }, { action: 'ALARM_EMERGENCY', title: '🆘 Emergency' }],
      door_response: [{ action: 'DOOR_OPEN', title: '🔓 Open' }, { action: 'DOOR_IGNORE', title: '🚪 Ignore' }],
      reply: [{ action: 'REPLY', title: '💬 Reply' }]
    };
    this._buttons = [...(templates[templateName] || [])];
  }

  _addButton() { if (this._buttons.length < 3) this._buttons = [...this._buttons, { action: '', title: '' }]; }
  _removeButton(i) { this._buttons = this._buttons.filter((_, idx) => idx !== i); }
  _updateButton(i, field, value) { this._buttons = this._buttons.map((btn, idx) => idx === i ? { ...btn, [field]: value } : btn); }

  _saveAsTemplate() {
    const name = prompt(this.t('templateName') + ":", this._title || "📝 New Template");
    if (!name) return;
    const newTemplate = this._buildTemplateFromForm(name, '');
    this._templates = [...this._templates, newTemplate];
    this._saveToStorage("notify_manager_templates", this._templates);
    this._success = `✅ ${this.t('templateSaved')}`;
    setTimeout(() => this._success = "", 3000);
  }

  _saveTemplateFromEditor() {
    if (!this._templateFormName) {
      alert(this.t('enterName'));
      return;
    }

    const template = this._buildTemplateFromForm(this._templateFormName, this._templateFormId);

    if (this._templateFormId) {
      // Update existing
      this._templates = this._templates.map(t => t.id === this._templateFormId ? template : t);
    } else {
      // Create new
      this._templates = [...this._templates, template];
    }

    this._saveToStorage("notify_manager_templates", this._templates);
    this._success = `✅ ${this.t('templateSaved')}`;
    setTimeout(() => this._success = "", 3000);

    // Reset form
    this._resetForm();
    this._templateFormId = '';
    this._templateFormName = '';
  }

  _buildTemplateFromForm(name, existingId) {
    return {
      id: existingId || 'tpl_' + Date.now(),
      name,
      title: this._title,
      message: this._message,
      type: this._type,
      priority: this._priority,
      buttons: [...this._buttons],
      // Save additional settings
      channel: this._channel,
      color: this._color,
      sound: this._sound,
      clickAction: this._clickAction,
      sticky: this._sticky,
      persistent: this._persistent,
      importance: this._importance,
      interruptionLevel: this._interruptionLevel,
      critical: this._critical,
      criticalVolume: this._criticalVolume,
    };
  }

  _deleteTemplate(id) {
    if (!confirm(this.t('deleteConfirm'))) return;
    this._templates = this._templates.filter(t => t.id !== id);
    this._saveToStorage("notify_manager_templates", this._templates);
  }

  _saveGroup(g) {
    if (!g.name) { alert(this.t('enterName')); return; }
    if (!g.devices?.length) { alert(this.t('selectAtLeastOne')); return; }
    if (g.id) {
      this._groups = this._groups.map(x => x.id === g.id ? {...g} : x);
    } else {
      g.id = 'grp_' + Date.now();
      this._groups = [...this._groups, {...g}];
    }
    this._saveToStorage("notify_manager_groups", this._groups);
    this._editingGroup = null;
  }

  _deleteGroup(id) {
    if (!confirm(this.t('deleteConfirm'))) return;
    this._groups = this._groups.filter(g => g.id !== id);
    this._saveToStorage("notify_manager_groups", this._groups);
  }

  async _send() {
    if (!this._message && this._type !== 'tts') return;
    this._loading = true;
    this._success = "";

    try {
      // Build data object with ALL options
      const data = {
        title: this._title || "Home Assistant",
        message: this._message,
      };

      // Basic options
      if (this._subtitle) data.subtitle = this._subtitle;
      if (this._clickAction) data.clickAction = this._clickAction;
      if (this._group) data.group = this._group;
      if (this._tag) data.tag = this._tag;

      // Target
      let targets = [];
      if (this._selectedGroup) {
        const group = this._groups.find(g => g.id === this._selectedGroup);
        if (group) targets = group.devices;
      } else if (this._selectedDevices.length) {
        targets = this._selectedDevices;
      }
      if (targets.length) data.target = targets;

      // Determine service and add type-specific data
      let service = "send_advanced";

      // Android options
      if (this._channel) data.channel = this._channel;
      if (this._importance !== 'default') data.importance = this._importance;
      if (this._color) data.color = this._color;
      if (this._ledColor) data.ledColor = this._ledColor;
      if (this._vibrationPattern) data.vibrationPattern = this._vibrationPattern;
      if (this._notificationIcon) data.notification_icon = this._notificationIcon;
      if (this._iconUrl) data.icon_url = this._iconUrl;
      if (this._sticky) data.sticky = true;
      if (this._persistent) data.persistent = true;
      if (this._alertOnce) data.alert_once = true;
      if (this._timeout > 0) data.timeout = this._timeout;
      if (this._visibility !== 'public') data.visibility = this._visibility;
      if (this._carUi) data.car_ui = true;
      if (this._chronometer) data.chronometer = true;

      // iOS options
      if (this._sound) data.sound = this._sound;
      if (this._badge > 0) data.badge = this._badge;
      if (this._interruptionLevel !== 'active') data["interruption-level"] = this._interruptionLevel;
      if (this._critical) {
        data.push = { sound: { critical: 1, volume: this._criticalVolume } };
      }

      // Type specific
      if (this._type === 'buttons' && this._buttons.length) {
        data.actions = this._buttons.filter(b => b.action && b.title);
      }

      if (this._type === 'image') {
        if (this._camera) data.camera_entity = this._camera;
        if (this._imageUrl) data.image = this._imageUrl;
      }

      if (this._type === 'media') {
        if (this._imageUrl) data.image = this._imageUrl;
        if (this._videoUrl) data.video = this._videoUrl;
        if (this._audioUrl) data.audio = this._audioUrl;
      }

      if (this._type === 'tts') {
        service = "send_tts";
        data.tts_text = this._message;
        data.media_stream = this._mediaStream;
      }

      if (this._type === 'map') {
        if (this._latitude && this._longitude) {
          data.action_data = {
            latitude: parseFloat(this._latitude),
            longitude: parseFloat(this._longitude),
          };
          if (this._secondPinLat && this._secondPinLng) {
            data.action_data.second_latitude = parseFloat(this._secondPinLat);
            data.action_data.second_longitude = parseFloat(this._secondPinLng);
          }
        }
      }

      if (this._type === 'progress') {
        data.progress = this._progress;
        data.progress_max = this._progressMax;
        if (this._progressIndeterminate) data.progress_indeterminate = true;
      }

      // Attachment options
      if (this._hideThumbnail) data["hide-thumbnail"] = true;
      if (this._lazyLoad) data.lazy = true;
      if (this._contentType) data["content-type"] = this._contentType;

      await this.hass.callService("notify_manager", service, data);
      this._success = `✅ ${this.t('sent')}`;
      setTimeout(() => this._success = "", 3000);
    } catch (err) {
      console.error("Send error:", err);
      this._success = `❌ ${this.t('error')}: ` + err.message;
    } finally {
      this._loading = false;
    }
  }
}

customElements.define("notify-manager-panel", NotifyManagerPanel);
