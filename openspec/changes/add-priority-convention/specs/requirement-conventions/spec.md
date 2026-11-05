## Purpose

Einheitliche Form von Anforderungen in OpenSpec-Spezifikationen von Projekten nach spec-concordance, damit sie OpenSpec-konform validieren und ihre MoSCoW-Priorität sowie ihre Herkunft erhalten bleiben. Gilt für funktionale und nicht-funktionale Anforderungen gleichermassen.

## ADDED Requirements

### Requirement: SHALL unabhängig von der Priorität (RC-001, Must)
Der Anforderungstext jeder Anforderung SHALL das Schlüsselwort SHALL verwenden und kein anderes RFC-2119-Schlüsselwort für Empfehlung oder Option (`SHOULD`, `MAY`). Als Anforderungstext gilt der Text, den OpenSpec der Anforderung zuordnet (ohne Szenarien und ohne Codeblöcke); als Schlüsselwort gilt das grossgeschriebene ganze Wort, wie es dargestellt wird. Inline-Code und Zitate («…», “…”, „…“) sind nur bei sicheren Grenzen eine Erwähnung; sonst wird gemeldet.

#### Scenario: Should-Anforderung validiert
- **GIVEN** eine Anforderung mit Priorität Should, formuliert mit SHALL und Priorität im Titel
- **WHEN** `openspec validate <change> --strict` ausgeführt wird
- **THEN** meldet OpenSpec weder Fehler noch Warnung zu dieser Anforderung

#### Scenario: Empfehlungs-Schlüsselwort im Anforderungstext
- **GIVEN** eine Anforderung, deren Anforderungstext das grossgeschriebene Wort `SHOULD` ausserhalb von Code und Zitat enthält
- **WHEN** `scripts/check-conventions.py` ausgeführt wird
- **THEN** meldet die Prüfung RC-001 mit Datei, Zeile und Titel und endet mit Exitcode 1

#### Scenario: Erwähnung ist kein Verstoss
- **GIVEN** eine Anforderung, die `SHOULD` nur in Backticks, in einem Codeblock oder in «…» bzw. „…“ erwähnt, oder ein Szenario, das das Wort enthält
- **WHEN** `scripts/check-conventions.py` ausgeführt wird
- **THEN** wird die Anforderung akzeptiert

#### Scenario: Inline-Code oder Zitat über einen Zeilenumbruch
- **GIVEN** eine Anforderung, die `SHOULD` in Inline-Code oder in einem Zitat erwähnt, das über einen Zeilenumbruch oder eine Absatzgrenze läuft
- **WHEN** `scripts/check-conventions.py` ausgeführt wird
- **THEN** meldet die Prüfung RC-001 (im Zweifel melden; Abhilfe: Erwähnung auf eine Zeile setzen)

#### Scenario: Unsichere Code-Grenzen
- **GIVEN** eine Anforderung, deren Text einen Backslash, `<` oder `[` enthält oder einen Backtick-Lauf ohne Gegenstück auf derselben Zeile, und die `SHOULD` ausserhalb von «…» enthält
- **WHEN** `scripts/check-conventions.py` ausgeführt wird
- **THEN** meldet die Prüfung RC-001, auch wenn `SHOULD` nach CommonMark in Code stünde

#### Scenario: Unsichere Zitatgrenzen
- **GIVEN** eine Anforderung mit Zitaten, deren Text eine Zeichenreferenz (`&`) enthält oder in der ein Anführungszeichen ohne Gegenstück bleibt, und die `SHOULD` ausserhalb von Inline-Code enthält
- **WHEN** `scripts/check-conventions.py` ausgeführt wird
- **THEN** meldet die Prüfung RC-001

#### Scenario: Schlüsselwort erst in der Darstellung
- **GIVEN** eine Anforderung, in der `SHOULD` erst bei der Darstellung entsteht, etwa aus einer Zeichenreferenz (`&#83;HOULD`) oder durch Hervorhebung, HTML oder unsichtbare Zeichen zerteilt (`SH*OUL*D`)
- **WHEN** `scripts/check-conventions.py` ausgeführt wird
- **THEN** meldet die Prüfung RC-001

#### Scenario: Unsicherer Codeblock
- **GIVEN** eine Spec-Datei mit einem Codeblock, in dem `SHOULD` steht und dessen Zaun eingerückt ist (z. B. unter einem Listenpunkt), dem ein eingerückter Zaun vorausgeht oder eine Zeile mit `<` oder `[` am Anfang
- **WHEN** `scripts/check-conventions.py` ausgeführt wird
- **THEN** meldet die Prüfung RC-001 auf der Zeile des Zauns, weil OpenSpec den Block ausblendet und CommonMark ihn womöglich als Text liest

#### Scenario: Gerade Anführungszeichen
- **GIVEN** eine Anforderung, in der `SHOULD` zwischen geraden Anführungszeichen steht, etwa als Zollzeichen
- **WHEN** `scripts/check-conventions.py` ausgeführt wird
- **THEN** meldet die Prüfung RC-001

#### Scenario: Kein stiller Durchlass gegenüber CommonMark
- **GIVEN** ein Anforderungstext, in dem `SHOULD` nach CommonMark ausserhalb von Inline-Code und «…», “…”, „…“ steht
- **WHEN** die Erkennung mit einem CommonMark-Parser verglichen wird (`tests/fuzz/`)
- **THEN** meldet die Prüfung RC-001 in jedem Fall

#### Scenario: Plugin besteht die eigene Prüfung
- **WHEN** `scripts/check-conventions.py` im Plugin-Repository ausgeführt wird
- **THEN** endet die Prüfung mit Exitcode 0

### Requirement: ID und Priorität im Titel (RC-002, Must)
Der Titel jeder Anforderung SHALL die Form `<Titel> (<ID>, <Priorität>)` haben. Die Priorität ist `Must`, `Should` oder `Could`; Won't-Anforderungen werden nicht in OpenSpec geführt, sondern in der Roadmap. Die ID entspricht dem Formatmuster `[A-Z][A-Z0-9]*(-[A-Z0-9]+)*-[0-9]+` (überschreibbar); dass sie der Kennung in der Anforderungsquelle entspricht, prüft das Council, nicht das Skript.

#### Scenario: Korrekter Titel
- **GIVEN** der Titel «Darstellungsmodi (LA-F-110, Should)»
- **WHEN** `scripts/check-conventions.py` ausgeführt wird
- **THEN** wird der Titel akzeptiert

#### Scenario: Fehlende Priorität
- **GIVEN** der Titel «Seitenleiste (LA-F-104)»
- **WHEN** `scripts/check-conventions.py` ausgeführt wird
- **THEN** meldet die Prüfung RC-002 «Priorität fehlt» mit Datei, Zeile und Titel und endet mit Exitcode 1

#### Scenario: Unbekannte Priorität
- **GIVEN** der Titel «Export (LA-F-308, Wichtig)»
- **WHEN** `scripts/check-conventions.py` ausgeführt wird
- **THEN** meldet die Prüfung RC-002 «Priorität muss Must, Should oder Could sein»

### Requirement: Gemischte Priorität wird getrennt (RC-003, Must)
Eine Quellanforderung mit gemischter Priorität (z. B. «Must / Should») SHALL in je eine OpenSpec-Anforderung pro Priorität getrennt werden, die dieselbe ID tragen. Geht aus der Quelle nicht eindeutig hervor, welcher Teil welche Priorität hat, wird die Zuordnung als offener Punkt beim Maintainer erfragt, nicht geraten.

#### Scenario: Must/Should-Quelle
> Manueller Test: Die Überführung ist eine Arbeitsregel für den Agenten, kein Skriptverhalten. Nachweis anhand eines realen Projekts.
- **GIVEN** die Quellanforderung LA-F-105 mit Priorität «Must / Should»
- **WHEN** sie in OpenSpec überführt wird
- **THEN** entstehen zwei Anforderungen mit den Titeln «… (LA-F-105, Must)» und «… (LA-F-105, Should)»

#### Scenario: Regel im Textbaustein
- **WHEN** der Test der Plugin-Vorlagen läuft
- **THEN** enthält `template-project/openspec-context.md` die Trennregel inklusive «ask the maintainer instead of guessing», und `skills/project-init/SKILL.md` enthält die Anweisung, bei unklarer Aufteilung beim Maintainer nachzufragen

### Requirement: Eindeutigkeit von ID und Priorität (RC-007, Must)
Innerhalb einer Spec-Datei SHALL jede Kombination aus ID und Priorität nur einmal vorkommen. Geprüft werden Basis-Specs sowie ADDED- und MODIFIED-Deltas aktiver Changes, nicht REMOVED, RENAMED und archivierte Changes.

#### Scenario: Duplikat in einer Datei
- **GIVEN** eine Spec-Datei mit zwei Anforderungen, die beide «(LA-F-105, Must)» tragen
- **WHEN** `scripts/check-conventions.py` ausgeführt wird
- **THEN** meldet die Prüfung RC-007 für die zweite Anforderung und endet mit Exitcode 1

#### Scenario: Gleiche ID mit zwei Prioritäten
- **GIVEN** eine Spec-Datei mit «(LA-F-105, Must)» und «(LA-F-105, Should)»
- **WHEN** `scripts/check-conventions.py` ausgeführt wird
- **THEN** werden beide akzeptiert

### Requirement: Priorität ändern über RENAMED (RC-004, Must)
Eine Umpriorisierung SHALL als RENAMED-Delta mit FROM/TO erfasst werden, weil der Titel die Anforderung identifiziert. Ein MODIFIED-Abschnitt, dessen Titel weder in der Basis-Spezifikation noch als TO-Titel eines RENAMED im selben Change existiert, sich von einem bestehenden Titel aber nur in der Priorität unterscheidet, wird von der Prüfung mit Hinweis auf RENAMED gemeldet. Umpriorisieren und inhaltlich ändern im selben Change ist erlaubt (RENAMED plus MODIFIED auf den neuen Titel).

#### Scenario: Should wird Must
- **GIVEN** die Basis-Anforderung «Darstellungsmodi (LA-F-110, Should)» in `openspec/specs/<cap>/spec.md`
- **WHEN** ein Change sie mit `## RENAMED Requirements`, `FROM: ### Requirement: Darstellungsmodi (LA-F-110, Should)` und `TO: ### Requirement: Darstellungsmodi (LA-F-110, Must)` umbenennt
- **THEN** akzeptiert `scripts/check-conventions.py` den Change

#### Scenario: Umpriorisierung fälschlich als MODIFIED
- **GIVEN** dieselbe Basis-Anforderung
- **WHEN** ein Change unter `## MODIFIED Requirements` den Titel «Darstellungsmodi (LA-F-110, Must)» führt
- **THEN** meldet die Prüfung RC-004 mit dem Hinweis, RENAMED zu verwenden, und endet mit Exitcode 1

#### Scenario: Umpriorisieren und ändern im selben Change
- **GIVEN** dieselbe Basis-Anforderung
- **WHEN** ein Change sie per RENAMED auf «Darstellungsmodi (LA-F-110, Must)» umbenennt und unter `## MODIFIED Requirements` denselben neuen Titel inhaltlich ändert
- **THEN** akzeptiert `scripts/check-conventions.py` den Change

### Requirement: Regel beim Projektstart verankert (RC-005, Must)
Der Skill `project-init` SHALL nach `openspec init` den Textbaustein `template-project/openspec-context.md` an den `context` in `openspec/config.yaml` des Projekts anfügen, ohne bestehenden Inhalt zu überschreiben und ohne ihn bei wiederholtem Lauf doppelt einzutragen. Must-, Should- und Could-Anforderungen werden überführt.

#### Scenario: Textbaustein vollständig
- **WHEN** der Test der Plugin-Vorlagen läuft
- **THEN** enthält `template-project/openspec-context.md` die Regeln RC-001 bis RC-004 und RC-007 in Kurzform mit Markierung `spec-concordance:requirement-conventions`
- **AND** `skills/project-init/SKILL.md` verweist auf den Textbaustein und auf die Prüfung, ob die Markierung bereits vorhanden ist

#### Scenario: Bestehender Kontext
> Manueller Test, nicht automatisierbar (KI-Lauf von `project-init`).
- **GIVEN** ein Projekt, dessen `openspec/config.yaml` bereits einen `context` mit Sprachangabe hat
- **WHEN** `project-init` zweimal ausgeführt wird
- **THEN** bleibt die Sprachangabe erhalten und der Baustein steht genau einmal im `context`

### Requirement: Prüfung im Plugin-Repository (RC-006, Should)
Das Plugin-Repository SHALL `scripts/check-conventions.py` in seiner CI ausführen. Die Bereitstellung der Prüfung für die CI von Projekten ist ein eigener Change.

#### Scenario: Plugin-CI
- **WHEN** ein Pull Request im Plugin-Repository erstellt wird
- **THEN** führt die CI die Prüfung im Projektstamm aus, prüft keine Testdaten unter `tests/` und schlägt bei einer Verletzung fehl

#### Scenario: Übergangsmodus
- **GIVEN** ein bestehendes Projekt mit Titeln ohne Priorität
- **WHEN** die Prüfung mit `--warn` ausgeführt wird
- **THEN** meldet sie alle Verstösse, endet aber mit Exitcode 0

### Requirement: Erkennung über OpenSpec (RC-008, Must)
Die Prüfung SHALL Struktur, Namen und Texte von Anforderungen ausschliesslich über die OpenSpec-CLI (ab Version 1.16) ermitteln, damit sie dieselben Anforderungen sieht wie OpenSpec; die Spec-Datei wird nur zur Zuordnung der Zeilennummer gelesen. Fehlt die CLI, ist sie zu alt, meldet sie einen Fehler oder liefert sie eine unerwartete Struktur, endet die Prüfung mit Exitcode 2 und einer Meldung mit Handlungsempfehlung.

#### Scenario: Verschachtelte Capability
- **GIVEN** eine Basis-Anforderung «Darstellungsmodi (LA-F-110, Should)» unter `openspec/specs/area/cap/spec.md`
- **WHEN** ein Change unter `specs/area/cap/spec.md` den Titel «Darstellungsmodi (LA-F-110, Must)» als MODIFIED führt
- **THEN** meldet die Prüfung RC-004 und endet mit Exitcode 1

#### Scenario: Basis-Anforderung ohne Präfix
- **GIVEN** eine Basis-Spec, deren Anforderung als `### Seitenleiste (LA-F-104)` ohne «Requirement:» geschrieben ist und die OpenSpec als Anforderung liest
- **WHEN** die Prüfung ausgeführt wird
- **THEN** meldet sie RC-002 «Priorität fehlt» und endet mit Exitcode 1

#### Scenario: OpenSpec fehlt
- **GIVEN** die OpenSpec-CLI ist nicht auffindbar
- **WHEN** die Prüfung ausgeführt wird
- **THEN** endet sie mit Exitcode 2 und der Meldung, dass OpenSpec benötigt wird

#### Scenario: OpenSpec meldet einen Fehler
- **GIVEN** ein Change ohne `proposal.md`
- **WHEN** die Prüfung ausgeführt wird
- **THEN** endet sie mit Exitcode 2 und gibt die Fehlermeldung von OpenSpec mit dem Namen des Changes aus

#### Scenario: OpenSpec zu alt
- **GIVEN** eine OpenSpec-CLI, die eine Version unter 1.16 meldet
- **WHEN** die Prüfung ausgeführt wird
- **THEN** endet sie mit Exitcode 2 und nennt die gefundene und die benötigte Version

#### Scenario: Unerwartete Struktur
- **GIVEN** eine OpenSpec-CLI, deren JSON-Ausgabe ein erwartetes Feld nicht enthält
- **WHEN** die Prüfung ausgeführt wird
- **THEN** endet sie mit Exitcode 2 und nennt das betroffene Spec oder den Change, statt «OK» zu melden

#### Scenario: Ordner ohne openspec/
- **WHEN** die Prüfung mit `openspec/specs` statt mit dem Projektstamm aufgerufen wird
- **THEN** endet sie mit Exitcode 2 und dem Hinweis, den Projektstamm anzugeben
