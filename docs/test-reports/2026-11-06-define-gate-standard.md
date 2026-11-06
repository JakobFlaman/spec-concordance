# Test-Summary: define-gate-standard

Datum: 2026-11-06 · Umgebung: Linux, Python 3, OpenSpec 1.16.0 · Ausgeführt von: umsetzender Agent (Nachprüfung im Qualitäts-Gate durch unabhängigen Agenten)

## Ergebnis (Lauf 1)

| Prüfung | Befehl | Ergebnis |
|---|---|---|
| Unit-Tests | `python3 -m unittest discover -s tests -v` | 67 von 67 grün (davon 6 neu in `tests/test_skills.py`) |
| Gegenprobe gegen den Stand von `main` vor dem Change | `tests/test_skills.py` auf alte Skills, Rolle, PR-Vorlage | 10 Fehlschläge (gewollt) |
| Konvention, OpenSpec, Übersetzungen | `check-conventions.py`, `openspec validate --all --strict`, `check-i18n.py` | Exit 0, gültig, OK (Hash der englischen Fassung nachgeführt) |

## Abdeckung der Abnahmekriterien

| Requirement | Szenario | Nachweis |
|---|---|---|
| CP-001 | Regel im Skill | `test_g7_row_has_both_parts`, `test_gate_phrases_per_requirement` (CP-001); alter Name: `test_no_old_g7_name_outside_changes` |
| CP-001 | Realistischer stiller Verstoss | **manuell, ausgeführt** (Probe Fall 1) |
| CP-002 | Pflicht im Skill | `test_gate_phrases_per_requirement` (CP-002) |
| CP-002 | Konstruierter Fall | **manuell, ausgeführt** (Probe Fall 2) |
| CP-003 | Regel im Skill | `test_gate_phrases_per_requirement` (CP-003) |
| CP-004 | Regel im Skill | `test_gate_phrases_per_requirement` (CP-004) |
| CP-005 | Regel im Skill | `test_proposal_requires_limits` |
| CP-005 | Prüffrage der Rolle Testmanagement | `test_role_asks_for_limits_as_major` |
| CP-005 | Change ohne Grenzen | **manuell, ausgeführt** (Probe Fall 3) |
| CP-006 | Regel im Skill | `test_gate_phrases_per_requirement` (CP-006); eigenes `gate-log.md` im Change |
| CP-007 | Regel im Skill | `test_gate_phrases_per_requirement` (CP-007) |
| CP-007 | Dritter Fehlschlag | **manuell, ausgeführt** (Probe Fall 4) |
| alle | Gegenprobe | `test_old_texts_fail` |

## Manuelle Probe (Task 3.1)

Ein unabhängiger Agent erhielt nur die eingefrorenen neuen Regeldateien (Skills `quality-gate`, `change-proposal`, Rolle Testmanagement) und vier Fälle, ohne die erwarteten Ergebnisse. Er sollte die Regeln wörtlich anwenden und die Regelstelle zitieren.

| Fall | Inhalt | Erwartet | Ergebnis |
|---|---|---|---|
| 1 | Befund Gate-Lauf 17 von `add-priority-convention` (versetzte Codezäune nach eingerücktem Schliesser) | realistisch, G7 ❌ | realistisch, G7 ❌ – zitiert Definition «realistisch» und «Ohne festgehaltenen Entscheid bleibt ein realistischer Befund ❌» |
| 2 | Befund Gate-Lauf 18 (`SH<!-- > -->OULD`), Grenze stand beim Review in design.md | konstruiert, Beobachtung | konstruiert und innerhalb gültiger Grenze, Beobachtung; prüft ausdrücklich, dass kein Sicherheitszweck vorliegt |
| 3 | Synthetischer Change «Prüfung auf Geheimnisse» ohne Abschnitt «Grenzen», mit absoluter Zusage | Rolle Testmanagement: Befund `major` | Befunde T1 `major` (Grenzen fehlen) und T2 `major` (absolute Zusage ohne Vergleichsmassstab), zitiert Prüffrage 7 |
| 4 | Synthetisches Gate-Protokoll, drei Läufe in Folge G7 zu RC-001 | zuerst Frage an den Maintainer, kein Lauf | fragt zuerst den Maintainer; erklärt, dass «behoben» die Zählung nicht zurücksetzt |

Vom Prüfer zusätzlich genannt (Folge-Change, nicht Teil dieses Changes):
- Die Rollendateien legen nicht fest, welcher Schweregrad zu welchem Votum führt.
- Ein Change mit erkennbarem Sicherheitszweck kann als `feature` klassifiziert sein; dann greift die strengere G7-Regel nur über einen Befund der Rolle Security.

## CI

Pull Request #3: Lauf 42253026135 zu Commit `9b06a98` – success (Tests, Konvention, OpenSpec, Übersetzungen, Manifest).
