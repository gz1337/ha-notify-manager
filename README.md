# Notify Manager for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/your-username/ha-notify-manager.svg)](https://github.com/your-username/ha-notify-manager/releases)
[![License](https://img.shields.io/github/license/your-username/ha-notify-manager.svg)](LICENSE)

Eine umfassende Benachrichtigungsverwaltung für die **Home Assistant Companion App** (iOS & Android) mit eigenem Frontend-Panel, Kategorien, Prioritäten, Actionable Notifications und vollständiger UI-Konfiguration.

![Notify Manager Screenshot](images/screenshot.png)

## Features

- 🔔 **Zentrale Benachrichtigungsverwaltung** - Verwalte alle Companion App Benachrichtigungen
- 📱 **iOS & Android Support** - Volle Unterstützung für beide Plattformen
- 🎛️ **Actionable Notifications** - Interaktive Buttons direkt in der Benachrichtigung
- 🚨 **Kritische Benachrichtigungen** - Durchbrechen Nicht-Stören-Modus (iOS)
- 📷 **Kamera-Integration** - Sende Snapshots von Kameras
- 💬 **Text-Eingabe** - Benutzer können auf Benachrichtigungen antworten
- 🏷️ **Kategorien** - Organisiere in Alarm, Sicherheit, Türklingel, etc.
- ⚡ **Prioritätsstufen** - Low, Normal, High und Critical
- 🎛️ **Eigenes Panel** - Vollständige UI im Home Assistant Sidebar
- 📊 **Verlauf & Statistiken** - Übersicht aller gesendeten Benachrichtigungen
- 🔄 **Callback-Handling** - Reagiere auf Button-Klicks in Automationen
- 🌐 **Mehrsprachig** - Deutsch und Englisch

## Installation

### HACS (Empfohlen)

1. Öffne HACS in Home Assistant
2. Klicke auf "Integrationen"
3. Klicke auf die drei Punkte oben rechts und wähle "Benutzerdefinierte Repositories"
4. Füge `(https://github.com/gz1337/ha-notification)` als Repository hinzu
5. Wähle "Integration" als Kategorie
6. Klicke auf "Hinzufügen"
7. Suche nach "Notify Manager" und installiere es
8. Starte Home Assistant neu

### Manuelle Installation

1. Kopiere den Ordner `custom_components/notify_manager` in deinen `config/custom_components` Ordner
2. Starte Home Assistant neu

## Konfiguration

1. Gehe zu **Einstellungen** → **Geräte & Dienste**
2. Klicke auf **+ Integration hinzufügen**
3. Suche nach "Notify Manager"
4. Folge dem Einrichtungsassistenten:
   - Wähle die Geräte, die Benachrichtigungen erhalten sollen
   - Aktiviere/Deaktiviere Kategorien
   - Setze die Standard-Priorität

## Verwendung

### Panel

Nach der Installation erscheint "Notify Manager" in der Sidebar. Das Panel bietet:

- **Übersicht** - Status, verbundene Geräte, Schnellaktionen
- **Kategorien** - Ein/Aus-Schalter für jede Kategorie
- **Test** - Sende Test-Benachrichtigungen
- **Verlauf** - Übersicht der gesendeten Benachrichtigungen

### Services

#### `notify_manager.send_notification`

Sendet eine einfache Benachrichtigung an konfigurierte Geräte.

```yaml
service: notify_manager.send_notification
data:
  title: "Home Assistant"
  message: "Willkommen zu Hause!"
  category: info
  priority: normal
  tag: welcome_home
```

#### `notify_manager.send_actionable`

Sendet eine Benachrichtigung mit interaktiven Buttons.

```yaml
service: notify_manager.send_actionable
data:
  title: "🔒 Alarmanlage"
  message: "Alarm wurde ausgelöst. Was möchtest du tun?"
  category: alarm
  priority: critical
  persistent: true
  sticky: true
  actions:
    - action: "ALARM_CONFIRM"
      title: "Alles OK"
      icon: "sfsymbols:checkmark.shield"
    - action: "ALARM_SNOOZE"
      title: "Später erinnern"
    - action: "ALARM_EMERGENCY"
      title: "Notfall!"
      destructive: true
  tag: alarm_action
```

#### `notify_manager.send_with_image`

Sendet eine Benachrichtigung mit Bild oder Kamera-Snapshot.

```yaml
service: notify_manager.send_with_image
data:
  title: "📷 Bewegung erkannt"
  message: "Bewegung an der Haustür"
  camera_entity: camera.haustuer
  category: doorbell
  priority: high
  actions:
    - action: "DOOR_OPEN"
      title: "Tür öffnen"
    - action: "DOOR_IGNORE"
      title: "Ignorieren"
```

#### `notify_manager.send_alarm_confirmation`

Sendet eine vorkonfigurierte Alarm-Benachrichtigung mit Standard-Buttons.

```yaml
service: notify_manager.send_alarm_confirmation
data:
  title: "🚨 ALARM"
  message: "Alarmanlage wurde ausgelöst!"
  template: alarm_response  # oder: confirm_dismiss, door_response, yes_no
  alarm_entity: alarm_control_panel.home_alarm
```

#### `notify_manager.send_text_input`

Sendet eine Benachrichtigung bei der der Benutzer antworten kann.

```yaml
service: notify_manager.send_text_input
data:
  title: "💬 Einkaufsliste"
  message: "Was soll ich noch einkaufen?"
  input_title: "Antworten"
  placeholder: "z.B. Milch, Brot..."
```

#### `notify_manager.clear_notifications`

Löscht Benachrichtigungen auf den Geräten.

```yaml
service: notify_manager.clear_notifications
data:
  tag: alarm_action  # Optional: nur bestimmte Tags löschen
```

### Entitäten

Die Integration erstellt folgende Entitäten:

**Switches:**
- `switch.notify_manager_alle_benachrichtigungen` - Master-Schalter
- `switch.notify_manager_kategorie_alarm` - Alarm-Kategorie
- `switch.notify_manager_kategorie_sicherheit` - Sicherheits-Kategorie
- etc.

**Sensoren:**
- `sensor.notify_manager_gesendete_benachrichtigungen` - Anzahl gesendeter Nachrichten
- `sensor.notify_manager_benachrichtigungen_heute` - Heute gesendet
- `sensor.notify_manager_aktive_kategorien` - Anzahl aktiver Kategorien

### Automatisierungen

#### Auf Button-Klicks reagieren

Die Companion App sendet ein Event `mobile_app_notification_action` wenn ein Button geklickt wird. Notify Manager feuert zusätzlich ein `notify_manager_action_received` Event.

```yaml
automation:
  # Methode 1: Standard mobile_app Event
  - alias: "Alarm - Button-Reaktion"
    trigger:
      - platform: event
        event_type: mobile_app_notification_action
        event_data:
          action: "ALARM_CONFIRM"
    action:
      - service: alarm_control_panel.alarm_disarm
        target:
          entity_id: alarm_control_panel.home_alarm
      - service: notify_manager.send_notification
        data:
          title: "✅ Bestätigt"
          message: "Alarm wurde deaktiviert."
          priority: normal

  # Methode 2: Notify Manager Event
  - alias: "Alarm - Notfall Button"
    trigger:
      - platform: event
        event_type: notify_manager_action_received
        event_data:
          action: "ALARM_EMERGENCY"
    action:
      - service: notify.persistent_notification
        data:
          title: "🚨 NOTFALL"
          message: "Notfall-Button wurde gedrückt!"
      # Hier weitere Notfall-Aktionen
```

#### Türklingel mit Kamera-Bild und Buttons

```yaml
automation:
  - alias: "Türklingel - Benachrichtigung mit Kamera"
    trigger:
      - platform: state
        entity_id: binary_sensor.doorbell_button
        to: "on"
    action:
      - service: notify_manager.send_with_image
        data:
          title: "🔔 Türklingel"
          message: "Jemand steht an der Tür!"
          camera_entity: camera.doorbell
          category: doorbell
          priority: high
          tag: doorbell_ring
          actions:
            - action: "DOOR_UNLOCK"
              title: "🔓 Tür öffnen"
            - action: "DOOR_SPEAK"
              title: "🎤 Sprechen"
            - action: "DOOR_IGNORE"
              title: "Ignorieren"

  - alias: "Türklingel - Tür öffnen"
    trigger:
      - platform: event
        event_type: mobile_app_notification_action
        event_data:
          action: "DOOR_UNLOCK"
    action:
      - service: lock.unlock
        target:
          entity_id: lock.haustuer
      - service: notify_manager.clear_notifications
        data:
          tag: doorbell_ring
```

#### Alarm-System Integration

```yaml
automation:
  - alias: "Alarmanlage - Bestätigung anfragen"
    trigger:
      - platform: state
        entity_id: alarm_control_panel.home_alarm
        to: "triggered"
    action:
      - service: notify_manager.send_alarm_confirmation
        data:
          title: "🚨 ALARM AUSGELÖST"
          message: >
            Alarm wurde ausgelöst um {{ now().strftime('%H:%M') }}!
            Sensor: {{ trigger.to_state.attributes.changed_by }}
          template: alarm_response
          alarm_entity: alarm_control_panel.home_alarm

  - alias: "Alarmanlage - Snooze"
    trigger:
      - platform: event
        event_type: mobile_app_notification_action
        event_data:
          action: "ALARM_SNOOZE"
    action:
      - delay: "00:05:00"
      - service: notify_manager.send_alarm_confirmation
        data:
          title: "🔔 Alarm Erinnerung"
          message: "Der Alarm ist immer noch aktiv!"
          template: alarm_response
```

#### Text-Eingabe verarbeiten

```yaml
automation:
  - alias: "Einkaufsliste - Fragen"
    trigger:
      - platform: time
        at: "17:00:00"
    condition:
      - condition: time
        weekday:
          - sat
    action:
      - service: notify_manager.send_text_input
        data:
          title: "🛒 Einkaufsliste"
          message: "Was brauchst du noch vom Supermarkt?"
          input_title: "Hinzufügen"
          placeholder: "z.B. Milch, Brot..."
          tag: shopping_list

  - alias: "Einkaufsliste - Antwort verarbeiten"
    trigger:
      - platform: event
        event_type: mobile_app_notification_action
        event_data:
          action: "REPLY"
    action:
      - service: shopping_list.add_item
        data:
          name: "{{ trigger.event.data.reply_text }}"
      - service: notify_manager.send_notification
        data:
          title: "✅ Hinzugefügt"
          message: "'{{ trigger.event.data.reply_text }}' wurde zur Liste hinzugefügt."
          priority: low
```

## Optionen

Nach der Einrichtung können unter **Einstellungen** → **Geräte & Dienste** → **Notify Manager** → **Konfigurieren** folgende Optionen angepasst werden:

- Geräte hinzufügen/entfernen
- Kategorien aktivieren/deaktivieren
- Prioritäten pro Kategorie setzen

## Fehlerbehebung

### Keine Geräte gefunden

Stelle sicher, dass:
1. Die Home Assistant Companion App auf deinem Gerät installiert ist
2. Die App mit Home Assistant verbunden ist
3. Benachrichtigungen in der App aktiviert sind

### Benachrichtigungen kommen nicht an

1. Prüfe, ob die Kategorie aktiviert ist
2. Prüfe den Master-Schalter
3. Schaue in die Home Assistant Logs

### Panel wird nicht angezeigt

1. Leere den Browser-Cache
2. Starte Home Assistant neu
3. Prüfe die Logs auf Fehler

## Beitragen

Beiträge sind willkommen! Bitte öffne ein Issue oder einen Pull Request auf GitHub.

## Lizenz

MIT License - siehe [LICENSE](LICENSE) Datei
