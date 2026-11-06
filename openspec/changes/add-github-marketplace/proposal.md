# Proposal: Installation direkt aus GitHub

## Why

Der Schnellstart im README verlangt heute einen lokalen Klon des Repositorys und danach einen Umweg über das Plugin-Menü in Claude Code («lokales Plugin hinzufügen»). Für ein neues Projekt wird die Startvorlage zusätzlich aus dem Klon kopiert. Der Maintainer möchte, dass die Installation nicht über diesen Umweg führt, sondern direkt aus dem GitHub-Repository erfolgt und vollständig im README auf GitHub beschrieben ist.

Claude Code installiert Plugins aus einem *Marktplatz* (Plugin-Katalog). Ein Marktplatz ist ein Git-Repository mit der Datei `.claude-plugin/marketplace.json`. Ab Claude Code 2.1.275 genügt ein einziger Befehl, der Marktplatz und Plugin zusammen aus GitHub einbindet.

- **Klassifikation:** feature (Lücke – es gibt keine Anforderung zur Verteilung)
- **Quelle:** Wunsch des Maintainers vom 2026-11-06
- **Schweregrad:** entfällt

## What Changes

Neue Fähigkeit `distribution` (ADDED):

- Das Repository wird zugleich Marktplatz: `.claude-plugin/marketplace.json` listet das Plugin `spec-concordance` mit Quelle `./` (Repository-Stamm).
- README (de/en): Installation aus GitHub in einem Schritt, mit Zwei-Schritt-Variante für ältere Claude-Code-Versionen und Hinweis zum Zugriff auf das private Repository. Kein lokaler Klon mehr nötig.
- README (de/en): Ein neues Projekt startet in einem leeren Ordner mit `/spec-concordance:project-init`; die Startvorlage kommt aus dem installierten Plugin, nicht aus einem Klon.
- README (de/en): Aktualisieren über Releases, Umstieg von der Klon-Installation, Zugriff mit minimalen Rechten.
- `project-init` bezieht alle Plugin-Dateien über `${CLAUDE_PLUGIN_ROOT}` (das Installationsverzeichnis, das Claude Code in Plugin-Skills einsetzt).
- Tests prüfen, dass Marktplatz-Datei und Plugin-Manifest zusammenpassen; die CI läuft auch auf Pull Requests.
- `main` wird nur noch über Pull Requests mit grüner CI geändert (Entscheid des Maintainers nach dem Council-Review); die Freigabe G11 ist das Mergen.
- ADR 0001 hält den Grundsatzentscheid fest.

Nach dem Council-Review überarbeitet (Entscheidungsliste D1–D16 in `council-review.md`).

## Out of Scope

- Veröffentlichung im Plugin-Verzeichnis von Anthropic. (Das Repository ist öffentlich – Entscheid des Maintainers vom 2026-11-06.)
- Release 0.2.0 (Versionssprung in `plugin.json` und CHANGELOG) – eigener Schritt nach diesem Change und `define-gate-standard`. Bis dahin trägt jede Installation die Version 0.1.0, auch wenn sie einen anderen Stand von `main` enthält; installierte Kopien werden erst mit dem Versionssprung aktualisiert.
- Einrichten des Branch-Schutzes in GitHub – macht der Maintainer; dieser Change beschreibt die Einstellungen.
- `source-hash`-Kopf für README.en.md und Prüfung der READMEs durch `check-i18n.py` – Folge-Change (D16).
- Automatische Aktualisierung bei Nutzern (Einstellung in Claude Code, nicht im Repository).
