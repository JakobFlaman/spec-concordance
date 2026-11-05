# Tasks: Prioritätskonvention

Version: Änderungen werden unter [Unreleased] gesammelt; `plugin.json` wird beim nächsten Release nachgezogen (D16).

## 1. Prüfung (zuerst, damit die Abnahmekriterien testbar sind)

- [ ] 1.1 `scripts/check-conventions.py` nach der Schnittstelle in `design.md` (Erkennungsregel RC-001, Titel RC-002, Duplikate RC-007, Umpriorisierung RC-004, Exitcodes 0/1/2, `--warn`, `--id-pattern`; nur Standardbibliothek, nur lesend)
- [ ] 1.2 Testdaten `tests/fixtures/conventions/` und `tests/test_check_conventions.py` (unittest): gültig, Priorität fehlt, unbekannte Priorität, SHOULD im Text, SHOULD als Erwähnung (Code, Zitat, Szenario), Duplikat, gleiche ID mit zwei Prioritäten, RENAMED korrekt, MODIFIED mit nur geänderter Priorität, `archive/` übersprungen, `--warn`, Pfad fehlt (RC-001 bis RC-004, RC-006, RC-007)
- [ ] 1.3 Test «Plugin besteht die eigene Prüfung» (RC-001)
- [ ] 1.4 Testbefehl `python3 -m unittest discover -s tests -v` in `CLAUDE.md` des Plugins; CI-Schritte für Tests und `python3 scripts/check-conventions.py openspec/specs openspec/changes` in `.github/workflows/checks.yml` (RC-006)

## 2. Regel verankern

- [ ] 2.1 `template-project/openspec-context.md`: Textbaustein mit Markierung `spec-concordance:requirement-conventions` (RC-005)
- [ ] 2.2 Test: Baustein enthält RC-001 bis RC-004 und RC-007, `project-init` verweist darauf (RC-005)
- [ ] 2.3 `skills/project-init/SKILL.md`: Schritt «OpenSpec initialisieren» mit idempotentem Anfügen des Bausteins; Schritt «Anforderungen überführen» für Must, Should und Could inkl. Regel «unklare Aufteilung erfragen» (RC-003, RC-005)
- [ ] 2.4 Eigene `openspec/config.yaml` des Plugins um den Baustein ergänzen (Dogfooding, RC-005)
- [ ] 2.5 `templates/de/04-requirements.md`: Hinweis zur Überführung inkl. NFR und Erklärung SHALL vs. MoSCoW (RC-001, RC-002; Doku)
- [ ] 2.6 `docs/de/process-model.md`: Abschnitt «Anforderungen in OpenSpec» mit RFC-2119-Erklärung, Beispiel Umpriorisierung (RENAMED) und Migration bestehender Projekte (`--warn`); englische Fassung nachführen, Hash setzen (RC-001 bis RC-004; Doku)
- [ ] 2.7 README (de/en): Python ≥ 3.10 als Voraussetzung für die Prüfskripte (D4)

## 3. Abschluss

- [ ] 3.1 CHANGELOG unter [Unreleased]
- [ ] 3.2 Test-Summary `docs/test-reports/2026-11-05-add-priority-convention.md`, inkl. Nachweis «Should validiert» über RC-006 in der eigenen Spec (G0) und manuellem Test RC-005 «Bestehender Kontext» als offen gekennzeichnet
- [ ] 3.3 Folge-Changes notieren: Projekt-CI-Bereitstellung der Prüfung (Plugin); Nachführung der Titel in pdf-concordance
