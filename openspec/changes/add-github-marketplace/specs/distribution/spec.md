## Purpose

Wie spec-concordance zu den Nutzern kommt: Installation direkt aus dem GitHub-Repository, ohne lokalen Klon.

## ADDED Requirements

### Requirement: Marktplatz-Datei im Repository (DI-001, Must)
Das Repository SHALL eine Datei `.claude-plugin/marketplace.json` enthalten, die einen Marktplatz mit `name`, `owner` und genau einem Plugin-Eintrag beschreibt. Der Eintrag SHALL denselben `name` tragen wie `.claude-plugin/plugin.json`, als `source` den Repository-Stamm `./` angeben und keine eigene `version` führen.

#### Scenario: Validierung mit Claude Code
- **WHEN** `claude plugin validate .` im Repository-Stamm ausgeführt wird
- **THEN** endet die Validierung ohne Fehler

#### Scenario: Name weicht ab
- **GIVEN** eine Marktplatz-Datei, deren Eintrag einen anderen `name` trägt als `plugin.json`
- **WHEN** die Tests ausgeführt werden
- **THEN** schlägt die Prüfung der Marktplatz-Datei fehl

### Requirement: Installation aus GitHub (DI-002, Must)
Das README (de und en) SHALL die Installation direkt aus dem GitHub-Repository beschreiben: den Einschritt-Befehl mit der nötigen Claude-Code-Version, die Zwei-Schritt-Variante und den Zugriff auf das private Repository. Es SHALL keinen lokalen Klon für die Installation verlangen.

#### Scenario: Befehle im README
- **WHEN** README.md und README.en.md gelesen werden
- **THEN** enthalten beide den Einschritt-Befehl und die Zwei-Schritt-Variante mit `JakobFlaman/spec-concordance` und keinen Platzhalter `<owner>`

#### Scenario: Installation in sauberer Umgebung
- **GIVEN** eine Umgebung mit Claude Code ab 2.1.275 und Lesezugriff auf das Repository, ohne installiertes spec-concordance
- **WHEN** der Einschritt-Befehl aus dem README ausgeführt wird
- **THEN** listet `claude plugin list` das Plugin `spec-concordance@spec-concordance` als aktiviert (manueller Test im Qualitäts-Gate)

### Requirement: Neues Projekt ohne Klon (DI-003, Must)
Der Schnellstart im README (de und en) SHALL ein neues Projekt in einem leeren Ordner mit `/spec-concordance:project-init` beginnen; Vorlagen und Startvorlage SHALL aus dem installierten Plugin stammen, nicht aus einer Kopie eines Klons.

#### Scenario: Kein Kopieren aus dem Klon
- **WHEN** der Schnellstart in README.md und README.en.md gelesen wird
- **THEN** enthält er weder `git clone` noch ein Kopieren von `template-project`

#### Scenario: project-init nutzt das Plugin
- **WHEN** `skills/project-init/SKILL.md` gelesen wird
- **THEN** bezieht der Skill Vorlagen, `openspec-context.md` und `CLAUDE.md` aus dem Plugin-Verzeichnis

### Requirement: Prüfung in der CI (DI-004, Should)
Die CI des Plugins SHALL bei jedem Push prüfen, dass Marktplatz-Datei und Plugin-Manifest zusammenpassen (Pflichtfelder, gleicher Name, Quelle `./`, keine Version im Eintrag).

#### Scenario: CI-Lauf
- **WHEN** ein Commit auf `main` gepusht wird
- **THEN** führt die CI die Prüfung der Marktplatz-Datei aus und schlägt bei einem Widerspruch fehl
