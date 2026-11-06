## Purpose

Wie spec-concordance zu den Nutzern kommt: Installation direkt aus dem GitHub-Repository ohne lokalen Klon, Aktualisierung über Releases, geschützter Verteilkanal.

## ADDED Requirements

### Requirement: Marktplatz-Datei im Repository (DI-001, Must)
Das Repository SHALL eine Datei `.claude-plugin/marketplace.json` enthalten mit `name`, `description`, `owner.name` (nur ein Name, keine E-Mail-Adresse) und genau einem Plugin-Eintrag. Der Eintrag SHALL denselben `name` tragen wie `.claude-plugin/plugin.json`, als `source` den Repository-Stamm `./` angeben und keine eigene `version` führen.

#### Scenario: Validierung mit Claude Code
- **WHEN** `claude plugin validate .` im Repository-Stamm ausgeführt wird
- **THEN** endet die Validierung ohne Fehler

> Manueller Test: Ausgabe mit Claude-Code-Version in der Test-Summary.

#### Scenario: Marktplatz-Datei passt zum Manifest
- **WHEN** die Tests ausgeführt werden
- **THEN** bestätigen sie Pflichtfelder, genau einen Eintrag, gleichen Namen, Quelle `./`, keine Version im Eintrag und keine E-Mail-Adresse im `owner`

#### Scenario: Name weicht ab
- **GIVEN** eine Marktplatz-Datei (Testdaten), deren Eintrag einen anderen `name` trägt als `plugin.json`
- **WHEN** die Prüfung der Marktplatz-Datei darauf angewendet wird
- **THEN** meldet sie den Widerspruch

### Requirement: Installation aus GitHub (DI-002, Must)
Das README (de und en) SHALL die Installation direkt aus dem GitHub-Repository beschreiben: den Einschritt-Befehl mit der nötigen Claude-Code-Version, die Zwei-Schritt-Variante, die Bestätigung in Claude Code, eine kurze Erklärung des Begriffs Marktplatz, den Zugriff bei einem privaten Repository mit minimalen Rechten und den Umstieg von der Klon-Installation. Es SHALL keinen lokalen Klon für die Installation verlangen.

#### Scenario: Befehle im README
- **WHEN** README.md und README.en.md gelesen werden
- **THEN** enthalten beide `/plugin install spec-concordance --marketplace JakobFlaman/spec-concordance`, `/plugin marketplace add JakobFlaman/spec-concordance` und `/plugin install spec-concordance@spec-concordance` und keinen Platzhalter `<owner>`

#### Scenario: Installation in sauberer Umgebung
- **GIVEN** eine Umgebung mit Claude Code ab 2.1.275 ohne installiertes spec-concordance
- **WHEN** der Einschritt-Befehl und in einer zweiten sauberen Umgebung die Zwei-Schritt-Variante ausgeführt werden
- **THEN** listet `claude plugin list` jeweils `spec-concordance@spec-concordance` als aktiviert

> Manueller Test nach festem Protokoll (`tasks.md` 4.1); Ergebnis in der Test-Summary.

### Requirement: Neues Projekt ohne Klon (DI-003, Must)
Der Schnellstart im README (de und en) SHALL ein neues Projekt in einem leeren Ordner mit `/spec-concordance:project-init` beginnen. Der Skill `project-init` SHALL jede Datei des Plugins (Vorlagen, `template-project/`, Prüfskript) über `${CLAUDE_PLUGIN_ROOT}` ansprechen.

#### Scenario: Kein Kopieren aus dem Klon
- **WHEN** der Abschnitt Schnellstart in README.md und README.en.md gelesen wird
- **THEN** enthält er weder `git clone` noch ein Kopieren von `template-project`

#### Scenario: project-init nutzt das Installationsverzeichnis
- **WHEN** `skills/project-init/SKILL.md` gelesen wird
- **THEN** beginnt jede Pfadangabe zu `templates/`, `template-project/` und `scripts/` mit `${CLAUDE_PLUGIN_ROOT}/`

#### Scenario: Dateien im installierten Plugin
- **GIVEN** ein aus GitHub installiertes Plugin
- **WHEN** im Installationsverzeichnis `templates/de/`, `template-project/` und `scripts/check-conventions.py` gesucht werden und das Prüfskript dort auf ein Testprojekt angewendet wird
- **THEN** sind die Dateien vorhanden und das Prüfskript läuft

> Manueller Test im Rahmen von `tasks.md` 4.1.

### Requirement: Prüfung in der CI (DI-004, Should)
Die CI des Plugins SHALL bei jedem Push auf `main` und bei jedem Pull Request die Prüfung der Marktplatz-Datei ausführen und bei einem Widerspruch fehlschlagen.

#### Scenario: CI-Lauf
- **WHEN** ein Pull Request geöffnet oder `main` aktualisiert wird
- **THEN** führt die CI die Tests einschliesslich der Prüfung der Marktplatz-Datei aus

> Nachweis: Run-ID eines grünen CI-Laufs in der Test-Summary.

### Requirement: Aktualisierung über Releases (DI-005, Must)
Die Version SHALL nur in `.claude-plugin/plugin.json` stehen, und das README (de und en) SHALL beschreiben, dass Nutzer neue Stände nur mit einem Release (Versionssprung) erhalten, mit welchem Befehl sie aktualisieren und wie sie die automatische Aktualisierung einschalten.

#### Scenario: Update-Anleitung
- **WHEN** README.md und README.en.md gelesen werden
- **THEN** enthalten beide `/plugin marketplace update spec-concordance` und den Hinweis, dass Neues nur mit einem Release kommt

### Requirement: Geschützter Verteilkanal (DI-006, Must)
Änderungen an `main` SHALL nur über Pull Requests mit grüner CI erfolgen. CLAUDE.md SHALL diese Arbeitsweise und die Einstellungen für den Branch-Schutz in GitHub beschreiben.

#### Scenario: Regel in CLAUDE.md
- **WHEN** CLAUDE.md gelesen wird
- **THEN** beschreibt sie die PR-Pflicht, die Freigabe G11 als Mergen und die Einstellungen für den Branch-Schutz

#### Scenario: Branch-Schutz aktiv
- **WHEN** der Schutz von `main` in GitHub abgefragt wird
- **THEN** verlangt er einen Pull Request und einen bestandenen Status-Check `checks`

> Manueller Test, sobald der Maintainer den Schutz eingerichtet hat; bis dahin als offen in der Test-Summary.
