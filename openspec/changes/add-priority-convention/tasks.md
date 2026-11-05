# Tasks: Prioritätskonvention

## 1. Prüfung (zuerst, damit die Abnahmekriterien testbar sind)

- [ ] 1.1 `scripts/check-conventions.py` schreiben: prüft Requirement-Titel (ID, Priorität) und SHOULD/MAY im Anforderungstext; Ausgabe mit Datei und Titel; Exitcode (RC-001, RC-002, RC-003)
- [ ] 1.2 Testfälle für die Prüfung: Testdateien unter `tests/fixtures/conventions/` (gültig, Priorität fehlt, unbekannte Priorität, SHOULD im Text, doppelte ID+Priorität, gleiche ID mit zwei Prioritäten) und `tests/test_check_conventions.py` (RC-001 bis RC-003)
- [ ] 1.3 Testbefehl in `CLAUDE.md` des Plugins festlegen (bisher fehlt einer) und in die CI aufnehmen (RC-005)

## 2. Regel verankern

- [ ] 2.1 `skills/project-init/SKILL.md`: Schritt «OpenSpec initialisieren» mit Eintrag der Regel in `openspec/config.yaml`; Schritt 3 «Anforderungen überführen» auf die Konvention verweisen (RC-004)
- [ ] 2.2 `template-project/openspec-context.md`: Textbaustein der Regel, den `project-init` in `config.yaml` übernimmt (RC-004)
- [ ] 2.3 `templates/de/04-requirements.md`: Hinweis, wie Must/Should/Could in OpenSpec überführt werden (RC-002, RC-003)
- [ ] 2.4 `docs/de/process-model.md` um Abschnitt «Anforderungen in OpenSpec» ergänzen; englische Fassung nachführen und Hash setzen

## 3. Abschluss

- [ ] 3.1 CHANGELOG unter [Unreleased]
- [ ] 3.2 Test-Summary unter `docs/test-reports/`
