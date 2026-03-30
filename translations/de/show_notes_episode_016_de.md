# OpenClaw Daily – Folge 016

**Titel:** OpenClaw wirft seine Haut ab  
**Untertitel:** Der Deep Dive zur Doppelversion v2026.3.22 und v2026.3.23

## 1) Episodenzusammenfassung
In dieser Folge entpacken wir die aufeinanderfolgenden Versionen 2026.3.22 und 2026.3.23 von OpenClaw und konzentrieren uns dabei auf die wichtigsten Änderungen für Betreuer, Plugin-Entwickler und selbstgehostete Benutzer. Wir schlüsseln Migrationsdruckpunkte auf (insbesondere Plugin-SDK, Browser-Tools und Matrix-/Skill-Ökosysteme), was Probleme verursacht und was vor und nach dem Upgrade zu tun ist. Das Ziel ist ein saubererer, sichererer Plattformzustand mit weniger Laufzeitüberraschungen, besserem Authentifizierungs-/Proxy-Verhalten und saubereren Standardeinstellungen für Benutzeroberfläche, Modelle und Erweiterungsintegrationen.

## 2) Was wir abdecken
- Wirkungsvolle Highlights aus **v2026.3.22** und **v2026.3.23**
- Warum „openclaw doctor --fix“ zum Upgrade-Ankerbefehl wurde
– Details zur Browser-/Chrome-MCP-Migration und was sich für bestehende Sitzungsabläufe geändert hat
- Veränderungen im Plugin-Ökosystem: SDK-Migration, Laufzeitverhalten und Entfernung alter Kompatibilitätsebenen
- ClawHub-First-Plugin-Installation und Marktplatz-/Plugin-Kompatibilitätskorrekturen
- Anleitung zur Matrix-Plugin-Migration und Zuverlässigkeitskorrekturen
- Aktualisierungen der Barrierefreiheit und der Verfeinerung der Benutzeroberfläche (einschließlich WCAG-ausgerichteter Kontrastoptimierung)
- Änderungen am Qwen/DashScope-Anbieter und Bereinigung der Modellkonfiguration
- Praktische Upgrade-Sequenzierungs- und Verifizierungs-Checkliste

## 3) Links zu Versionshinweisen
- [OpenClaw v2026.3.22](https://github.com/openclaw/openclaw/releases/tag/v2026.3.22)
- [OpenClaw v2026.3.23](https://github.com/openclaw/openclaw/releases/tag/v2026.3.23)

## 4) Schlüsselthemen mit Links
- [`openclaw doctor --fix`](https://docs.openclaw.ai/gateway/doctor) – Migrations- und Reparatureinstiegspunkt für Umgebung, Plugins und bekannte Konfigurationsdrift
– [Browser/Chrome MCP](https://docs.openclaw.ai/tools/browser) – Aktualisierungen rund um die Browseranbindung bestehender Sitzungen und die Entfernung älterer Chrome-Erweiterungspfade
- [Plugin-SDK-Migration](https://docs.openclaw.ai/plugins/sdk-migration) – Ersetzen älterer Import-/Interop-Annahmen durch die neue SDK-Oberfläche
– [Plugin-SDK-Übersicht](https://docs.openclaw.ai/plugins/sdk-overview) – wie Plugin-Laufzeitgrenzen und APIs jetzt funktionieren sollen
- [Matrix-Migration](https://docs.openclaw.ai/install/migrating-matrix) – Upgrades für den neuen Matrix-Plugin-Stack erforderlich
- [ClawHub](https://docs.openclaw.ai/tools/clawhub) – neuer Standardablauf für Installation/Aktualisierung/Suche und Paketkompatibilität
- [OpenClaw-Migrationsleitfaden](https://docs.openclaw.ai/install/migrating) – umfassendere Grundlagen der Konfigurations-/Statusmigration
– [Qwen/DashScope (Model Studio)](https://www.alibabacloud.com/en/product/modelstudio) – Anbieteränderungen und Endpunktpfadaktualisierungen
– [WCAG 2.1 AA](https://www.w3.org/TR/WCAG21/) – Basislinie zur Barrierefreiheit für UI-Kontrast- und Steuerungsaktualisierungen in der Version

## 5) Upgrade-Checkliste (9 Schritte)
- [ ] **Sichern Sie Ihre aktuelle OpenClaw-Konfiguration/Ihren aktuellen OpenClaw-Status** vor Upgrades (einschließlich „.openclaw“ + jedem benutzerdefinierten Plugin-Status).
- [ ] **Nacheinander aktualisieren**: Zuerst „2026.3.22“ installieren/aktualisieren, dann „2026.3.23“, damit die Übergangskorrekturen der Reihe nach landen.
- [ ] **Führen Sie „openclaw doctor --fix“ unmittelbar nach jeder Upgrade-Phase aus**, um Migrationsdrift und veraltete Konfigurationsreferenzen zu reparieren.
- [ ] **Alte Plugin-/Agent-Importe** von entfernten Kompatibilitätsoberflächen auf die neuen „openclaw/plugin-sdk/*“-Muster und das neue Laufzeitausführungsmodell umstellen.
- [ ] **Plugin-Installationen und Metadatenpfade** in Richtung ClawHub migrieren (Flows „clawhub:<package>“, sofern verfügbar) und Skill-/Plugin-Kompatibilitätsstatus aktualisieren.
- [ ] **Matrix-Plugin-Setup aktualisieren** mithilfe der Migrationsanleitung, wenn es vom alten Matrix-Stack kommt.
- [ ] **Konfigurationshygiene migrieren**: Ersetzen Sie alte Umgebungsnamen und alte Statusspeicherorte („CLAWDBOT_*“/„MOLTBOT_*“, „~/.moltbot“) durch aktuelle OpenClaw-Entsprechungen.- [ ] **Überprüfen Sie die Konfiguration der Browser-Tools** auf Chrome-/Browser-MCP-Änderungen (vorhandene Sitzungen, userDataDir-Anhang, Entfernung des Erweiterungs-Relay-Pfads).
- [ ] **Überprüfen Sie Anbieter und Benutzeroberfläche/Zugänglichkeit nach dem Neustart** (Qwen/DashScope-Endpunkte, Modellstandards und wichtige UI-Abläufe) und führen Sie einen kurzen Rauchtest der Hilfstools durch.

## 6) Links erwähnt
- https://github.com/openclaw/openclaw/releases/tag/v2026.3.22
- https://github.com/openclaw/openclaw/releases/tag/v2026.3.23
- https://docs.openclaw.ai/gateway/doctor
- https://docs.openclaw.ai/tools/browser
- https://docs.openclaw.ai/plugins/sdk-migration
- https://docs.openclaw.ai/plugins/sdk-overview
- https://docs.openclaw.ai/install/migrating-matrix
- https://docs.openclaw.ai/tools/clawhub
- https://docs.openclaw.ai/install/migrating
- https://www.alibabacloud.com/en/product/modelstudio
- https://www.w3.org/TR/WCAG21/

## 7) Wo Sie uns finden
Besuchen Sie uns unter: **[tobyonfitnesstech.com](https://tobyonfitnesstech.com)**