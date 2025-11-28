/**
 * Notify Manager Panel - Vollständig mit Kategorien, Sensoren, Vorlagen & Gruppen
 * Version 1.2.3.1
 */

import {
  LitElement,
  html,
  css,
} from "https://unpkg.com/lit-element@2.5.1/lit-element.js?module";

class NotifyManagerPanel extends LitElement {
  static get properties() {
    return {
      hass: { type: Object },
      narrow: { type: Boolean },
      _tab: { type: String },
      _loading: { type: Boolean },
      _success: { type: String },
      // Send Form
      _title: { type: String },
      _message: { type: String },
      _type: { type: String },
      _priority: { type: String },
      _camera: { type: String },
      _buttons: { type: Array },
      _selectedDevices: { type: Array },
      _selectedGroup: { type: String },
      // Templates & Groups (localStorage)
      _templates: { type: Array },
      _groups: { type: Array },
      // Edit mode
      _editingTemplate: { type: Object },
      _editingGroup: { type: Object },
    };
  }

  constructor() {
    super();
    this._tab = "send";
    this._loading = false;
    this._success = "";
    this._title = "";
    this._message = "";
    this._type = "simple";
    this._priority = "normal";
    this._camera = "";
    this._buttons = [];
    this._selectedDevices = [];
    this._selectedGroup = "";
    this._editingTemplate = null;
    this._editingGroup = null;
    
    this._templates = this._loadFromStorage("notify_manager_templates", [
      { id: "doorbell", name: "🚪 Türklingel", title: "Türklingel", message: "Jemand ist an der Tür!", type: "image", priority: "high", buttons: [{ action: "DOOR_OPEN", title: "🔓 Öffnen" }, { action: "DOOR_IGNORE", title: "Ignorieren" }] },
      { id: "alarm", name: "🚨 Alarm", title: "Alarm!", message: "Bewegung erkannt", type: "buttons", priority: "critical", buttons: [{ action: "ALARM_OK", title: "✓ OK" }, { action: "ALARM_CALL", title: "📞 Anrufen" }] },
      { id: "reminder", name: "⏰ Erinnerung", title: "Erinnerung", message: "", type: "simple", priority: "normal", buttons: [] },
    ]);
    this._groups = this._loadFromStorage("notify_manager_groups", []);
    
    // Sync templates to Home Assistant on load
    this._syncTemplatesToHA();
  }

  _loadFromStorage(key, defaultValue) {
    try {
      const stored = localStorage.getItem(key);
      return stored ? JSON.parse(stored) : defaultValue;
    } catch {
      return defaultValue;
    }
  }

  _saveToStorage(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      // Also sync to HA if templates
      if (key === "notify_manager_templates") {
        this._syncTemplatesToHA();
      }
    } catch (e) {
      console.error("Storage error:", e);
    }
  }

  async _syncTemplatesToHA() {
    // Send templates to Home Assistant so services can use them
    if (this.hass && this._templates) {
      try {
        await this.hass.callService("notify_manager", "save_templates", {
          templates: this._templates
        });
      } catch (e) {
        // Service might not exist yet, that's ok
        console.debug("Template sync:", e);
      }
    }
  }

  static get styles() {
    return css`
      :host {
        display: block;
        padding: 16px;
        max-width: 1000px;
        margin: 0 auto;
        --accent: var(--primary-color, #03a9f4);
        --card-bg: var(--ha-card-background, var(--card-background-color, #fff));
        --text: var(--primary-text-color, #212121);
        --text2: var(--secondary-text-color, #727272);
        --border: var(--divider-color, #e0e0e0);
        --success: #4caf50;
        --error: #f44336;
        --warning: #ff9800;
      }

      /* Header mit Logo */
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
      }
      .header-logo {
        width: 64px;
        height: 64px;
        border-radius: 12px;
        background: white;
        padding: 4px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
      }
      .header-info { flex: 1; }
      .header-title {
        font-size: 26px;
        font-weight: 600;
        margin: 0 0 4px 0;
      }
      .header-version {
        font-size: 13px;
        opacity: 0.9;
      }

      /* Tabs */
      .tabs {
        display: flex;
        gap: 4px;
        margin-bottom: 16px;
        border-bottom: 1px solid var(--border);
        padding-bottom: 8px;
        flex-wrap: wrap;
      }
      .tab {
        padding: 10px 16px;
        background: none;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 500;
        color: var(--text2);
        transition: all 0.2s;
      }
      .tab:hover { background: rgba(0,0,0,0.05); color: var(--text); }
      .tab.active { background: var(--accent); color: white; }

      /* Cards */
      .card {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 20px;
        box-shadow: var(--ha-card-box-shadow, 0 2px 8px rgba(0,0,0,0.1));
        margin-bottom: 16px;
      }
      .card-title {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 16px;
        display: flex;
        align-items: center;
        gap: 8px;
        justify-content: space-between;
        color: var(--text);
      }

      /* Stats Grid */
      .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 12px;
        margin-bottom: 16px;
      }
      .stat-card {
        background: linear-gradient(135deg, rgba(3,169,244,0.1), rgba(3,169,244,0.05));
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        border: 1px solid rgba(3,169,244,0.2);
      }
      .stat-value {
        font-size: 32px;
        font-weight: 700;
        color: var(--accent);
      }
      .stat-label {
        font-size: 12px;
        color: var(--text2);
        margin-top: 4px;
      }

      /* Switch List */
      .switch-list { display: flex; flex-direction: column; gap: 8px; }
      .switch-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 16px;
        background: rgba(0,0,0,0.02);
        border-radius: 10px;
        transition: all 0.2s;
      }
      .switch-item:hover { background: rgba(0,0,0,0.04); }
      .switch-item.master {
        background: linear-gradient(135deg, rgba(3,169,244,0.15), rgba(3,169,244,0.05));
        border: 1px solid rgba(3,169,244,0.3);
      }
      .switch-info { display: flex; align-items: center; gap: 12px; }
      .switch-icon {
        width: 36px;
        height: 36px;
        border-radius: 8px;
        background: var(--accent);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
      }
      .switch-name { font-weight: 500; color: var(--text); }
      .switch-toggle {
        position: relative;
        width: 50px;
        height: 28px;
        background: #ccc;
        border-radius: 14px;
        cursor: pointer;
        transition: all 0.3s;
      }
      .switch-toggle.on { background: var(--accent); }
      .switch-toggle::after {
        content: '';
        position: absolute;
        width: 22px;
        height: 22px;
        background: white;
        border-radius: 50%;
        top: 3px;
        left: 3px;
        transition: all 0.3s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
      }
      .switch-toggle.on::after { left: 25px; }

      /* Form Elements */
      .form-group { margin-bottom: 16px; }
      label {
        display: block;
        font-size: 13px;
        font-weight: 500;
        color: var(--text2);
        margin-bottom: 6px;
      }
      input, textarea, select {
        width: 100%;
        padding: 10px 12px;
        border: 1px solid var(--border);
        border-radius: 8px;
        font-size: 14px;
        background: var(--card-bg);
        color: var(--text);
        box-sizing: border-box;
        font-family: inherit;
      }
      input:focus, textarea:focus, select:focus {
        outline: none;
        border-color: var(--accent);
        box-shadow: 0 0 0 2px rgba(3,169,244,0.2);
      }
      textarea { resize: vertical; min-height: 80px; }

      .row { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
      @media (max-width: 600px) { .row { grid-template-columns: 1fr; } }

      /* Buttons & Chips */
      .type-selector, .device-selector { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }
      .type-btn, .device-chip {
        padding: 10px 14px;
        border: 2px solid var(--border);
        border-radius: 10px;
        background: var(--card-bg);
        cursor: pointer;
        font-size: 13px;
        font-weight: 500;
        color: var(--text);
        transition: all 0.2s;
        display: flex;
        align-items: center;
        gap: 6px;
      }
      .type-btn:hover, .device-chip:hover { border-color: var(--accent); }
      .type-btn.active, .device-chip.selected {
        border-color: var(--accent);
        background: var(--accent);
        color: white;
      }
      .device-chip.group { border-style: dashed; }
      .device-chip.group.selected { border-style: solid; }

      /* Button List */
      .button-list { display: flex; flex-direction: column; gap: 8px; }
      .button-item { display: flex; gap: 8px; align-items: center; }
      .button-item input { flex: 1; }

      /* Buttons */
      .btn {
        padding: 8px 16px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.2s;
        display: inline-flex;
        align-items: center;
        gap: 6px;
      }
      .btn:hover { opacity: 0.85; transform: translateY(-1px); }
      .btn-primary { background: var(--accent); color: white; }
      .btn-success { background: var(--success); color: white; }
      .btn-danger { background: var(--error); color: white; }
      .btn-outline { background: transparent; border: 1px solid var(--border); color: var(--text); }
      .btn-small { padding: 6px 12px; font-size: 12px; }
      .btn-icon { width: 36px; height: 36px; padding: 0; justify-content: center; border-radius: 50%; }

      .send-btn {
        width: 100%;
        padding: 14px;
        background: linear-gradient(135deg, var(--accent), #0288d1);
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        box-shadow: 0 4px 12px rgba(3,169,244,0.3);
      }
      .send-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(3,169,244,0.4); }
      .send-btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; box-shadow: none; }

      /* Messages */
      .success-msg {
        background: rgba(76,175,80,0.1);
        color: var(--success);
        padding: 12px;
        border-radius: 8px;
        margin-top: 12px;
        text-align: center;
        font-weight: 500;
      }
      .error-msg {
        background: rgba(244,67,54,0.1);
        color: var(--error);
        padding: 12px;
        border-radius: 8px;
        margin-top: 12px;
        text-align: center;
        font-weight: 500;
      }

      /* Preview */
      .preview {
        background: #1a1a1a;
        border-radius: 12px;
        padding: 16px;
        color: white;
        margin-top: 16px;
      }
      .preview-title { font-size: 12px; color: #888; margin-bottom: 8px; }
      .preview-notification {
        background: #2d2d2d;
        border-radius: 10px;
        padding: 12px;
      }
      .preview-header { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
      .preview-icon { width: 20px; height: 20px; background: var(--accent); border-radius: 4px; }
      .preview-app { font-size: 11px; color: #888; }
      .preview-t { font-weight: 600; font-size: 14px; }
      .preview-m { font-size: 13px; color: #ccc; margin-top: 4px; }
      .preview-buttons {
        display: flex;
        gap: 8px;
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid #444;
      }
      .preview-btn {
        flex: 1;
        padding: 8px;
        background: #444;
        border-radius: 6px;
        text-align: center;
        font-size: 12px;
        color: white;
      }

      /* Grids */
      .template-grid, .group-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 12px;
      }
      .template-card, .group-card {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 14px;
        cursor: pointer;
        transition: all 0.2s;
      }
      .template-card:hover, .group-card:hover {
        border-color: var(--accent);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
      }
      .template-name, .group-name { font-weight: 600; font-size: 15px; margin-bottom: 4px; }
      .template-preview, .group-info { font-size: 12px; color: var(--text2); }
      .template-actions, .group-actions { display: flex; gap: 8px; margin-top: 10px; }

      /* Modal */
      .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
      }
      .modal {
        background: var(--card-bg);
        border-radius: 16px;
        padding: 24px;
        max-width: 500px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
      }
      .modal-title { font-size: 18px; font-weight: 600; margin-bottom: 16px; }
      .modal-actions { display: flex; gap: 8px; justify-content: flex-end; margin-top: 20px; }

      /* Empty State */
      .empty-state { text-align: center; padding: 40px; color: var(--text2); }
      .empty-state-icon { font-size: 48px; margin-bottom: 16px; }

      /* Help */
      .help-section { margin-bottom: 20px; }
      .help-section h3 { font-size: 15px; margin: 0 0 8px 0; color: var(--text); }
      .help-section p, .help-section li { font-size: 13px; color: var(--text2); line-height: 1.6; }
      .help-section code {
        background: rgba(0,0,0,0.05);
        padding: 2px 6px;
        border-radius: 4px;
        font-family: monospace;
        font-size: 12px;
      }
      .help-section pre {
        background: rgba(0,0,0,0.05);
        padding: 12px;
        border-radius: 8px;
        overflow-x: auto;
        font-size: 11px;
        font-family: monospace;
      }
    `;
  }

  render() {
    return html`
      <!-- Header mit Logo -->
      <div class="header">
        <img src="/notify_manager_static/images/logo.png" alt="Logo" class="header-logo">
        <div class="header-info">
          <h1 class="header-title">Notify Manager</h1>
          <div class="header-version">v1.2.3.1 • ${this._getDevices().length} Geräte • ${this._getServiceCount()} Services</div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="tabs">
        <button class="tab ${this._tab === 'send' ? 'active' : ''}" @click=${() => this._tab = 'send'}>📤 Senden</button>
        <button class="tab ${this._tab === 'devices' ? 'active' : ''}" @click=${() => this._tab = 'devices'}>📱 Geräte</button>
        <button class="tab ${this._tab === 'categories' ? 'active' : ''}" @click=${() => this._tab = 'categories'}>🏷️ Kategorien</button>
        <button class="tab ${this._tab === 'templates' ? 'active' : ''}" @click=${() => this._tab = 'templates'}>📋 Vorlagen</button>
        <button class="tab ${this._tab === 'groups' ? 'active' : ''}" @click=${() => this._tab = 'groups'}>👥 Gruppen</button>
        <button class="tab ${this._tab === 'help' ? 'active' : ''}" @click=${() => this._tab = 'help'}>❓ Hilfe</button>
      </div>

      <!-- Tab Content -->
      ${this._tab === 'send' ? this._renderSendTab() : ''}
      ${this._tab === 'devices' ? this._renderDevicesTab() : ''}
      ${this._tab === 'categories' ? this._renderCategoriesTab() : ''}
      ${this._tab === 'templates' ? this._renderTemplatesTab() : ''}
      ${this._tab === 'groups' ? this._renderGroupsTab() : ''}
      ${this._tab === 'help' ? this._renderHelpTab() : ''}

      <!-- Modals -->
      ${this._editingTemplate ? this._renderTemplateModal() : ''}
      ${this._editingGroup ? this._renderGroupModal() : ''}
    `;
  }

  // ==================== DEVICES TAB ====================
  _renderDevicesTab() {
    const devices = this._getDevices();
    const sensors = this._getSensors();

    return html`
      <!-- Statistiken -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value">${devices.length}</div>
          <div class="stat-label">Geräte</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">${this._getServiceCount()}</div>
          <div class="stat-label">Services</div>
        </div>
        ${sensors.map(s => html`
          <div class="stat-card">
            <div class="stat-value">${this.hass.states[s]?.state || '0'}</div>
            <div class="stat-label">${this.hass.states[s]?.attributes?.friendly_name?.replace('Notify Manager ', '') || s}</div>
          </div>
        `)}
      </div>

      <!-- Verbundene Geräte -->
      <div class="card">
        <div class="card-title">📱 Verbundene Geräte</div>
        <div class="device-selector">
          ${devices.map(d => html`
            <div class="device-chip selected">
              ${d.toLowerCase().includes('iphone') || d.toLowerCase().includes('ipad') ? '📱' : '🤖'} 
              ${d}
            </div>
          `)}
        </div>
        ${!devices.length ? html`<p style="color: var(--text2);">Keine Companion App Geräte gefunden.</p>` : ''}
      </div>
    `;
  }

  // ==================== CATEGORIES TAB ====================
  _renderCategoriesTab() {
    const switches = this._getSwitches();
    const masterSwitch = switches.find(s => s.includes('alle_benachrichtigungen') || s.includes('all_notifications'));
    const categorySwitches = switches.filter(s => s !== masterSwitch);

    const categoryIcons = {
      'alarm': '🚨',
      'sicherheit': '🔒',
      'security': '🔒',
      'bewegung': '🏃',
      'motion': '🏃',
      'tuerklingel': '🚪',
      'doorbell': '🚪',
      'system': '⚙️',
      'information': 'ℹ️',
      'info': 'ℹ️',
      'klima': '🌡️',
      'climate': '🌡️',
    };

    const getIcon = (entityId) => {
      for (const [key, icon] of Object.entries(categoryIcons)) {
        if (entityId.toLowerCase().includes(key)) return icon;
      }
      return '🏷️';
    };

    return html`
      <div class="card">
        <div class="card-title">🎛️ Steuerelemente</div>
        
        <div class="switch-list">
          <!-- Master Switch -->
          ${masterSwitch ? html`
            <div class="switch-item master">
              <div class="switch-info">
                <div class="switch-icon">🔔</div>
                <div class="switch-name">Alle Benachrichtigungen</div>
              </div>
              <div class="switch-toggle ${this.hass.states[masterSwitch]?.state === 'on' ? 'on' : ''}"
                   @click=${() => this._toggleSwitch(masterSwitch)}></div>
            </div>
          ` : ''}

          <!-- Category Switches -->
          ${categorySwitches.map(s => html`
            <div class="switch-item">
              <div class="switch-info">
                <div class="switch-icon" style="background: ${this.hass.states[s]?.state === 'on' ? 'var(--accent)' : '#999'}">
                  ${getIcon(s)}
                </div>
                <div class="switch-name">
                  ${this.hass.states[s]?.attributes?.friendly_name?.replace('Notify Manager ', '').replace('Kategorie: ', '') || s}
                </div>
              </div>
              <div class="switch-toggle ${this.hass.states[s]?.state === 'on' ? 'on' : ''}"
                   @click=${() => this._toggleSwitch(s)}></div>
            </div>
          `)}
        </div>

        ${!switches.length ? html`<p style="color: var(--text2);">Keine Schalter gefunden.</p>` : ''}
      </div>
    `;
  }

  // ==================== SEND TAB ====================
  _renderSendTab() {
    const devices = this._getDevices();
    const cameras = Object.keys(this.hass?.states || {}).filter(e => e.startsWith('camera.'));

    return html`
      <div class="card">
        <div class="card-title">📨 Schnell-Benachrichtigung</div>

        <!-- Vorlagen -->
        <div class="form-group">
          <label>Vorlage verwenden</label>
          <div class="type-selector">
            ${this._templates.map(t => html`
              <div class="type-btn" @click=${() => this._applyTemplate(t)}>${t.name}</div>
            `)}
          </div>
        </div>

        <!-- Empfänger -->
        <div class="form-group">
          <label>Empfänger</label>
          <div class="device-selector">
            <div class="device-chip ${this._selectedDevices.length === 0 && !this._selectedGroup ? 'selected' : ''}" 
                 @click=${() => { this._selectedDevices = []; this._selectedGroup = ''; }}>
              📱 Alle Geräte
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
                ${d.toLowerCase().includes('iphone') || d.toLowerCase().includes('ipad') ? '📱' : '🤖'} ${d}
              </div>
            `)}
          </div>
        </div>

        <!-- Typ -->
        <div class="form-group">
          <label>Benachrichtigungstyp</label>
          <div class="type-selector">
            <button class="type-btn ${this._type === 'simple' ? 'active' : ''}" @click=${() => this._type = 'simple'}>📱 Einfach</button>
            <button class="type-btn ${this._type === 'buttons' ? 'active' : ''}" @click=${() => this._type = 'buttons'}>🔘 Mit Buttons</button>
            <button class="type-btn ${this._type === 'image' ? 'active' : ''}" @click=${() => this._type = 'image'}>📷 Mit Kamera</button>
            <button class="type-btn ${this._type === 'tts' ? 'active' : ''}" @click=${() => this._type = 'tts'}>🔊 TTS</button>
          </div>
        </div>

        <!-- Titel & Priorität -->
        <div class="row">
          <div class="form-group">
            <label>Titel</label>
            <input type="text" .value=${this._title} @input=${(e) => this._title = e.target.value} placeholder="z.B. Home Assistant">
          </div>
          <div class="form-group">
            <label>Priorität</label>
            <select .value=${this._priority} @change=${(e) => this._priority = e.target.value}>
              <option value="low">🔇 Leise</option>
              <option value="normal">📱 Normal</option>
              <option value="high">🔔 Wichtig</option>
              <option value="critical">🚨 Kritisch</option>
            </select>
          </div>
        </div>

        <!-- Nachricht -->
        <div class="form-group">
          <label>${this._type === 'tts' ? 'Text zum Vorlesen' : 'Nachricht'}</label>
          <textarea .value=${this._message} @input=${(e) => this._message = e.target.value}
                    placeholder="${this._type === 'tts' ? 'Was soll vorgelesen werden?' : 'Deine Nachricht...'}"></textarea>
        </div>

        <!-- Kamera -->
        ${this._type === 'image' ? html`
          <div class="form-group">
            <label>Kamera</label>
            <select .value=${this._camera} @change=${(e) => this._camera = e.target.value}>
              <option value="">-- Kamera wählen --</option>
              ${cameras.map(c => html`<option value="${c}">${this.hass.states[c]?.attributes?.friendly_name || c}</option>`)}
            </select>
          </div>
        ` : ''}

        <!-- Buttons -->
        ${this._type === 'buttons' ? html`
          <div class="form-group">
            <label>Button-Vorlage wählen</label>
            <div class="type-selector" style="margin-bottom: 12px;">
              <div class="type-btn ${this._buttons.length === 0 ? 'active' : ''}" @click=${() => this._buttons = []}>Keine</div>
              <div class="type-btn" @click=${() => this._applyButtonTemplate('confirm_dismiss')}>✅ Bestätigen/Ablehnen</div>
              <div class="type-btn" @click=${() => this._applyButtonTemplate('yes_no')}>👍 Ja/Nein</div>
              <div class="type-btn" @click=${() => this._applyButtonTemplate('alarm_response')}>🚨 Alarm</div>
              <div class="type-btn" @click=${() => this._applyButtonTemplate('door_response')}>🚪 Tür</div>
              <div class="type-btn" @click=${() => this._applyButtonTemplate('reply')}>💬 Antwort</div>
            </div>
            <label>Buttons <span style="font-weight: normal; color: var(--text2);">(können angepasst werden)</span></label>
            <div class="button-list">
              ${this._buttons.map((btn, i) => html`
                <div class="button-item">
                  <input type="text" placeholder="Action ID (z.B. CONFIRM)" .value=${btn.action} @input=${(e) => this._updateButton(i, 'action', e.target.value)}>
                  <input type="text" placeholder="Button Text" .value=${btn.title} @input=${(e) => this._updateButton(i, 'title', e.target.value)}>
                  <button class="btn btn-danger btn-icon" @click=${() => this._removeButton(i)}>✕</button>
                </div>
              `)}
              <button class="btn btn-success btn-small" @click=${this._addButton}>+ Button hinzufügen</button>
            </div>
          </div>
        ` : ''}

        <!-- Vorschau -->
        <div class="preview">
          <div class="preview-title">📱 Vorschau</div>
          <div class="preview-notification">
            <div class="preview-header">
              <div class="preview-icon"></div>
              <span class="preview-app">HOME ASSISTANT</span>
            </div>
            <div class="preview-t">${this._title || 'Titel'}</div>
            <div class="preview-m">${this._message || 'Nachricht...'}</div>
            ${this._type === 'buttons' && this._buttons.length ? html`
              <div class="preview-buttons">
                ${this._buttons.map(b => html`<div class="preview-btn">${b.title || 'Button'}</div>`)}
              </div>
            ` : ''}
          </div>
        </div>

        <!-- Als Vorlage speichern -->
        <div style="margin-top: 12px;">
          <button class="btn btn-outline" @click=${this._saveAsTemplate}>💾 Als Vorlage speichern</button>
        </div>

        <!-- Senden -->
        <button class="send-btn" style="margin-top: 16px;" @click=${this._send} ?disabled=${this._loading || !this._message}>
          ${this._loading ? '⏳ Sende...' : '📤 Benachrichtigung senden'}
        </button>
        ${this._success ? html`<div class="${this._success.startsWith('❌') ? 'error-msg' : 'success-msg'}">${this._success}</div>` : ''}
      </div>
    `;
  }

  // ==================== TEMPLATES TAB ====================
  _renderTemplatesTab() {
    return html`
      <div class="card">
        <div class="card-title">
          <span>📋 Vorlagen verwalten</span>
          <button class="btn btn-primary btn-small" @click=${() => this._editingTemplate = { id: '', name: '', title: '', message: '', type: 'simple', priority: 'normal', buttons: [] }}>
            + Neue Vorlage
          </button>
        </div>

        ${this._templates.length ? html`
          <div class="template-grid">
            ${this._templates.map(t => html`
              <div class="template-card">
                <div class="template-name">${t.name}</div>
                <div class="template-preview">${t.title}: ${t.message?.substring(0, 40)}${t.message?.length > 40 ? '...' : ''}</div>
                <div class="template-preview">Typ: ${t.type} | Priorität: ${t.priority}</div>
                <div class="template-actions">
                  <button class="btn btn-primary btn-small" @click=${() => this._applyTemplateAndSwitch(t)}>Verwenden</button>
                  <button class="btn btn-outline btn-small" @click=${() => this._editingTemplate = {...t, buttons: [...(t.buttons || [])]}}>✏️</button>
                  <button class="btn btn-danger btn-small" @click=${() => this._deleteTemplate(t.id)}>🗑️</button>
                </div>
              </div>
            `)}
          </div>
        ` : html`
          <div class="empty-state">
            <div class="empty-state-icon">📋</div>
            <p>Noch keine eigenen Vorlagen erstellt.</p>
            <button class="btn btn-primary" @click=${() => this._editingTemplate = { id: '', name: '', title: '', message: '', type: 'simple', priority: 'normal', buttons: [] }}>
              Erste Vorlage erstellen
            </button>
          </div>
        `}
      </div>
    `;
  }

  // ==================== GROUPS TAB ====================
  _renderGroupsTab() {
    const devices = this._getDevices();

    return html`
      <div class="card">
        <div class="card-title">
          <span>👥 Gerätegruppen</span>
          <button class="btn btn-primary btn-small" @click=${() => this._editingGroup = { id: '', name: '', devices: [] }}>
            + Neue Gruppe
          </button>
        </div>

        <p style="color: var(--text2); font-size: 13px; margin-bottom: 16px;">
          Erstelle Gruppen um Benachrichtigungen an mehrere Geräte gleichzeitig zu senden.
        </p>

        ${this._groups.length ? html`
          <div class="group-grid">
            ${this._groups.map(g => html`
              <div class="group-card">
                <div class="group-name">👥 ${g.name}</div>
                <div class="group-info">${g.devices?.length || 0} Gerät(e): ${g.devices?.join(', ') || 'Keine'}</div>
                <div class="group-actions">
                  <button class="btn btn-outline btn-small" @click=${() => this._editingGroup = {...g, devices: [...(g.devices || [])]}}>✏️ Bearbeiten</button>
                  <button class="btn btn-danger btn-small" @click=${() => this._deleteGroup(g.id)}>🗑️</button>
                </div>
              </div>
            `)}
          </div>
        ` : html`
          <div class="empty-state">
            <div class="empty-state-icon">👥</div>
            <p>Noch keine Gruppen erstellt.</p>
            <button class="btn btn-primary" @click=${() => this._editingGroup = { id: '', name: '', devices: [] }}>
              Erste Gruppe erstellen
            </button>
          </div>
        `}
      </div>

      <div class="card">
        <div class="card-title">📱 Verfügbare Geräte für Gruppen</div>
        <div class="device-selector">
          ${devices.map(d => html`
            <div class="device-chip">
              ${d.toLowerCase().includes('iphone') || d.toLowerCase().includes('ipad') ? '📱' : '🤖'} ${d}
            </div>
          `)}
        </div>
        ${!devices.length ? html`<p style="color: var(--text2);">Keine Geräte gefunden.</p>` : ''}
      </div>
    `;
  }

  // ==================== HELP TAB ====================
  _renderHelpTab() {
    return html`
      <div class="card">
        <div class="card-title">❓ Hilfe & Dokumentation</div>
        
        <div class="help-section">
          <h3>🚀 Schnellstart</h3>
          <p>1. Wähle im <strong>Senden</strong>-Tab Empfänger und Typ<br>
             2. Gib Titel und Nachricht ein<br>
             3. Klicke auf <strong>Senden</strong></p>
        </div>

        <div class="help-section">
          <h3>📋 Vorlagen</h3>
          <p>Speichere häufig genutzte Benachrichtigungen als Vorlage. Diese erscheinen dann als Schnell-Buttons im Senden-Tab.</p>
        </div>

        <div class="help-section">
          <h3>👥 Gruppen</h3>
          <p>Erstelle Gerätegruppen wie "Familie" oder "Alle iPhones" um mehrere Geräte gleichzeitig zu benachrichtigen.</p>
        </div>

        <div class="help-section">
          <h3>🔄 Auf Buttons reagieren</h3>
          <pre>trigger:
  - platform: event
    event_type: mobile_app_notification_action
    event_data:
      action: "DEINE_ACTION_ID"</pre>
        </div>

        <div class="help-section">
          <h3>📲 Verfügbare Services</h3>
          <ul>
            <li><code>send_notification</code> - Einfach</li>
            <li><code>send_actionable</code> - Mit Buttons</li>
            <li><code>send_with_image</code> - Mit Kamera</li>
            <li><code>send_tts</code> - Text vorlesen</li>
            <li><code>send_progress</code> - Fortschrittsbalken</li>
            <li><code>device_command</code> - Geräte steuern</li>
            <li><code>send_advanced</code> - Alle Optionen</li>
          </ul>
        </div>
      </div>
    `;
  }

  // ==================== MODALS ====================
  _renderTemplateModal() {
    const t = this._editingTemplate;
    return html`
      <div class="modal-overlay" @click=${(e) => { if(e.target === e.currentTarget) this._editingTemplate = null; }}>
        <div class="modal">
          <div class="modal-title">${t.id ? '✏️ Vorlage bearbeiten' : '📋 Neue Vorlage'}</div>
          
          <div class="form-group">
            <label>Vorlagen-Name (mit Emoji)</label>
            <input type="text" .value=${t.name} @input=${(e) => t.name = e.target.value} placeholder="z.B. 🚪 Türklingel">
          </div>
          
          <div class="row">
            <div class="form-group">
              <label>Titel</label>
              <input type="text" .value=${t.title} @input=${(e) => t.title = e.target.value}>
            </div>
            <div class="form-group">
              <label>Typ</label>
              <select .value=${t.type} @change=${(e) => { t.type = e.target.value; this.requestUpdate(); }}>
                <option value="simple">Einfach</option>
                <option value="buttons">Mit Buttons</option>
                <option value="image">Mit Kamera</option>
                <option value="tts">TTS</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>Nachricht</label>
            <textarea .value=${t.message} @input=${(e) => t.message = e.target.value}></textarea>
          </div>

          <div class="form-group">
            <label>Priorität</label>
            <select .value=${t.priority} @change=${(e) => t.priority = e.target.value}>
              <option value="low">Leise</option>
              <option value="normal">Normal</option>
              <option value="high">Wichtig</option>
              <option value="critical">Kritisch</option>
            </select>
          </div>

          ${t.type === 'buttons' ? html`
            <div class="form-group">
              <label>Buttons</label>
              <div class="button-list">
                ${(t.buttons || []).map((btn, i) => html`
                  <div class="button-item">
                    <input type="text" placeholder="Action ID" .value=${btn.action} @input=${(e) => { t.buttons[i].action = e.target.value; this.requestUpdate(); }}>
                    <input type="text" placeholder="Text" .value=${btn.title} @input=${(e) => { t.buttons[i].title = e.target.value; this.requestUpdate(); }}>
                    <button class="btn btn-danger btn-icon" @click=${() => { t.buttons.splice(i, 1); this.requestUpdate(); }}>✕</button>
                  </div>
                `)}
                <button class="btn btn-success btn-small" @click=${() => { t.buttons = [...(t.buttons || []), {action: '', title: ''}]; this.requestUpdate(); }}>+ Button</button>
              </div>
            </div>
          ` : ''}

          <div class="modal-actions">
            <button class="btn btn-outline" @click=${() => this._editingTemplate = null}>Abbrechen</button>
            <button class="btn btn-primary" @click=${() => this._saveTemplate(t)}>💾 Speichern</button>
          </div>
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
          <div class="modal-title">${g.id ? '✏️ Gruppe bearbeiten' : '👥 Neue Gruppe'}</div>
          
          <div class="form-group">
            <label>Gruppen-Name</label>
            <input type="text" .value=${g.name} @input=${(e) => g.name = e.target.value} placeholder="z.B. Familie">
          </div>

          <div class="form-group">
            <label>Geräte auswählen (klicken zum Hinzufügen/Entfernen)</label>
            <div class="device-selector">
              ${devices.map(d => html`
                <div class="device-chip ${(g.devices || []).includes(d) ? 'selected' : ''}"
                     @click=${() => { 
                       g.devices = g.devices || [];
                       if(g.devices.includes(d)) g.devices = g.devices.filter(x => x !== d);
                       else g.devices = [...g.devices, d];
                       this.requestUpdate();
                     }}>
                  ${d.toLowerCase().includes('iphone') || d.toLowerCase().includes('ipad') ? '📱' : '🤖'} ${d}
                </div>
              `)}
            </div>
          </div>

          <div class="modal-actions">
            <button class="btn btn-outline" @click=${() => this._editingGroup = null}>Abbrechen</button>
            <button class="btn btn-primary" @click=${() => this._saveGroup(g)}>💾 Speichern</button>
          </div>
        </div>
      </div>
    `;
  }

  // ==================== HELPERS ====================
  _getDevices() {
    return Object.keys(this.hass?.services?.notify || {})
      .filter(s => s.startsWith('mobile_app_'))
      .map(s => s.replace('mobile_app_', ''));
  }

  _getSwitches() {
    return Object.keys(this.hass?.states || {})
      .filter(e => e.startsWith('switch.notify_manager'));
  }

  _getSensors() {
    return Object.keys(this.hass?.states || {})
      .filter(e => e.startsWith('sensor.notify_manager'));
  }

  _getServiceCount() {
    return Object.keys(this.hass?.services?.notify_manager || {}).length;
  }

  _toggleSwitch(entityId) {
    this.hass.callService('switch', 'toggle', { entity_id: entityId });
  }

  _toggleDevice(device) {
    this._selectedGroup = '';
    if (this._selectedDevices.includes(device)) {
      this._selectedDevices = this._selectedDevices.filter(d => d !== device);
    } else {
      this._selectedDevices = [...this._selectedDevices, device];
    }
  }

  _applyTemplate(t) {
    this._title = t.title || '';
    this._message = t.message || '';
    this._type = t.type || 'simple';
    this._priority = t.priority || 'normal';
    this._buttons = [...(t.buttons || [])];
  }

  _applyTemplateAndSwitch(t) {
    this._applyTemplate(t);
    this._tab = 'send';
  }

  _applyButtonTemplate(templateName) {
    const buttonTemplates = {
      confirm_dismiss: [
        { action: 'CONFIRM', title: '✅ Bestätigen' },
        { action: 'DISMISS', title: '❌ Ablehnen' }
      ],
      yes_no: [
        { action: 'YES', title: '👍 Ja' },
        { action: 'NO', title: '👎 Nein' }
      ],
      alarm_response: [
        { action: 'ALARM_CONFIRM', title: '✅ Alles OK' },
        { action: 'ALARM_SNOOZE', title: '⏰ Später' },
        { action: 'ALARM_EMERGENCY', title: '🆘 Notfall!' }
      ],
      door_response: [
        { action: 'DOOR_UNLOCK', title: '🔓 Öffnen' },
        { action: 'DOOR_IGNORE', title: '🚪 Ignorieren' },
        { action: 'DOOR_SPEAK', title: '🔊 Sprechen' }
      ],
      reply: [
        { action: 'REPLY', title: '💬 Antworten', behavior: 'textInput', textInputButtonTitle: 'Senden', textInputPlaceholder: 'Nachricht...' }
      ]
    };
    
    this._buttons = [...(buttonTemplates[templateName] || [])];
  }

  _addButton() { this._buttons = [...this._buttons, { action: "", title: "" }]; }
  _removeButton(i) { this._buttons = this._buttons.filter((_, idx) => idx !== i); }
  _updateButton(i, field, value) { this._buttons = this._buttons.map((btn, idx) => idx === i ? { ...btn, [field]: value } : btn); }

  _saveAsTemplate() {
    const name = prompt("Name für die Vorlage (mit Emoji):", this._title || "📝 Neue Vorlage");
    if (!name) return;
    
    const newTemplate = {
      id: 'tpl_' + Date.now(),
      name,
      title: this._title,
      message: this._message,
      type: this._type,
      priority: this._priority,
      buttons: [...this._buttons]
    };
    
    this._templates = [...this._templates, newTemplate];
    this._saveToStorage("notify_manager_templates", this._templates);
    this._success = "✅ Vorlage gespeichert!";
    setTimeout(() => this._success = "", 3000);
  }

  _saveTemplate(t) {
    if (!t.name) { alert("Bitte Namen eingeben"); return; }
    
    if (t.id) {
      this._templates = this._templates.map(x => x.id === t.id ? {...t} : x);
    } else {
      t.id = 'tpl_' + Date.now();
      this._templates = [...this._templates, {...t}];
    }
    
    this._saveToStorage("notify_manager_templates", this._templates);
    this._editingTemplate = null;
  }

  _deleteTemplate(id) {
    if (!confirm("Vorlage wirklich löschen?")) return;
    this._templates = this._templates.filter(t => t.id !== id);
    this._saveToStorage("notify_manager_templates", this._templates);
  }

  _saveGroup(g) {
    if (!g.name) { alert("Bitte Namen eingeben"); return; }
    if (!g.devices?.length) { alert("Bitte mindestens ein Gerät auswählen"); return; }
    
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
    if (!confirm("Gruppe wirklich löschen?")) return;
    this._groups = this._groups.filter(g => g.id !== id);
    this._saveToStorage("notify_manager_groups", this._groups);
  }

  async _send() {
    if (!this._message) return;
    this._loading = true;
    this._success = "";

    try {
      let service = "send_notification";
      let data = { title: this._title || "Home Assistant", message: this._message, priority: this._priority };

      // Zielgeräte
      let targets = [];
      if (this._selectedGroup) {
        const group = this._groups.find(g => g.id === this._selectedGroup);
        if (group) targets = group.devices;
      } else if (this._selectedDevices.length) {
        targets = this._selectedDevices;
      }
      if (targets.length) data.target = targets;

      if (this._type === "buttons" && this._buttons.length) {
        service = "send_actionable";
        data.actions = this._buttons.filter(b => b.action && b.title);
      } else if (this._type === "image" && this._camera) {
        service = "send_with_image";
        data.camera_entity = this._camera;
      } else if (this._type === "tts") {
        service = "send_tts";
        data = { tts_text: this._message, media_stream: this._priority === "critical" ? "alarm_stream_max" : "music_stream" };
        if (targets.length) data.target = targets;
      }

      await this.hass.callService("notify_manager", service, data);
      this._success = "✅ Benachrichtigung gesendet!";
      setTimeout(() => this._success = "", 3000);
    } catch (err) {
      console.error("Send error:", err);
      this._success = "❌ Fehler: " + err.message;
    } finally {
      this._loading = false;
    }
  }
}

customElements.define("notify-manager-panel", NotifyManagerPanel);
