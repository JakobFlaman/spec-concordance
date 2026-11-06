# change-process Specification

## Purpose
Regeln für den Weg eines Changes vom Proposal bis zum Archiv, damit das Ergebnis des Qualitäts-Gates vorhersehbar ist: fester Massstab, früh festgelegte Grenzen, nachvollziehbarer Gate-Verlauf, Eskalation statt endloser Schlaufe.

## Requirements

### Requirement: Massstab für Spezifikation und Verhalten (CP-001, Must)
Der Skill `quality-gate` SHALL Gate-Punkt G7 «Spezifikation nachgeführt und stimmt mit dem Verhalten überein» mit zwei Teilen prüfen: (a) die Spec-Deltas sind vollständig und widerspruchsfrei, (b) keine ausdrückliche Zusage von Spec oder Design wird gebrochen und kein Verstoss gegen eine Anforderung geht realistisch und still durch. Realistisch heisst: Der Fall kann bei der normalen Arbeit entstehen.

#### Scenario: Regel im Skill
- **WHEN** `skills/quality-gate/SKILL.md` gelesen wird
- **THEN** enthält die Zeile G7 beide Teile (a) und (b) und die Definition von «realistisch»

#### Scenario: Realistischer stiller Verstoss
- **GIVEN** der Befund aus Gate-Lauf 17 von `add-priority-convention` (versetzte Codezäune nach einem eingerückten Schliesser, Exit 0)
- **WHEN** ein unabhängiger Prüfer ihn nach dem Skill einordnet
- **THEN** ordnet er ihn als «realistisch» ein und wertet G7 als ❌

> Manueller Test: Einordnungsprobe mit unabhängigem Agenten, Ergebnis in der Test-Summary.

### Requirement: Einordnung der Befunde (CP-002, Must)
Jeder G7-Befund SHALL als «realistisch» oder «konstruiert» eingeordnet werden; im Zweifel gilt «realistisch». Konstruiert ist ein Fall, der nur durch absichtliche Verschleierung entsteht. Konstruierte Fälle und Fälle innerhalb einer gültigen Grenze SHALL als Beobachtung geführt werden; eine Beobachtung hat keinen Schweregrad und macht G7 nicht ❌.

#### Scenario: Pflicht im Skill
- **WHEN** `skills/quality-gate/SKILL.md` gelesen wird
- **THEN** verlangt er die Einordnung «realistisch» / «konstruiert», die Zweifelsregel und definiert «Beobachtung»

#### Scenario: Konstruierter Fall
- **GIVEN** der Befund aus Gate-Lauf 18 von `add-priority-convention` (`SH<!-- > -->OULD`)
- **WHEN** ein unabhängiger Prüfer ihn nach dem Skill einordnet
- **THEN** ordnet er ihn als «konstruiert» ein und führt ihn als Beobachtung

> Manueller Test: Einordnungsprobe mit unabhängigem Agenten, Ergebnis in der Test-Summary.

### Requirement: Gültige Grenzen und Sicherheitszweck (CP-003, Must)
Als gültige Grenze SHALL nur gelten, was beim Council-Review bereits in `design.md` stand oder was der Maintainer später ausdrücklich als Grenze bestätigt hat, festgehalten im Gate-Protokoll. Bei Anforderungen mit Sicherheitszweck (Klassifikation `security` oder Befund der Rolle Security) SHALL ein konstruierter Fall als realistisch gelten, ausser er ist als Grenze dokumentiert und die Rolle Security hat ihr im Council zugestimmt.

#### Scenario: Regel im Skill
- **WHEN** `skills/quality-gate/SKILL.md` gelesen wird
- **THEN** enthält er die Regel für gültige Grenzen und die Ausnahme für den Sicherheitszweck

### Requirement: Entscheide des Maintainers (CP-004, Must)
Der Maintainer SHALL eine Einordnung umstufen oder einen realistischen Befund mit Begründung in einen Folge-Change verschieben können; jeder solche Entscheid SHALL mit Begründung im Gate-Protokoll stehen. Ohne festgehaltenen Entscheid bleibt ein realistischer Befund ❌.

#### Scenario: Regel im Skill
- **WHEN** `skills/quality-gate/SKILL.md` gelesen wird
- **THEN** beschreibt er Umstufung und Verschiebung durch den Maintainer und die Pflicht, sie im Gate-Protokoll festzuhalten

### Requirement: Grenzen vor der Umsetzung (CP-005, Must)
Der Skill `change-proposal` SHALL für Changes, deren Ergebnis eine automatische Prüfung, Erkennung oder Entscheidung ist (z. B. Prüfskripte, Validierungsregeln, Gate-Kriterien), einen Abschnitt «Grenzen» in `design.md` vor dem Council-Review verlangen; ob ein Change darunter fällt, entscheidet das Council, im Zweifel gilt die Pflicht. Zusagen ohne Ausnahme («nie», «immer», «in jedem Fall») SHALL nur mit Vergleichsmassstab und Grenzen stehen.

#### Scenario: Regel im Skill
- **WHEN** `skills/change-proposal/SKILL.md` gelesen wird
- **THEN** verlangt er den Abschnitt «Grenzen» mit Geltungsbereich, Beispielen und Entscheidungsinstanz sowie die Regel für absolute Zusagen

#### Scenario: Prüffrage der Rolle Testmanagement
- **WHEN** `agents/council-test-management.md` gelesen wird
- **THEN** enthält die Rolle die Prüffrage nach dem Abschnitt «Grenzen» mit Schweregrad `major` bei Fehlen

#### Scenario: Change ohne Grenzen
- **GIVEN** ein synthetischer Change mit Prüfskript, dessen `design.md` keinen Abschnitt «Grenzen» hat
- **WHEN** die Rolle Testmanagement ihn nach ihrer Rollendatei prüft
- **THEN** führt sie das Fehlen als Befund mit Schweregrad `major`

> Manueller Test: Probe-Review mit unabhängigem Agenten, Ergebnis in der Test-Summary.

### Requirement: Gate-Protokoll (CP-006, Must)
Jeder Gate-Lauf SHALL in `openspec/changes/<id>/gate-log.md` festgehalten werden: Laufnummer, Datum, Ergebnis, nicht erfüllte Gate-Punkte mit betroffener Anforderung, Einordnung der G7-Befunde und Entscheide des Maintainers; die Dauer ist optional. Der Skill `quality-gate` SHALL das Protokoll vor jedem Lauf lesen.

#### Scenario: Regel im Skill
- **WHEN** `skills/quality-gate/SKILL.md` gelesen wird
- **THEN** verlangt er das Gate-Protokoll mit diesen Feldern und das Lesen vor jedem Lauf

### Requirement: Eskalation bei wiederholtem Scheitern (CP-007, Should)
Ist in drei aufeinanderfolgenden Gate-Läufen derselbe Gate-Punkt ❌ – bei G3 und G7 zusätzlich zur selben Anforderung –, SHALL vor dem nächsten Lauf der Maintainer gefragt werden, ob der Massstab gilt, angepasst wird oder Befunde als Grenze bestätigt werden; die Antwort SHALL im Gate-Protokoll stehen und setzt die Zählung zurück.

#### Scenario: Regel im Skill
- **WHEN** `skills/quality-gate/SKILL.md` gelesen wird
- **THEN** enthält er die Zählregel und die Pflicht zur Frage an den Maintainer

#### Scenario: Dritter Fehlschlag
- **GIVEN** ein synthetisches Gate-Protokoll mit drei aufeinanderfolgenden nicht bestandenen Läufen, jeweils G7 zu RC-001
- **WHEN** ein unabhängiger Agent nach dem Skill einen vierten Lauf vorbereitet
- **THEN** fragt er zuerst den Maintainer nach dem Massstab, statt den Lauf zu starten

> Manueller Test: Probe mit unabhängigem Agenten, Ergebnis in der Test-Summary.
