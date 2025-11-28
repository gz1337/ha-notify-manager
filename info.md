{% if installed %}

<p align="center">
  <img src="https://raw.githubusercontent.com/gz1337/ha-notify-manager/main/icon.png" alt="Notify Manager" width="120">
</p>

## Änderungen in dieser Version

### v{{ version_installed }}

{% if version_installed.replace("v", "").replace(".","") | int < 100 %}
- Erste Veröffentlichung
- Vollständiges Panel mit Übersicht, Kategorien, Test und Verlauf
- Services: send_notification, send_actionable, clear_notifications
- Switches für Kategorien und Master-Schalter
- Sensoren für Statistiken
{% endif %}

---

{% endif %}

## Features

- 🔔 **Zentrale Benachrichtigungsverwaltung** - Alle Mobile App Benachrichtigungen an einem Ort
- 📱 **Multi-Device Support** - Sende an mehrere Geräte gleichzeitig
- 🏷️ **Kategorien** - Alarm, Sicherheit, Türklingel, Bewegung, System, Info
- ⚡ **Prioritätsstufen** - Low, Normal, High, Critical
- 🎛️ **Eigenes Panel** - Vollständige UI im Sidebar
- 🔘 **Aktions-Benachrichtigungen** - Interaktive Buttons
- 📊 **Statistiken** - Übersicht gesendeter Benachrichtigungen

## Schnellstart

1. Installation über HACS
2. Home Assistant neustarten
3. Integration unter Einstellungen → Geräte & Dienste hinzufügen
4. Geräte und Kategorien konfigurieren
5. "Notify Manager" im Sidebar nutzen

## Beispiel

```yaml
service: notify_manager.send_actionable
data:
  title: "🔒 Alarmanlage"
  message: "Alarm ausgelöst!"
  category: alarm
  actions:
    - action: "CONFIRM"
      title: "Bestätigen"
    - action: "DISMISS"
      title: "Abbrechen"
```
