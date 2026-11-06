## Purpose

Regeln für das Qualitäts-Gate, damit sein Ergebnis vorhersehbar ist: fester Massstab, früh festgelegte Grenzen, Eskalation statt endloser Schlaufe.

## ADDED Requirements

### Requirement: Massstab für Spezifikation und Verhalten (QG-001, Must)
Der Skill `quality-gate` SHALL Gate-Punkt G7 als «Spezifikation stimmt mit dem Verhalten überein» festlegen und ihn nur dann als nicht erfüllt werten, wenn eine ausdrückliche Zusage von Spec oder Design gebrochen wird oder ein Verstoss gegen eine Anforderung realistisch und still durchgeht. Realistisch heisst: Der Fall kann bei der normalen Arbeit entstehen.

#### Scenario: Realistischer stiller Verstoss
- **GIVEN** ein Change, dessen Prüfung einen beim normalen Arbeiten entstehenden Verstoss ohne Meldung durchlässt
- **WHEN** das Qualitäts-Gate nach dem Skill ausgeführt wird
- **THEN** ist G7 ❌ und das Gate nicht bestanden

#### Scenario: Regel im Skill
- **WHEN** `skills/quality-gate/SKILL.md` gelesen wird
- **THEN** enthält er den Massstab für G7

### Requirement: Einordnung der Befunde (QG-002, Must)
Jeder G7-Befund SHALL als «realistisch» oder «konstruiert» eingeordnet werden. Absichtlich konstruierte Fälle (Verschleierung) und Fälle innerhalb dokumentierter Grenzen SHALL als Beobachtung geführt werden und machen G7 nicht ❌.

#### Scenario: Konstruierter Fall
- **GIVEN** ein Befund, der nur durch absichtliche Verschleierung entsteht oder unter eine in `design.md` dokumentierte Grenze fällt
- **WHEN** das Qualitäts-Gate nach dem Skill ausgeführt wird
- **THEN** wird der Befund als Beobachtung mit der Einordnung «konstruiert» geführt und G7 nicht deswegen ❌

#### Scenario: Pflicht im Skill
- **WHEN** `skills/quality-gate/SKILL.md` gelesen wird
- **THEN** verlangt er die Einordnung «realistisch» / «konstruiert» für jeden G7-Befund

### Requirement: Grenzen vor der Umsetzung (QG-003, Must)
Der Skill `change-proposal` SHALL für Changes mit Prüf-, Erkennungs- oder Automatisierungslogik einen Abschnitt «Grenzen» in `design.md` verlangen, der vor dem Council-Review benennt, was bewusst nicht abgedeckt ist. Zusagen ohne Ausnahme («nie», «immer», «in jedem Fall») SHALL nur zusammen mit einem Vergleichsmassstab und den Grenzen stehen.

#### Scenario: Regel im Skill
- **WHEN** `skills/change-proposal/SKILL.md` gelesen wird
- **THEN** verlangt er den Abschnitt «Grenzen» und die Regel für absolute Zusagen

#### Scenario: Change ohne Grenzen
- **GIVEN** ein Change mit Prüflogik, dessen `design.md` keinen Abschnitt «Grenzen» hat
- **WHEN** das Council-Review nach dem Skill `council-review` durchgeführt wird
- **THEN** führt mindestens die Rolle Testmanagement das Fehlen als Befund mit Schweregrad `major`

### Requirement: Eskalation bei wiederholtem Scheitern (QG-004, Should)
Scheitert das Qualitäts-Gate dreimal in Folge am selben Gate-Punkt und derselben Anforderung, SHALL vor dem nächsten Lauf der Maintainer gefragt werden, ob der Massstab gilt, angepasst wird oder die Befunde als Grenze dokumentiert werden.

#### Scenario: Dritter Fehlschlag
- **GIVEN** drei aufeinanderfolgende nicht bestandene Gate-Läufe mit Befunden zu G7 und RC-001
- **WHEN** ein vierter Lauf angestossen werden soll
- **THEN** fragt der Agent zuerst den Maintainer nach dem Massstab und hält die Antwort im Change fest
