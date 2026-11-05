# Tasks: Prioritätskonvention

Version: Änderungen werden unter [Unreleased] gesammelt; `plugin.json` wird beim nächsten Release nachgezogen (D16).

## 1. Prüfung (zuerst, damit die Abnahmekriterien testbar sind)

- [x] 1.1 `scripts/check-conventions.py` nach der Schnittstelle in `design.md` (Erkennungsregel RC-001, Titel RC-002, Duplikate RC-007, Umpriorisierung RC-004, Exitcodes 0/1/2, `--warn`, `--id-pattern`; nur Standardbibliothek, nur lesend)
- [x] 1.2 Testdaten `tests/fixtures/conventions/` und `tests/test_check_conventions.py` (unittest): gültig, Priorität fehlt, unbekannte Priorität, SHOULD im Text, SHOULD als Erwähnung (Code, Zitat, Szenario), Duplikat, gleiche ID mit zwei Prioritäten, RENAMED korrekt, MODIFIED mit nur geänderter Priorität, `archive/` übersprungen, `--warn`, Pfad fehlt (RC-001 bis RC-004, RC-006, RC-007)
- [x] 1.3 Test «Plugin besteht die eigene Prüfung» (RC-001)
- [x] 1.4 Testbefehl `python3 -m unittest discover -s tests -v` in `CLAUDE.md` des Plugins; CI-Schritte für Tests und `python3 scripts/check-conventions.py openspec/specs openspec/changes` in `.github/workflows/checks.yml` (RC-006) – Aufruf durch 10.5/10.6 ersetzt: jetzt im Projektstamm ohne Argumente

## 2. Regel verankern

- [x] 2.1 `template-project/openspec-context.md`: Textbaustein mit Markierung `spec-concordance:requirement-conventions` (RC-005)
- [x] 2.2 Test: Baustein enthält RC-001 bis RC-004 und RC-007, `project-init` verweist darauf (RC-005)
- [x] 2.3 `skills/project-init/SKILL.md`: Schritt «OpenSpec initialisieren» mit idempotentem Anfügen des Bausteins; Schritt «Anforderungen überführen» für Must, Should und Could inkl. Regel «unklare Aufteilung erfragen» (RC-003, RC-005)
- [x] 2.4 Eigene `openspec/config.yaml` des Plugins um den Baustein ergänzen (Dogfooding, RC-005)
- [x] 2.5 `templates/de/04-requirements.md`: Hinweis zur Überführung inkl. NFR und Erklärung SHALL vs. MoSCoW (RC-001, RC-002; Doku)
- [x] 2.6 `docs/de/process-model.md`: Abschnitt «Anforderungen in OpenSpec» mit RFC-2119-Erklärung, Beispiel Umpriorisierung (RENAMED) und Migration bestehender Projekte (`--warn`); englische Fassung nachführen, Hash setzen (RC-001 bis RC-004; Doku)
- [x] 2.7 README (de/en): Python ≥ 3.10 als Voraussetzung für die Prüfskripte (D4)

## 3. Abschluss

- [x] 3.1 CHANGELOG unter [Unreleased]
- [x] 3.2 Test-Summary `docs/test-reports/2026-11-05-add-priority-convention.md`, inkl. Nachweis «Should validiert» über RC-006 in der eigenen Spec (G0) und manuellem Test RC-005 «Bestehender Kontext» als offen gekennzeichnet
- [x] 3.3 Folge-Changes notieren: Projekt-CI-Bereitstellung der Prüfung (Plugin); Nachführung der Titel in pdf-concordance

## 4. Nach Qualitäts-Gate (Lauf 1 nicht bestanden)

- [x] 4.1 RC-004: RENAMED plus MODIFIED im selben Change zulassen; Szenario, Fixture, Test, Skript
- [x] 4.2 RC-003: Szenario «Must/Should-Quelle» als manuell kennzeichnen und Nachweis ausführen; Szenario «Regel im Textbaustein» mit Test
- [x] 4.3 RC-005: manuellen Idempotenz-Test ausführen und dokumentieren
- [x] 4.4 Beobachtungen: Archiv-Ausschluss nur `openspec/changes/archive/`; Codeblöcke und „…“ als Erwähnung (RC-001); RC-Nummern im Protokoll; Tests geschärft

## 5. Nach Qualitäts-Gate (Lauf 2 nicht bestanden)

- [x] 5.1 G7: Codeblöcke dateiweit vor der Abschnitts- und Anforderungserkennung ausblenden; Fixture «fenced-headings» und Test
- [x] 5.2 Meldung bei ungültiger Titelform präzisiert; `design.md` zu Archiv und Codeblöcken präzisiert

## 6. Nach Qualitäts-Gate (Lauf 3 nicht bestanden)

- [x] 6.1 G7: Codeblock-Erkennung nach CommonMark (gleiches Zeichen, Mindestlänge, keine Sprachangabe beim Schliessen); Inline-Code mit mehreren Backticks; Fixtures und Tests für geschachtelte Zäune, Zaun mit Sprachangabe, doppelte Backticks
- [x] 6.2 Beobachtung BOM: Dateien mit Byte-Order-Mark werden geprüft statt still bestanden; Fixture und Test

## 7. Nach Qualitäts-Gate (Lauf 4 nicht bestanden)

- [x] 7.1 G7: Archiv-Ausschluss an `openspec/changes/archive/` gebunden; Fixtures und Tests für `changes/archive` ausserhalb von `openspec/` und für eine Capability namens «changes»
- [x] 7.2 G7: `design.md` präzisiert – TO-Titel unter RENAMED werden auf RC-002 geprüft; Test
- [x] 7.3 Beobachtung: Datei nicht UTF-8 → Exit 2 mit Meldung statt Abbruch; Test

## 8. Nach Qualitäts-Gate (Lauf 5 nicht bestanden)

- [x] 8.1 G7: Kopfzeilen- und RENAMED-Erkennung an den OpenSpec-Parser angeglichen (Gross-/Kleinschreibung, Leerraum, Aufzählungszeichen, abschliessende #); Fixtures und Tests
- [x] 8.2 Sicherheitsnetz: Hinweis bei Anforderungsabschnitt ohne erkannte Anforderung; Test; design.md nachgeführt

## 9. Nach Qualitäts-Gate (Lauf 6 nicht bestanden)

- [x] 9.1 G7: Zaun-Erkennung wörtlich wie OpenSpec `parsers/code-fence.js` (beliebiger Einzug); Fixtures für eingerückten Öffner und Schliesser; Gegenprobe mit `openspec show --json` (beide sehen dieselben Anforderungen); design.md nachgeführt

## 10. Revision 2 – Erkennung über OpenSpec (Entscheid Maintainer nach Gate-Lauf 7; Nachtrags-Review N1–N12)

- [x] 10.1 `scripts/check-conventions.py` auf OpenSpec-CLI umbauen: Struktur aus `list`/`show --json`, eigener Markdown-Parser entfällt bis auf Zeilenzuordnung (RC-001, RC-002, RC-004, RC-007, RC-008; N8, N11)
- [x] 10.2 Versionsprüfung, Fehler- und Strukturprüfung, Namensprüfung, Pfadprüfung, Timeout, Umgebung (RC-008; N3, N9, N10)
- [x] 10.3 Fixtures als OpenSpec-Projekte mit `proposal.md`; Attrappe für `OPENSPEC_BIN` (RC-008; N4, N5)
- [x] 10.4 Tests umbauen und ergänzen (RC-008-Szenarien, Zeilennummern, Stamm-Fehler, kein stilles Überspringen in der CI) (RC-001–RC-008; N2, N5, N11)
- [x] 10.5 CI: Node, OpenSpec 1.16.0, `permissions: contents: read`, `DO_NOT_TRACK=1`, neuer Aufruf (RC-006; N1, N2)
- [x] 10.6 Aufrufe und Doku nachführen: CLAUDE.md, process-model DE/EN, README DE/EN, Textbaustein (N2, N12)
- [x] 10.7 Test-Summary: Lauf 8, Zuordnung alte → neue Tests, getestete OpenSpec-Version; CHANGELOG (N4)

## 11. Nach Qualitäts-Gate (Lauf 8 nicht bestanden)

- [x] 11.1 G7 / RC-007: Einträge pro Spec-Datei vor der Duplikatprüfung nach Zeilennummer sortieren; Testprojekt «duplicate-modified-first» und Test
- [x] 11.2 G6 / N1: Auflagentext korrigiert (S4 wörtlich: nie `pull_request_target`; `push` auf `main` bleibt); Einzelvoten des Nachtrags-Reviews abgelegt
- [x] 11.3 Beobachtungen: OpenSpec-Version im README fixiert (1.16.0); eingerückter Code in design.md geklärt

## 12. Nach Qualitäts-Gate (Lauf 9 nicht bestanden)

- [x] 12.1 G7 / RC-001: Inline-Code nach CommonMark (gleich lange Backtick-Läufe, auch über Zeilenumbrüche; unpaarige Läufe sind Text); Szenarien «Inline-Code über einen Zeilenumbruch» und «Unpaarige Backticks»; Testprojekte und Tests
- [x] 12.2 Beobachtungen: veralteter Aufruf in 1.4 vermerkt; Laufbezeichnung in der Test-Summary; exakte Fixierung der GitHub-Actions per SHA als Folge-Change (aus dieser Sitzung nicht abfragbar)

## 13. Nach Qualitäts-Gate (Lauf 10 nicht bestanden; Entscheid Maintainer «Im Zweifel melden»)

- [x] 13.1 G7 / RC-001: Inline-Code und Zitate zählen nur innerhalb einer Zeile als Erwähnung; `\`` und `\\` begrenzen keinen Code; Regel und Begründung in Spec und `design.md`
- [x] 13.2 Szenario «Inline-Code oder Zitat über einen Zeilenumbruch» umgekehrt (meldet RC-001), Szenario «Maskierte Backticks» neu; Testprojekte `code-span-escaped`, `quote-wrap`; Tests
