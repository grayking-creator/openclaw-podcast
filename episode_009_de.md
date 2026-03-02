# OpenClaw Daily - Episode 9: OpenClaw v2026.3.1 — Wenn dein Assistent anfängt, sich wie Infrastruktur zu verhalten
# Datum: 2. März 2026
# Hosts: Nova (warm britisch) & Alloy (amerikanisch)

[NOVA]: Willkommen zurück bei OpenClaw Daily. Ich bin Nova.

[ALLOY]: Und ich bin Alloy.

[NOVA]: Heute machen wir eine Release-Folge zu OpenClaw v2026.3.1. Erwartet keinen „neues, glänzendes Modell“-Moment. Das ist eine „morgen fühlt sich dein System weniger fragil an“-Folge.

[ALLOY]: Es ist die Art Update, bei der du nicht eine riesige Funktion spürst — sondern drei kleine Ärgernisse, die du schon als normal akzeptiert hast … einfach aufhören.

[NOVA]: Genau. Ein Infrastruktur-Release.

[ALLOY]: Klingt langweilig — bis du es selbst betreiben musst.

[NOVA]: Wenn du OpenClaw wirklich betreibst — über Discord, Telegram, vielleicht einen Phone-Node, vielleicht einen Server, vielleicht Docker — willst du keine Überraschungen. Du willst vorhersagbare Lebenszyklen. Gesundheits-Signale. Streaming, das nicht auseinanderfällt. Automatisierung, die deine Kanäle nicht zuspammt.

[ALLOY]: Und dieses Release trifft genau das.

[NOVA]: Wir sprechen über: Discord-Thread-Session-Lifecycles, Telegram-DM-Themen, Android-Node-Aktionen und Device Health, Container-Probes, WebSocket-first Streaming für OpenAI Responses und Cron-Automation mit „Light Context“-Runs. Plus Extras wie das diffs-Tool und UI-Verbesserungen.

[ALLOY]: Und der rote Faden: Das sind keine Zufallsänderungen. OpenClaw zieht Schrauben nach, damit die Maschine schneller laufen kann, ohne sich selbst zu zerlegen.

[NOVA]: Los geht’s.

## Segment 1 — Das Muster: OpenClaw wird zum System

[ALLOY]: In jedem guten Open-Source-Projekt gibt es einen Übergang.

[NOVA]: Nämlich?

[ALLOY]: Erst ist es beeindruckend, weil es clever ist. Dann ist es beeindruckend, weil es zuverlässig ist.

[NOVA]: Und Zuverlässigkeit ist der echte Flex.

[ALLOY]: Genau. Cleverness bringt Stars und Demos. Zuverlässigkeit bringt Adoption.

[NOVA]: Diese Release Notes lesen sich wie von jemandem, der „on call“ war: Warum ist der Thread reset? Warum postet Cron Lärm? Warum hängt Streaming? Warum kann ich den Container nicht prüfen?

[ALLOY]: Fragen, die du erst stellst, wenn du wirklich abhängig davon bist.

## Segment 2 — Discord-Threads: Von fixem TTL zu Inaktivitäts-Workspaces

[NOVA]: Discord-Threads sind eines der besten Frontends für OpenClaw.

[ALLOY]: Weil Threads natürlich Projekten entsprechen.

[NOVA]: v2026.3.1 verschiebt die Thread-Bindings von „fixed TTL“ zu „inactivity-based“.

[ALLOY]: Richtig so: solange ich es nutze, bleibt es. Wenn nicht, verfällt es.

[NOVA]: Es gibt idleHours (Default 24) und optional maxAgeHours.

[ALLOY]: idleHours: „Wenn X Stunden niemand schreibt, läuft die Session ab.“

[NOVA]: maxAgeHours: „Selbst wenn aktiv: nicht älter als X.“

[ALLOY]: Hygiene und Sicherheitsventil gegen Kontext-Vermischung.

## Segment 3 — Telegram DM Topics: Eine Person, mehrere Workstreams

[ALLOY]: Telegram-DMs sind ohne Struktur ein Chaos.

[NOVA]: Ein Stream für alles wird zur „Junk Drawer“.

[ALLOY]: v2026.3.1 bringt DM Topics — mit eigenen Policies pro Thema: skills, systemPrompt, allowlists, requireTopic.

[NOVA]: Wichtig: skills pro Topic. Damit kannst du einen „Safe Mode“-Topic bauen, der brainstormt, aber keine Infrastruktur anfassen darf.

[ALLOY]: Und einen „Ops“-Topic mit Tools, aber mit expliziten Bestätigungen.

[NOVA]: requireTopic verhindert, dass alles wieder im selben Strom landet.

## Segment 4 — Android Nodes: Notification Actions + Device Health

[NOVA]: Mobile-Integration ist schwer. Deshalb zählen Guardrails.

[ALLOY]: Neu: camera.list, device.permissions, device.health und notifications.actions (öffnen, verwerfen, antworten).

[NOVA]: Notification-Aktionen sind mächtig — und riskant. Deshalb: erst zusammenfassen, dann Vorschlag, dann klare Bestätigung.

## Segment 5 — Health Probes: Liveness/Readiness

[ALLOY]: Wer ernsthaft deployt, will zwei Antworten: lebt es, und ist es bereit?

[NOVA]: Neu: health/healthz sowie ready/readyz. Außerdem Route-Fallbacks, damit nichts überschrieben wird.

## Segment 6 — Streaming: OpenAI Responses wird WebSocket-first

[NOVA]: Streaming macht Assistenten „lebendig“ — und bricht gern unter Proxies/Timeouts.

[ALLOY]: v2026.3.1 setzt WebSockets als Default, mit SSE-Fallback und Session-Cleanup.

[NOVA]: Weniger halbe Antworten, weniger Doppel-Resends, mehr Vertrauen.

## Segment 7 — Cron/Automation: Light Context gegen Spam

[ALLOY]: Automatisierung scheitert oft nicht technisch, sondern sozial: zu viel Lärm.

[NOVA]: Light Context reduziert injected Kontext für Cron-Runs. Ergebnis: weniger Leaks, weniger Erklärtext, mehr „Final Output“.

## Segment 8 — Extras: diffs, i18n, CLI-QoL

[NOVA]: Neues diffs-Tool (read-only) für saubere Diff-Renderings.

[ALLOY]: Web UI bekommt deutsche Locale.

[NOVA]: CLI zeigt den aktiven Config-Path — spart Stunden.

## Segment 9 — Upgrade-Checkliste

[ALLOY]: Update, sauber neu starten.

[NOVA]: Discord: idleHours an Kultur anpassen, maxAgeHours als Hygiene.

[ALLOY]: Telegram: Topics (Build/Admin/Personal) definieren, requireTopic erwägen.

[NOVA]: Android: mit permissions/health anfangen, Notification-Antworten nur mit Bestätigung.

[ALLOY]: Streaming testen, Cron auf Light Context + striktes Output-Format bringen.

## Abschluss

[NOVA]: Diese Version ist nicht gimmicky. Sie reduziert „weird output“ und macht das System vertrauenswürdiger.

[ALLOY]: Vertrauen ist kein Modellproblem. Es ist Engineering.

[NOVA]: OpenClaw wird zur Plattform, auf der du deinen Assistenten wirklich betreibst.
