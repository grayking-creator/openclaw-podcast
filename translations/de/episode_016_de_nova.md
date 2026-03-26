[NOVA]: Ich bin NOVA, das ist OpenClaw Daily, und heute haben wir eines dieser Releases, bei denen die Versionsnummern ordentlich aussehen, die eigentliche Geschichte darunter aber chaotisch, folgenreich und ehrlich gesagt ziemlich faszinierend ist. ... Diese Woche haben zwei Bugs ein echtes Power-User-Setup so hart getroffen, dass sie dir fast alles sagen, was du darüber wissen musst, wo OpenClaw gerade steht.

[ALLOY]: Ja. Das waren keine niedlichen kleinen Edge Cases. Das waren die Art von Bugs, die dich an deinem eigenen Setup zweifeln lassen, weil das, was du siehst, nicht das ist, was das System tatsächlich macht.

[NOVA]: Bug eins: Ein User hatte MiniMax als sein Reasoning-Modell konfiguriert. Die Upstream-API warf api_error. OpenClaw sah das, entschied, es müsse transient sein, versuchte es still noch einmal, machte den Fehler nie sichtbar, löste Fallback nie korrekt aus, und der User bekam ein degradiertes Ergebnis zurück, ohne jede Ahnung, dass der ursprüngliche Aufruf fehlgeschlagen war.

[ALLOY]: Das ist brutal, weil die schlimmsten Bugs die sind, die nicht explodieren. Sie werden einfach still immer schlimmer. Du bekommst kein rotes Licht. Du bekommst ein matteres grünes Licht.

[NOVA]: Genau. Und Bug zwei war eine andere Art von Schmerz, aber genauso real. Ein User fügt ein frisches OpenAI Codex-Token ein, sieht die Bestätigung, alles wirkt erfolgreich, startet das Gateway neu, und das Token ist wieder auf die abgelaufene Credential zurückgeschnappt.

[ALLOY]: Bei dem hier fühlst du dich verrückt. Denn aus Sicht des Users hat er alles richtig gemacht. Er hat das neue Token eingefügt. Die App sagte: ja, gespeichert. Dann nach dem Neustart: nein. Wieder das alte kaputte Token. ... Unter der Haube hat der In-Memory-Auth-State des Gateways beim Neustart den frisch auf Platte gespeicherten Wert überschrieben.

[NOVA]: Beides ist in v2026.3.23 behoben. Aber um zu verstehen, warum das passiert ist, musst du verstehen, was v2026.3.22 geändert hat. Denn .22 ist die große. .22 ist OpenClaw, das etwas tut, was es wahrscheinlich schon vor einem Jahr hätte tun sollen.

[ALLOY]: Die Legacy-Säuberung.

[NOVA]: Die Legacy-Säuberung. Die alten Namen, die Kompatibilitätsschichten, die seltsamen Übergangspfade, die Browser-Relay-Krücken, der Plugin-SDK-Brei — vieles davon wurde rausgerissen. ... Und ich glaube, die richtige Art, diese beiden Releases zusammen zu rahmen, ist diese: .22 entfernt die tote Haut, und .23 sorgt dafür, dass die neue Haut nicht aufreißt.

[ALLOY]: Das ist die ganze Episode. Wenn du eine echte Installation wartest, sind das keine dekorativen Updates. Sie sind strukturell.

[NOVA]: Fangen wir mit der emotional aufgeladensten Änderung an, denn Menschen hängen seltsam stark an Namen, selbst wenn diese Namen längst für immer hätten ausgemustert werden sollen. Die Environment-Namen CLAWDBOT_* und MOLTBOT_* sind weg. Nicht deprecated. Nicht mit einer Warnung toleriert. Weg.

[ALLOY]: Und ich will das bewusst langsamer machen, denn wenn du OpenClaw auf einem Laptop und sonst nirgendwo betreibst, hörst du das vielleicht und denkst: okay, ein paar Variablen umbenennen, passt. Das ist nicht der echte Failure Mode. Der echte Failure Mode ist, dass du eine alte .env-Datei in Docker Compose hast oder eine verkrustete systemd-Unit auf einem VPS oder irgendetwas in einem Shell-Profil, das du seit acht Monaten nicht mehr angesehen hast. Du machst ein Upgrade, OpenClaw startet, und diese Werte werden stillschweigend ignoriert.

[NOVA]: Kein Fehler. Kein Migrationsbanner.

[ALLOY]: Kein „hey, ich habe CLAWDBOT_TOKEN gesehen und das ist veraltet“. Einfach fehlende Config. Plötzlich passt auth nicht mehr, der State-Pfad ist nicht da, wo du ihn vermutet hast, vielleicht lädt ein Plugin nicht, vielleicht wirkt ein Token abwesend. ... Das ist die Art von Bruch, die dich um zwei Uhr morgens nach einem Upgrade auf einer Maschine erwischt, die du lange nicht angefasst hast.

[NOVA]: Mach grep über deine Env-Dateien. In jeder Umgebung, in der du OpenClaw betreibst. Auf jedem Host. In jeder Compose-Datei. In jeder Startup-Unit. In jedem Shell-Bootstrap. Wenn du CLAWDBOT_* oder MOLTBOT_* hast, behandle das als kaputt, bis es korrigiert ist.

[ALLOY]: Dasselbe gilt für das alte ~/.moltbot-State-Verzeichnis. Dieser Pfad gehört nicht mehr zur Zukunft. Wenn dein State noch dort liegt, wird OpenClaw das nach dem Upgrade nicht magisch für dich erschließen. Verschiebe ihn nach ~/.openclaw oder setze OPENCLAW_STATE_DIR explizit und mach damit Schluss.

[NOVA]: Und das ist eine dieser Entscheidungen, bei denen ich der Härte tatsächlich zustimme. Übergangs-Aliasse wirken kurzfristig nett, aber sie bringen die Architektur dazu, über sich selbst zu lügen. Es kostet real etwas, so zu tun, als wären alte Namen noch immer erstklassig.

[ALLOY]: Ich stimme dem Endzustand zu. Ich stimme nicht zu, wie gelassen manche beim Migrationsschmerz sind. Wenn du die Person bist, die fünf Installationen verwaltet und zwei davon sind seltsam, dann ist das keine philosophische Aufräumaktion. Das ist eine Schnitzeljagd.

[NOVA]: Fair. ... Die zweite große Breaking Change in .22 ist, dass ClawHub jetzt first-class ist, und die praktische Bedeutung davon ist größer, als das Marketing-Wording vermuten lässt. openclaw plugins install name prüft jetzt zuerst ClawHub und fällt nur dann auf npm zurück, wenn ClawHub das Paket nicht hat.

[ALLOY]: Das bedeutet, das Installationsverhalten hat sich geändert, selbst wenn du deinen Befehl nicht geändert hast. Das ist die Sache, die die Leute hören müssen. Wenn du Skripte hast, die von einem npm-Paketauflösungspfad ausgehen, und derselbe Name jetzt auf ClawHub existiert, bekommst du vielleicht zuerst die ClawHub-Version.

[NOVA]: Es gibt jetzt auch native Befehle: openclaw skills search, openclaw skills install, openclaw skills update. ... Und für mich ist das OpenClaw, das das Produkt endlich mit seinem beabsichtigten Ökosystem in Einklang bringt. ClawHub sollte immer das Zuhause für Skills sein. Dieses Release macht das real statt bloß aspirativ.

[ALLOY]: Es ist sauberer, aber teste deine Automatisierung. Wenn du Bootstrap-Skripte, Dotfiles oder Onboarding-Dokumente hast, stelle sicher, dass sie immer noch das installieren, was du glaubst, dass sie installieren. Die Änderung ist gut. Überraschungen sind es nicht.

[NOVA]: Drittens: der Plugin SDK-Umbau. Das ist kein kleines Knabbern an den Rändern. openclaw/extension-api ist weg. Es gibt keinen Compatibility-Shim. Die neue Oberfläche ist openclaw/plugin-sdk/* mit engeren Subpaths und viel klareren Grenzen.

[ALLOY]: Wenn du eigene Plugins hast, ist das eine echte Migration. Sie ist nicht optional. Es gibt keinen Fallback. Du kannst nicht sagen: „Ich update später.“ Später ist kaputt.

[NOVA]: Gebündelte Plugins müssen jetzt auch die injizierte Runtime für hostseitige Operationen verwenden, was nach einer dieser Änderungen klingt, die bürokratisch wirken, bis du merkst, dass sie eine Menge mehrdeutiges Privilegien-Ausbluten entfernt. Host-Verhalten ist explizit. Runtime-Grenzen sind explizit.

[ALLOY]: Und auch die Message-Discovery hat sich geändert. describeMessageTool() ist jetzt erforderlich. Der alte Ablauf mit listActions, getCapabilities, getToolSchema ist entfernt. ... Das ist keine Umbenennung. Das ist eine Vertragsänderung.

[NOVA]: Das neue SDK ist tatsächlich sauberer. Wirklich. Die Imports sind enger. Die Intention ist klarer. Das Runtime-Modell ist kohärenter. Aber du musst migrieren. Und wenn du Plugin-Developer bist, lies docs.openclaw.ai/plugins/sdk-migration. Improvisiere nicht aus dem Gedächtnis.

[ALLOY]: Ich will das unterstreichen. Das ist nicht die Woche, um deine Migration frei Hand nach Gefühl hinzuschreiben.

[NOVA]: Vierter Block: Security-Hardening. Manches davon ist unsichtbar, bis es dich rettet, was bedeutet, dass es nicht so viel Airtime bekommt, aber es ist wichtig. Der Exec-Sandbox blockiert jetzt MAVEN_OPTS, SBT_OPTS, GRADLE_OPTS, ANT_OPTS sowie GLIBC_TUNABLES und DOTNET_ADDITIONAL_DEPS. ... Das ist im Grunde eine Bereinigung gegen Runtime-Injection-Oberflächen, von denen die Leute vergessen, dass sie existieren.

[ALLOY]: Genau. Diese Env Vars sind die Art von Dingen, die Angreifer lieben und Betreiber vergessen. Wenn deine Tool-Sandbox sagt: „Wir kontrollieren, was läuft“, du aber immer noch Build-Tool- oder Runtime-Injection-Variablen durchrutschen lässt, kontrollierst du in Wahrheit nicht besonders viel.

[NOVA]: Es gibt auch eine subtile, aber clevere Allowlist-Änderung: time ist jetzt transparent in der Allowlist-Auswertung. Also bindet time ./approved-script an das innere Skript, nicht an den time-Wrapper.

[ALLOY]: Das ist so praktisch. Leute wrappen beim Debugging ständig Befehle mit time. Früher konnten Wrapper seltsame Policy-Edge-Cases erzeugen. Jetzt bewertet es das Ding, das du tatsächlich ausführen wolltest.

[NOVA]: Und auch das Voice-Webhook-Hardening wurde strenger: fehlende Provider-Signaturen werden vor dem Lesen des Bodys abgelehnt, mit einem 64KB- und 5s-Pre-Auth-Limit. Das ist einfach saubere Perimeter-Hygiene. Verbrate keine Ressourcen darauf, nicht authentifizierten Müll zu parsen.

[ALLOY]: Schließlich zu den leisen Fixes, die wichtig sind: Discord-Slash-Commands. Carbon reconcile ist jetzt der Default, sodass Gateway-Neustarts Slash-Commands nicht länger über den lokalen Deploy-Pfad durchchurnen.

[NOVA]: Ich liebe diese Klasse von Fixes, weil User sie als weniger Geister erleben.

[ALLOY]: Ja. Leise, aber real. Neustarts haben Ghost-Commands erzeugt. Jetzt nicht mehr. Das ist nicht glamourös, aber genau die Art von Paper Cut, die eine Plattform amateurhaft wirken lässt, wenn du sie ungefixt lässt.

[NOVA]: Also .22 in einem Satz: OpenClaw hat aufgehört so zu tun, als sei Legacy harmlos.

[ALLOY]: Und wenn du dein Setup eine Weile nicht angefasst hast, ist .22 das Release, das das für dich herausfinden wird.

[NOVA]: Ich glaube auch, dass dieses Release eine Linie zwischen Kompatibilität und Ballast zieht. Lange Zeit hat OpenClaw alte Namen, alte Installationsannahmen, alte Plugin-Discovery-Formen und alte Browser-Pfade mitgeschleppt, weil es riskant wirkte, sie zu entfernen. ... Aber sie drin zu lassen war ebenfalls riskant. Es machte die Plattform schwerer zu durchdenken.

[ALLOY]: Das ist der Trade-off, den Menschen übersehen. Abwärtskompatibilität erhält nicht nur Funktion. Sie erhält auch Verwirrung. Jeder Alias, jeder alte Pfad, jeder „das akzeptieren wir immer noch“-Zweig wird zu einer weiteren Sache, an die der Support denken muss, und zu einer weiteren Sache, über die Betreiber stolpern.

[NOVA]: Und sobald du um ClawHub, das moderne Plugin SDK und aktuelle Benennung zentralisierst, kann die Dokumentation endlich aufhören, in zwei Zeitlinien zu sprechen.

[ALLOY]: Das ist wichtiger, als viele denken. Die Hälfte des operativen Schmerzes ist nicht der Bug selbst. Es ist das Gefühl, dass jede Anleitung, die du liest, für eine andere Generation des Produkts sein könnte.

[NOVA]: Wenn sich .22 also hart anfühlt, dann deshalb, weil es sich für eine Realität entscheidet.

[ALLOY]: Ja. Eine Realität, weniger Aliasse, weniger Relikte. Kurzfristiger Schmerz, langfristige Vernunft.

[NOVA]: Wir müssen echte Zeit auf Browser-Tooling verwenden, denn für viele User ist das die größte einzelne operative Änderung in diesem Doppelt-Release. Das Legacy-Chrome-Extension-Relay ist weg. driver: "extension", gebündelte Extension-Assets, browser.relayBindHost — alles entfernt.

[ALLOY]: Und falls du damals nicht dabei warst: Hier ist, was die Extension tatsächlich war. OpenClaw hat früher eine Chrome-Extension ausgeliefert, die wie ein Relay für CDP, das Chrome DevTools Protocol, fungierte. Du hast die Extension manuell installiert, Browser-Berechtigungen vergeben, und sie diente als Brücke zwischen OpenClaw und dem Browser.

[NOVA]: Was sich immer ein bisschen improvisiert angefühlt hat.

[ALLOY]: Es war improvisiert. Nützlich, aber improvisiert. Es funktionierte, weil Browser-Steuerung chaotisch ist und die Extension dir einen Weg gab, der einfacher war, als allen Direct-Attach zu erklären. Aber sie brachte den ganzen Ballast einer Extension mit: Installationsreibung, seltsame Berechtigungen, Kompatibilitätsdrift, Browser-Profileigenheiten und ein weiteres bewegliches Teil, das du diagnostizieren musst, wenn etwas schiefläuft.

[NOVA]: Das Ersatzmodell ist einfach besser. OpenClaw verbindet sich jetzt direkt mit einer laufenden Chrome-Instanz oder mit einem User-Profil über Standard-CDP-Mechanismen. Keine Extension nötig. Kein Custom-Relay in der Mitte. ... Architektonisch ist das sauberer. Weniger maßgeschneiderte Schichten. Weniger im Tooling versteckte Geheimnisse.

[ALLOY]: Aber — und das ist die wichtige praktische Warnung — wenn du ein Upgrade machst, ohne vorher openclaw doctor --fix auszuführen, oder zumindest direkt danach, kann deine Browser-Automatisierung komplett kaputtgehen. Und sie geht nicht immer auf offensichtliche Weise kaputt. Du bekommst nicht zwangsläufig eine freundliche Nachricht wie „extension relay removed“. Wahrscheinlicher ist, dass es einfach nicht verbindet oder Consent-Schleifen sich merkwürdig verhalten oder dein Attach-Pfad halb lebendig aussieht und dann stirbt.

[NOVA]: openclaw doctor --fix liest deine aktuelle Config und migriert host-lokale Browser-Setups in den richtigen modernen Modus: existing-session oder user. Das ist keine kosmetische Empfehlung. Es ist Teil der Migration.

[ALLOY]: Und es lohnt sich, die drei Modi jetzt klarzustellen. existing-session bedeutet, an ein laufendes Chrome anzudocken. user bedeutet, mit einem User-Profil zu starten. Rohes CDP für Docker-, headless-, Sandbox- oder Remote-Setups — das bleibt im Wesentlichen unverändert.

[NOVA]: Das ist die richtige Trennung. Der alte Extension-Pfad war eine Krücke. Das hier ist der richtige Move.

[ALLOY]: Ich stimme größtenteils zu, aber ich will verteidigen, warum User die Krücke mochten. Eine Krücke ist ein Problem, wenn sie Heilung verhindert. Sie ist hilfreich, wenn sie dich gehen lässt. Für viele User war die Extension der einzige Browser-Flow, den sie konsistent zum Laufen bringen konnten.

[NOVA]: Fair, aber es war Konsistenz, die mit Fragilität erkauft wurde. Das System hatte eine zusätzliche Custom-Brücke nur, um das Attach-Modell zu kaschieren.

[ALLOY]: Stimmt. Und .23 beweist deinen Punkt sogar, denn nachdem .22 den alten Pfad entfernt hat, musste .23 den neuen Pfad sofort in der echten Welt zuverlässig machen. ... Zwei Fixes sind hier wichtig. Erstens: Timing beim Tab-Attach. OpenClaw behandelte den Chrome-MCP-Handshake so, als wäre der Browser in dem Moment vollständig bereit, in dem die Verbindung hochkam. Auf macOS stimmte das nicht immer. Tabs existierten, aber sie waren noch nicht benutzbar. Also konnte der erste Attach Consent churnen, Timeouts drehen und sich insgesamt heimgesucht anfühlen.

[NOVA]: Dieser Fix ist wichtig, weil Bereitschaft nicht binär ist. Ein offener Socket ist nicht dasselbe wie eine stabile UI-Oberfläche.

[ALLOY]: Genau. Zweiter Fix: Loopback-Reuse. Bei headless- oder Loopback-Setups konnte OpenClaw bei einem kurzen Probe-Lauf einen laufenden Browser verpassen und sofort auf Relaunch zurückfallen. Das erzeugte Second-Run-Regressions, bei denen der erste Lauf funktionierte und der nächste so tat, als müsste er die Session niederwalzen. .23 fügt vor diesem Fallback eine kurze Wartezeit hinzu.

[NOVA]: Das klingt winzig, bis du damit lebst. Dann ist es der Unterschied zwischen einem Browser-Tool, das flaky wirkt, und einem, das sich absichtlich gebaut anfühlt.

[ALLOY]: Deshalb lautet meine Zusammenfassung dieser Browser-Transition: .22 hat den alten Pfad entfernt, .23 hat den neuen Pfad zuverlässig gemacht, und du brauchst beides. Wenn du nur auf Ebene der Release-Headlines denkst, wirst du übersehen, wie eng diese beiden Versionen tatsächlich gekoppelt sind.

[NOVA]: Außerdem solltest du, wenn du host-lokale Browser-Automatisierung betreibst, doctor --fix als Teil der Browser-Migration behandeln, nicht als allgemeine Wartungsaufgabe. Es macht gezielte Arbeit.

[ALLOY]: Ja. Kein optionales Housekeeping. Ein Migrationsschritt.

[NOVA]: Und es gibt auch eine größere Lektion in diesem Browser-Wechsel. Browser-Automatisierung ist eines dieser Gebiete, in denen Leute absurde Komplexität tolerieren, weil der Payoff so hoch ist. Sie installieren eine Extension, pinnen eine Version, segnen ein Profil, schleppen seltsame Launch-Flags mit sich herum — alles, solange der Browser gehorcht. ... Aber jeder versteckte Workaround wird zu technischer Schuld mit Benutzeroberfläche.

[ALLOY]: Das ist eine gute Formulierung. Die Extension war nicht nur Code-Schuld. Sie war User-Ritual-Schuld. Du musstest daran denken, dass sie existiert, daran denken, wie sie installiert wurde, daran denken, warum ein Browser-Profil etwas Besonderes war, daran denken, was kaputtging, wenn Chrome updatete. Das ist keine Plattform-Story, die du für immer willst.

[NOVA]: Existing-session-Attach ist ein viel ehrlicheres Modell. Entweder gibt es einen Browser, an den du andocken kannst, oder es gibt ihn nicht. Entweder ist das Profil brauchbar, oder es ist es nicht. Es gibt weniger Magie.

[ALLOY]: Weniger Magie, aber mehr Verantwortung, Bereitschaft und Timing richtig hinzubekommen, weshalb diese .23-Fixes so wichtig sind. Wenn du die alte Brücke entfernst, muss sich der direkte Pfad langweilig anfühlen. Langweilig ist Erfolg in der Browser-Automatisierung.

[NOVA]: Langweilig, verlässlich, lesbar. Das ist das Ziel.

[NOVA]: Als Nächstes: Bildgenerierung. Das hier ist weniger dramatisch als Browser-Tooling, aber es sagt dir viel darüber, wohin OpenClaw geht. Die gebündelte Skill nano-banana-pro wurde entfernt. Weg. Kein Shim.

[ALLOY]: Das bedeutet: Wenn du Workflows, Prompts oder interne Docs hattest, die nano-banana-pro aufrufen, finde sie und ersetze sie. Das ist ein harter Bruch. Geh nicht davon aus, dass ein Alias auf dich wartet.

[NOVA]: Die Plattform standardisiert sich auf das Core-Tool image_generate. Und philosophisch halte ich das für genau richtig. Ein Tool, konfigurierbares Backend, konsistente Invocation-Oberfläche. Besser, als für immer einen gebündelten Skill-Wrapper mitzuschleppen, nur weil Menschen sich an seinen Namen gewöhnt haben.

[ALLOY]: Solange du den Config-Key setzt. Das ist der Teil, den Menschen überspringen. Du brauchst agents.defaults.imageGenerationModel.primary: "google/gemini-3-pro-image-preview". Wenn du das nicht setzt, ist das Verhalten undefiniert. Und undefiniert im Config-Land bedeutet nie spannend. Es bedeutet verwirrend.

[NOVA]: Hier steckt ein breiteres Muster drin. OpenClaw versucht, Core-Fähigkeiten wie Core-Fähigkeiten aussehen zu lassen. Bildgenerierung sollte sich nicht wie ein Sidecar-Trick anfühlen.

[ALLOY]: Richtig, aber operativ würde ich es direkter formulieren: Standardisierung ist nur dann schön, wenn die Defaults explizit sind. Wenn du das alte gebündelte Ding rausziehst und das neue Backend nicht setzt, hast du eine sauberere Architektur und einen schlechteren Dienstag geschaffen.

[NOVA]: Faire Kritik. ... Es gibt in diesem Shift auch Marketplace-Verbesserungen. Marketplace-Installationen sind jetzt first-class, einschließlich plugin@marketplace-Syntax und Claude-Marketplace-Registry-Support.

[ALLOY]: Das reduziert die Menge an Folklore bei der Plugin-Installation. Weniger Momente von „eigentlich machst du es bei diesem Plugin auf diese andere Art“.

[NOVA]: Und Owner-gated /plugins- und /plugin-Chat-Befehle setzen genau dieses Thema fort: der Plattform eine einzige kohärente Geschichte für das Entdecken, Installieren und Verwalten von Extensions zu geben.

[ALLOY]: Ich mag auch, dass sie owner-gated sind. Je mächtiger die Installationsoberfläche wird, desto weniger willst du, dass zufällige Runtime-Kontexte sie wie ein Spielzeug behandeln.

[NOVA]: Für mich ist die Story bei der Bildgenerierung diese: OpenClaw bewegt sich von gebündelter Persönlichkeit hin zu konfigurierter Fähigkeit. ... Das ist Reife.

[ALLOY]: Für mich ist es dies: Aktualisiere deine Workflows, setze den Model-Key, und lass keine kaputten Bildaufrufe in Automatisierung herumliegen, die du erst während einer Demo entdeckst.

[NOVA]: Und in dieser Standardisierung versteckt sich auch eine subtile Governance-Änderung. Wenn Bildgenerierung ein Core-Tool statt einer geliebten gebündelten Skill ist, kannst du Provider austauschen, die Oberfläche einmal verbessern, ein Verhalten dokumentieren und eine Permission-Oberfläche auditieren.

[ALLOY]: Genau. Es hört auf, „dieses eine besondere Ding zu sein, das funktioniert, weil ein Wrapper existiert“, und wird Teil des eigentlichen Plattformvertrags. Das ist gesünder.

[NOVA]: Es verändert auch, wie Teams über Portabilität nachdenken sollten. Wenn dein Workflow image_generate sagt und dein Backend separat konfiguriert ist, kannst du Provider migrieren, ohne die Workflow-Logik selbst umzuschreiben.

[ALLOY]: Das ist in der Theorie sehr schön und noch schöner, wenn ein Vendor an einem Freitagnachmittag Preise oder Rate Limits ändert.

[NOVA]: Genau. Standardisierung ist nicht nur Eleganz. Sie ist Hebelwirkung.

[ALLOY]: Solange du den Config-Key setzt.

[NOVA]: Solange du den Config-Key setzt. Das kannst du bis ans Ende aller Zeiten wiederholen.

[NOVA]: Das ist das Herzstück der Episode. Denn .22 ist die Säuberung, aber .23 ist der Reliability Pass, der die Säuberung überlebbar macht. Gehen wir zurück zum ersten Bug aus dem Intro: MiniMax-Failover.

[ALLOY]: Das ist der Bug. Das ist der, der die Leute verbrannt hat.

[NOVA]: Das ursprüngliche Problem war die Klassifizierung. Generische api_error-Antworten von MiniMax wurden standardmäßig als transient behandelt. Also versuchte OpenClaw stillschweigend neu, unterdrückte den eigentlichen Fehler und löste korrektes Fallback nie aus, wenn das zugrunde liegende Problem etwas wie Billing, auth oder malformed context war.

[ALLOY]: Und das ist die entscheidende Unterscheidung. Ein transienter Fehler ist: Vielleicht hat das Netzwerk geniest, vielleicht hatte der Provider einen kurzen Wackler, vielleicht funktioniert ein Retry wirklich. Aber ein Billing-Problem ist nicht transient. Ein Auth-Problem ist nicht transient. Eine Format- oder Kontextablehnung ist nicht transient. Diese Dinge neu zu versuchen verschwendet nur Zeit und versteckt die Wahrheit.

[NOVA]: Der Fix ist präzise. Es ist nicht: „Hört auf, MiniMax neu zu versuchen.“ Es ist: „Versuche nur dann erneut, wenn der Fehler tatsächlich transient aussieht.“ ... Das ist die Art von Fix, der ich vertraue, weil er das ursprüngliche Designziel — Resilienz — bewahrt und gleichzeitig die schlampige Klassifizierung entfernt, die Resilienz wie Verschleierung wirken ließ.

[ALLOY]: Und für Betreiber ist hier der praktische Impact: schlechter Key, schlechter Account-Status, malformed request, gesprengtes Kontextfenster — all das sollte jetzt auf eine Weise fehlschlagen, die sichtbar wird und Fallback korrekt eingreifen lässt. Genau das hatten die Leute die ganze Zeit erwartet.

[NOVA]: Das ist einer dieser Bugs, bei denen das degradierte Erlebnis fast schlimmer war als ein harter Fehler, weil der User Output bekam und annahm, er sei korrekt.

[ALLOY]: Ja. Eine falsche Antwort ohne sichtbaren Alarm ist unheimlicher als ein sichtbarer Fehler. Ein sichtbarer Fehler lädt zumindest zur Untersuchung ein.

[NOVA]: Als Nächstes: der OpenAI-Token-Revert-Bug. Das ist ein perfektes Beispiel dafür, wie State-Drift zwischen Speicher und Festplatte den User verrät. Der Write-Pfad des Gateway-Auth-Profils erlaubte es, dass veraltete In-Memory-Werte frisch gespeicherte Credentials beim Neustart überschrieben.

[ALLOY]: Also fügst du das Token ein, siehst grün, startest neu, abgelaufen. Jedes Mal. ... Deshalb fühlte sich dieser Bug so persönlich an. Er griff das Vertrauen in den grundlegenden Akt des Speicherns von Credentials an.

[NOVA]: Und der Fix ist, dass das Einfügen des Tokens jetzt korrekt in den aufgelösten Agent-Store schreibt, statt den veralteten In-Memory-Snapshot beim Neustart gewinnen zu lassen.

[ALLOY]: Das heißt, nach dem Upgrade solltest du es testen. Nimm nicht einfach an, dass es stimmt, nur weil die Release Notes sagen, es sei behoben. Füge ein frisches Token ein, starte das Gateway neu, verifiziere, dass es persistiert hat. Das ist genau die Sorte Bug, bei der du Vertrauen gewinnst, indem du den alten Fehler reproduzierst und dabei zusiehst, wie er nicht mehr passiert.

[NOVA]: Drittens: Cron und Sommerzeit. Das klingt langweilig, bis es etwas trifft, auf das du dich verlässt.

[ALLOY]: Das hat mich erwischt. Mein Morgenbericht ging nach der Zeitumstellung eine Stunde versetzt los.

[NOVA]: Konkretes Beispiel: Du planst einen Job für 8 AM. DST schlägt zu. Vor .23 konnten diese „8 AM“ zu 7 AM oder 9 AM werden, abhängig davon, wie der Scheduler die Grenze interpretierte. ... Das ist nicht nur eine kosmetische Abweichung. Für eine tägliche Routine ist das ein gebrochenes Versprechen.

[ALLOY]: Der Fix ist, dass --at --tz jetzt lokale Wanduhrzeit über DST-Grenzen hinweg respektiert. Und OpenClaw lehnt --tz auch für --every ab, was gut ist, weil die Semantik wiederkehrender Intervalle und die Semantik lokaler Zeitzonen-Wanduhrzeit nicht dasselbe sind.

[NOVA]: Das ist die Art von Einschränkung, die Users vor falschen Intuitionen bewahrt.

[ALLOY]: Genau. Wenn du meinst: „alle sechs Stunden“, ist das nicht dasselbe wie: „immer wenn meine lokale Uhr acht sagt“. Das Tool spiegelt diesen Unterschied jetzt wider, statt ihn zu verwischen.

[NOVA]: Viertens: der Mistral-422-Fix. Ältere persistierte Mistral-Configs trugen Output-Limits in Kontextgröße mit sich herum, die Mistral sofort ablehnt. Ergebnis: 422-Fehler, die mysteriös wirken, wenn du die Config-Herkunft nicht kennst.

[ALLOY]: Und wieder macht openclaw doctor --fix hier echte Arbeit. Es erkennt und repariert jetzt diese veralteten Mistral-Configs.

[NOVA]: Noch ein Grund, doctor --fix laufen zu lassen. Manche hören diesen Befehl als generelles Doktern, als würde er vielleicht ein paar offensichtliche Dinge aufräumen. Nein. In dieser Release-Reihe kodifiziert er Migrationswissen.

[ALLOY]: Fünftens: ClawHub auf macOS. Hier gibt es zwei Probleme. Gespeicherte Credentials respektierten den macOS-Application-Support-Pfad nicht korrekt, und das Browse-all-Verhalten lief gegen unauthentifizierte 429-Rate-Limits.

[NOVA]: Das bedeutet, die UI konnte dich auf vage Weise in die Irre führen und dich denken lassen, ClawHub sei leer oder kaputt.

[ALLOY]: Skill-Browsing fiel auf macOS stillschweigend auf unauthentifiziert zurück. Du sahst leere Listen und nahmst an, es gäbe keine Skills, oder du dachtest, deine Installation sei kaputt, obwohl in Wirklichkeit die Behandlung des Auth-Pfads falsch war. ... Die Fixes waren, den korrekten Auth-Pfad zu respektieren und Browse-all auf den Search-Endpoint umzustellen, was ein viel sinnvollerer Weg ist, sinnloses unauthentifiziertes Throttling zu vermeiden.

[NOVA]: Sechstens: gebündelte Plugin-Runtimes. WhatsApp- und Matrix-Runtime-Sidecars fehlten im npm-Paket, was bedeutete, dass globale Installationen auf eine Weise fehlschlagen konnten, die wie Packaging-Voodoo aussah.

[ALLOY]: Das ist eine Regression aus den Packaging-Änderungen von .22, und zu OpenClaws Ehren muss man sagen: Es wurde in .23 schnell behoben. Aber wenn du diese Runtimes global betreibst, ist das keine Fußnote. Fehlende Sidecars bedeuten, dass der Plugin-Stack schlicht nicht vollständig ist.

[NOVA]: Siebtens: veraltete Provider-Behandlung in web_search. Das Tool verwendete den Provider-State, der beim Startup eingebacken worden war, statt der aktiven Runtime-Config.

[ALLOY]: Genau die Art von Bug, die dich infrage stellen lässt, ob Config-Reloads real sind oder nur dekorativ.

[NOVA]: Du konfigurierst Brave, es sollte Brave verwenden. Es hätte immer so funktionieren sollen.

[ALLOY]: Und jetzt tut es das. Wieder nicht glamourös, aber eine direkte Reparatur von Erwartung versus Verhalten.

[NOVA]: Achtens: Telegram-Threading. currentThreadTs wird jetzt im Threading-Tool-Context-Fallback für Telegram-DM-Themen befüllt, sodass thread-aware Tools tatsächlich den richtigen Themenkontext erhalten.

[ALLOY]: Das ist einer dieser Fixes, bei denen du, wenn du Telegram-DM-Themen nicht nutzt, mit den Schultern zuckst, und wenn du sie nutzt, sagst: Gott sei Dank. Denn wenn Tool-Context thread-blind ist, endest du damit, dass Agents am falschen Ort antworten oder die Gesprächsspur verlieren.

[NOVA]: Was besonders schmerzhaft ist in einem System, das um Kontexttreue herum gebaut ist.

[ALLOY]: Genau. Der ganze Punkt ist, dass das Tool wissen sollte, wo es ist.

[NOVA]: Zusammengenommen ist das .23-Release also nicht flashy im üblichen Produktsinn. Es ist ein Reliability Pass im tiefsten Sinn des Ausdrucks. Es verschärft Klassifizierung, State-Persistenz, Scheduler-Semantik, Provider-Verdrahtung, Packaging-Vollständigkeit und Thread-Kontext.

[ALLOY]: Es macht die neue Welt von .22 tatsächlich bewohnbar.

[NOVA]: Und ich glaube, deshalb sollten Betreiber diese beiden Releases als eine Geschichte mit zwei Kapiteln lesen. Kapitel eins sagt: „Wir haben die alten Kompromisse entfernt.“ Kapitel zwei sagt: „Wir haben die Stellen repariert, an denen die neuen Annahmen noch raue Kanten hatten.“ ... Das ist ein viel ehrlicherer Entwicklungsrhythmus, als so zu tun, als wäre die große Bereinigung am ersten Tag perfekt gelandet.

[ALLOY]: Ja. Ich respektiere .23 tatsächlich, weil es nicht versucht zu verbergen, was .22 destabilisiert hat. Es behebt es einfach. Schnell. Direkt. Ohne Ego.

[NOVA]: Und als User ist das genau das, was du nach einem strukturellen Release willst. Keine Verleugnung. Schnelle Korrektur.

[ALLOY]: Besonders bei den stillen Sachen. MiniMax-Fallback, Token-Persistenz, veraltete Provider-Config — das sind alles Bugs, die Vertrauen erodieren, weil sie das System weniger lesbar wirken lassen, als es sein sollte.

[NOVA]: Zuverlässigkeit ist teils Korrektheit und teils Verständlichkeit. Die Plattform muss das Richtige tun, und du musst verstehen können, warum sie getan hat, was sie getan hat.

[ALLOY]: Deshalb ist .23 wichtiger, als es ein Feature-Release wäre.

[NOVA]: Schauen wir auf die kleineren Änderungen, denn kleiner sind sie nur in der Oberfläche, nicht unbedingt in ihrer Wichtigkeit. Erstens: Qwen und DashScope. OpenClaw unterstützt jetzt Standard-DashScope-Endpoints für China und globale Qwen-API-Keys, und der Provider wurde in Qwen (Alibaba Cloud Model Studio) umbenannt.

[ALLOY]: Pay-as-you-go-Keys funktionieren jetzt. Das ist die praktische Änderung. Wenn du außerhalb der Standard-OpenAI-Anthropic-Umlaufbahn unterwegs bist, ist das ziemlich wichtig.

[NOVA]: Qwen ist gerade eine der besten Open-Weight-Familien. Richtiger DashScope-Support bedeutet echte Zugänglichkeit für User, die starke Modelle wollen, ohne in dieselben zwei Provider-Ökosysteme gezwungen zu werden, die alle anderen voraussetzen.

[ALLOY]: Und bessere Benennung ist ebenfalls wichtig. Das Umbenennen in die volle Model-Studio-Identität macht die Config-Oberfläche weniger kryptisch.

[NOVA]: Als Nächstes: CSP-Hardening. SHA-256-Hashes für Inline-Script-Blöcke. Inline-Scripts standardmäßig blockiert.

[ALLOY]: Wenn du OpenClaw hinter einem strikten Reverse Proxy betreibst, ist das die Version, auf die du upgraden solltest.

[NOVA]: Das ist wichtig für Supply-Chain-Sicherheit. Ein injiziertes Script wird nicht ausgeführt, weil der Hash nicht passt. ... Das sind die Arten von Kontrollen, die eine Demo nicht hübscher machen, aber deinen Blast Radius kleiner.

[ALLOY]: Und ehrlich gesagt machen reife Plattformen genau das. Sie hören auf, sich auf „na ja, dort sollte niemand etwas injizieren“ zu verlassen, und bauen stattdessen um die Frage herum: „Wenn etwas injiziert wird, was läuft dann immer noch nicht?“

[NOVA]: Auch das Knot-Theme bekam Aufmerksamkeit: WCAG 2.1 AA-Kontrast-Compliance, Feintuning der Schwarz-Rot-Palette, Config-Icons, diskrete Rundungsstufen.

[ALLOY]: Der AA-Kontrast-Fix ist der, der zählt. Er fiel bei Accessibility-Checks durch. Stil macht Spaß; Lesbarkeit ist Pflicht.

[NOVA]: Und ich mag es immer, wenn Accessibility-Verbesserungen als Standard-Qualitätsverbesserungen behandelt werden statt als Nischen-Nebenmission.

[ALLOY]: Letztes kleines Ding: Gateway-Usage-Gesamtsummen enthalten jetzt rotierte und archivierte Sessions.

[NOVA]: Was fast nach Buchhaltung klingt.

[ALLOY]: Das ist es auch. Aber Usage wurde zu niedrig gezählt. Jetzt nicht mehr. Wenn du versuchst, die tatsächliche Systemlast zu verstehen oder Aktivität über die Zeit zu vergleichen, dann sind fehlende archivierte Sessions kein Rundungsfehler. Es ist einfach falsch.

[NOVA]: Also zeigen sogar die kleinen Dinge in diesen Releases in dieselbe Richtung: weniger Mehrdeutigkeiten, weniger Auslassungslügen, eine präzisere Darstellung dessen, was das System wirklich tut.

[ALLOY]: Alles klar, machen wir es konkret. Wenn du ein Upgrade machst, hier ist die Checkliste, und ich meine ganz wörtlich Checkliste. Vertraue dir nicht, dass du sie mitten in der Migration im Kopf behältst.

[NOVA]: Schritt eins ist nicht verhandelbar.

[ALLOY]: openclaw doctor --fix. Zuerst, vor allem anderen. Und ehrlich gesagt direkt nach jeder Upgrade-Stufe, wenn du die Sequenz sauber durchziehst.

[NOVA]: Das ist der Ankerbefehl für diese Releases. Kein Nice-to-have. Anker.

[ALLOY]: Schritt zwei: Suche per grep nach CLAWDBOT_* und MOLTBOT_* in allen .env-Dateien, Docker-Dateien, systemd-Units, Shell-Profilen, jeder Startup-Oberfläche, die du hast.

[NOVA]: Wenn die alten Namen existieren, geh davon aus, dass sie jetzt tote Config sind.

[ALLOY]: Schritt drei: Prüfe auf ~/.moltbot. Wenn es existiert, verschiebe den State nach ~/.openclaw oder setze OPENCLAW_STATE_DIR explizit.

[NOVA]: Schritt vier: setze agents.defaults.imageGenerationModel.primary: "google/gemini-3-pro-image-preview". Lass die Bildgenerierung nicht in undefiniertem Limbo hängen.

[ALLOY]: Schritt fünf: Teste MiniMax nach dem Upgrade mit einem schlechten Key erneut und bestätige, dass Fallback feuert. Schick nicht nur einen Happy-Path-Prompt. Erzeuge den alten Failure Mode.

[NOVA]: Schritt sechs: Füge ein OpenAI-Token ein, starte das Gateway neu und bestätige, dass es persistiert hat. Vertraue, aber verifiziere.

[ALLOY]: Schritt sieben: Wenn du eigene Plugins hast, migriere von openclaw/extension-api zu openclaw/plugin-sdk/*. Lies die Migrationsdocs. Behandle Compiler-Fehler nicht wie eine Karte.

[NOVA]: Schritt acht: Mach einen Spot-Check der ClawHub-Skills nach der Verhaltensänderung bei der Installation. Stelle sicher, dass deine Skripte und Erwartungen immer noch zu dem passen, was aufgelöst wird.

[ALLOY]: Schritt neun: Verifiziere Cron-Jobs, die --at --tz verwenden, besonders wenn DST dich schon einmal erwischt hat.

[NOVA]: Die tiefere Zusammenfassung ist, dass diese beiden Releases zusammen OpenClaw dabei zeigen, wie es vollendet, was es begonnen hat. Die Namen Moltbot und Clawdbot sind weg. Das Extension-Relay ist weg. Das Plugin SDK ist vereinheitlicht. Die stillen Fehler sind behoben.

[ALLOY]: Zuerst Doctor --fix. Alles andere hängt davon ab, was du betreibst. Aber doctor --fix ist bedingungslos.

[NOVA]: Das ist die Plattform, die du wolltest, dass sie es ist.

[ALLOY]: Und ich denke, das ist der richtige Ton zum Beenden. Diese Releases sind fordernd, aber sie sind fordernd im Dienst von etwas Echtem: einer Plattform, die sagt, was sie ist, tut, was sie sagt, und weniger Geister aus früheren Epochen mit sich herumschleppt.

[NOVA]: Was bei einem Tool wie OpenClaw wichtiger ist als Neuheit. ... Zuverlässigkeit ist ein Feature. Konsistente Benennung ist ein Feature. Ehrlicher Migrationsdruck ist ein Feature. Ein Browser-Stack mit weniger improvisierten Brücken ist ein Feature.

[ALLOY]: Und wenn du gerade mitten im Upgrade steckst, hol tief Luft, mach die Checkliste, führe openclaw doctor --fix aus und überspringe die Verifikationsschritte nicht bloß, weil der Service wieder hochgekommen ist.

[NOVA]: Du findest die Show Notes, alle erwähnten Links und das Episodenarchiv unter tobyonfitnesstech.com. Das ist tobyonfitnesstech.com.

[ALLOY]: Wenn dich diese Episode vor einem kaputten Browser-Setup, einer verschwundenen Env Var oder einem weiteren mysteriösen Auth-Fehler bewahrt hat, dann hat sie ihren Job getan.

[ALLOY]: Ich bin Alloy.

[NOVA]: Und das war OpenClaw Daily. Wir sind bald zurück.