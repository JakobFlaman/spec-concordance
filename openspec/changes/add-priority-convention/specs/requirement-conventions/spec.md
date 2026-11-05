## Purpose

Einheitliche Form von Anforderungen in OpenSpec-Spezifikationen von Projekten nach spec-concordance, damit sie OpenSpec-konform validieren und ihre MoSCoW-Priorität sowie ihre Herkunft erhalten bleiben.

## ADDED Requirements

### Requirement: SHALL unabhängig von der Priorität (RC-001, Must)
Jede Anforderung in einer OpenSpec-Spezifikation SHALL mit dem Schlüsselwort SHALL formuliert sein; SHOULD und MAY werden in Anforderungstexten nicht verwendet.

#### Scenario: Should-Anforderung validiert
- **GIVEN** eine Anforderung mit Priorität Should, formuliert mit SHALL und Priorität im Titel
- **WHEN** `openspec validate <change> --strict` ausgeführt wird
- **THEN** meldet OpenSpec weder Fehler noch Warnung zu dieser Anforderung

#### Scenario: SHOULD im Anforderungstext
- **GIVEN** eine Anforderung, deren Text «SHOULD» oder «MAY» als Schlüsselwort enthält
- **WHEN** `scripts/check-conventions.py` ausgeführt wird
- **THEN** meldet die Prüfung die Anforderung mit Datei und Titel und endet mit Exitcode ungleich 0

### Requirement: ID und Priorität im Titel (RC-002, Must)
Der Titel jeder Anforderung SHALL die Form `<Titel> (<ID>, <Priorität>)` haben, wobei die Priorität `Must`, `Should` oder `Could` ist und die ID der stabilen Kennung in der Anforderungsquelle des Projekts entspricht.

#### Scenario: Korrekter Titel
- **GIVEN** der Titel «Darstellungsmodi (LA-F-110, Should)»
- **WHEN** `scripts/check-conventions.py` ausgeführt wird
- **THEN** wird der Titel akzeptiert

#### Scenario: Fehlende Priorität
- **GIVEN** der Titel «Seitenleiste (LA-F-104)»
- **WHEN** `scripts/check-conventions.py` ausgeführt wird
- **THEN** meldet die Prüfung «Priorität fehlt» mit Datei und Titel und endet mit Exitcode ungleich 0

#### Scenario: Unbekannte Priorität
- **GIVEN** der Titel «Export (LA-F-308, Wichtig)»
- **WHEN** `scripts/check-conventions.py` ausgeführt wird
- **THEN** meldet die Prüfung «Priorität muss Must, Should oder Could sein»

### Requirement: Gemischte Priorität wird getrennt (RC-003, Must)
Eine Quellanforderung mit gemischter Priorität (z. B. «Must / Should») SHALL in je eine OpenSpec-Anforderung pro Priorität getrennt werden, die dieselbe ID tragen.

#### Scenario: Must/Should-Quelle
- **GIVEN** die Quellanforderung LA-F-105 mit Priorität «Must / Should»
- **WHEN** sie in OpenSpec überführt wird
- **THEN** entstehen zwei Anforderungen mit den Titeln «… (LA-F-105, Must)» und «… (LA-F-105, Should)»
- **AND** `scripts/check-conventions.py` akzeptiert eine ID, die mit unterschiedlichen Prioritäten mehrfach vorkommt, meldet aber dieselbe ID mit derselben Priorität doppelt

### Requirement: Regel beim Projektstart verankert (RC-004, Must)
Der Skill `project-init` SHALL die Konvention beim Initialisieren von OpenSpec in den `context` von `openspec/config.yaml` des Projekts eintragen.

#### Scenario: Neues Projekt
- **GIVEN** ein neues Projekt, in dem `project-init` OpenSpec initialisiert hat
- **WHEN** `openspec/config.yaml` gelesen wird
- **THEN** enthält der `context` die Regeln RC-001 bis RC-003 in Kurzform

### Requirement: Prüfung in der CI (RC-005, Should)
Das Plugin SHALL `scripts/check-conventions.py` so bereitstellen, dass Projekte es in ihrer CI auf `openspec/specs/` und `openspec/changes/` ausführen können; das Plugin-Repository führt es auf seine eigenen Spezifikationen aus.

#### Scenario: Plugin-CI
- **WHEN** ein Pull Request im Plugin-Repository erstellt wird
- **THEN** führt die CI `scripts/check-conventions.py` aus und schlägt bei einer Verletzung fehl
