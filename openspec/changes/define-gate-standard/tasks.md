# Tasks: Massstab für das Qualitäts-Gate

## 1. Skills und Rolle

- [ ] 1.1 `skills/quality-gate/SKILL.md`: G7 mit Teilen (a) und (b), Definition «realistisch» (CP-001; D6)
- [ ] 1.2 `skills/quality-gate/SKILL.md`: Einordnung, Zweifelsregel, Beobachtung, gültige Grenzen, Sicherheitszweck, Entscheide des Maintainers (CP-002, CP-003, CP-004; D3, D4, D5)
- [ ] 1.3 `skills/quality-gate/SKILL.md`: Gate-Protokoll `gate-log.md` mit Feldern, Lesen vor jedem Lauf; Eskalation mit Zählregel (CP-006, CP-007; D1, D2, D12)
- [ ] 1.4 `skills/change-proposal/SKILL.md`: Abschnitt «Grenzen» mit Geltungsbereich, Beispielen, Entscheid im Council, im Zweifel Pflicht; Regel für absolute Zusagen (CP-005; D7)
- [ ] 1.5 `agents/council-test-management.md`: Prüffrage «Grenzen benannt?», `major` bei Fehlen (CP-005)
- [ ] 1.6 `.github/PULL_REQUEST_TEMPLATE.md`: G7-Name nachführen (CP-001; D9)

## 2. Prüfung und Doku

- [ ] 2.1 Neue Datei `tests/test_skills.py`: feste Formulierungen je Anforderung (G7-Zeile mit (a)/(b), «realistisch»/«konstruiert», «im Zweifel», «Beobachtung», `gate-log.md`, «drei aufeinanderfolgenden», «Grenzen» mit `major` in der Rolle); alter G7-Name kommt nirgends mehr vor; Gegenprobe gegen die bisherigen Skills (CP-001 bis CP-007; D9, D10)
- [ ] 2.2 `docs/de/process-model.md`: Massstab des Qualitäts-Gates, Grenzen, Gate-Protokoll; englische Fassung nachführen, Hash setzen (CP-001 bis CP-007)
- [ ] 2.3 Eigenes `gate-log.md` für diesen Change führen (Dogfooding, CP-006)

## 3. Manueller Nachweis

- [ ] 3.1 Probe mit unabhängigem Agenten nach den neuen Skills: Einordnung Lauf 17 (erwartet realistisch, ❌) und Lauf 18 (erwartet konstruiert, Beobachtung); Probe-Review Testmanagement auf synthetischen Change ohne «Grenzen» (erwartet `major`); synthetisches Gate-Protokoll mit drei Fehlschlägen (erwartet Frage an den Maintainer) (CP-001, CP-002, CP-005, CP-007; D8)

## 4. Abschluss

- [ ] 4.1 CHANGELOG unter [Unreleased]
- [ ] 4.2 Test-Summary `docs/test-reports/2026-11-06-define-gate-standard.md`
