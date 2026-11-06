# Council-Review: define-gate-standard
Datum: 2026-11-06 · Ergebnis: **freigegeben mit Auflagen**

Einzelvoten: `council-review-votes.md` (gemeinsamer Lauf mit `add-github-marketplace`). Die Voten nennen die IDs vor der Überarbeitung: QG-001 → CP-001, QG-002 → CP-002, QG-003 → CP-005, QG-004 → CP-007; CP-003, CP-004 und CP-006 sind aus den Auflagen neu.

## Voten

| Rolle | Votum | Befunde |
|---|---|---|
| Security | Zustimmung mit Auflagen | S1 major, S2 minor |
| Architektur | Zustimmung mit Auflagen | A1–A4 major, A5 minor; kein ADR nötig |
| Support/Betrieb | Zustimmung mit Auflagen | O1 major, O2–O3 minor |
| Entwicklung | Zustimmung mit Auflagen | E1–E3 major, E4–E6 minor |
| Fachbereich | Zustimmung mit Auflagen | F1–F2 major, F3–F4 minor |
| Testmanagement | Zustimmung mit Auflagen | T1 major, T2–T5 minor |

## Widersprüche

Fachbereich F1 hält den Befund B1 aus Gate-Lauf 19 (Zeilentrennung bei U+2028) für realistisch; der Prüfer von Lauf 19 hatte ihn als konstruiert eingeordnet. Aufgelöst über D3: realistische Fälle sind ❌, ausser der Maintainer verschiebt sie mit Begründung in einen Folge-Change; der Entscheid steht im Gate-Protokoll. (Ursprünglich «realistische, aber seltene Fälle»; «selten» nach Gate-Lauf 1 gestrichen, weil ohne Kriterium.)

## Entscheidungsliste

| Nr. | Auflage | Schweregrad | Rolle(n) | Status |
|---|---|---|---|---|
| D1 | Gate-Protokoll `gate-log.md` im Change (Lauf, Datum, Ergebnis, nicht erfüllte Punkte mit Anforderung, Einordnung, Entscheide des Maintainers, optional Dauer); der Skill liest es vor jedem Lauf | major | O1, E1, A3, T5 | eingearbeitet (Skill «Gate-Protokoll», `gate-log.md`) |
| D2 | Zählregel Eskalation: drei Läufe in Folge, in denen derselbe Gate-Punkt ❌ ist – bei Punkten mit Anforderungsbezug (G3, G7) zusätzlich dieselbe Anforderung | major / minor | A3, O2, F4 | eingearbeitet (Skill «Eskalation», CP-007) |
| D3 | Zweifelsregel und Umstufung als Anforderung: im Zweifel «realistisch»; Umstufung oder Verschiebung in einen Folge-Change nur durch den Maintainer, mit Begründung im Gate-Protokoll | major | A2, E4, F1, S2 | eingearbeitet (Skill «Massstab für G7», CP-002, CP-004) |
| D4 | Nur Grenzen zählen, die beim Council-Review vorlagen; nachträgliche Grenzen nur mit festgehaltenem Entscheid des Maintainers | major | F2 | eingearbeitet (CP-003) |
| D5 | Ausnahme Sicherheitszweck: Bei Anforderungen mit Sicherheitszweck gilt ein konstruierter Fall als realistisch, ausser er ist als Grenze dokumentiert und Security hat zugestimmt | major | S1 | eingearbeitet (CP-003) |
| D6 | G7 prüft weiterhin die formale Vollständigkeit der Spec-Deltas und zusätzlich die Übereinstimmung mit dem Verhalten | major | E2, F3 | eingearbeitet (G7 Teil (a) und (b), CP-001) |
| D7 | Geltungsbereich «Grenzen»-Pflicht einheitlich und positiv definiert (Changes, deren Ergebnis eine automatische Prüfung, Erkennung oder Entscheidung ist), Entscheid im Council, im Zweifel Pflicht; Beispiele im Skill | major | A1, E6 | eingearbeitet (change-proposal, CP-005) |
| D8 | Verhaltensszenarien als «> Manueller Test» kennzeichnen, reproduzierbarer Nachweis mit Referenzfällen aus dem Trockenlauf (Lauf 17 realistisch, Lauf 18 konstruiert, synthetischer Change ohne Grenzen, synthetisches Gate-Protokoll) | major | T1, E3 | eingearbeitet (Szenarien gekennzeichnet, Probe in der Test-Summary) |
| D9 | PR-Vorlage nachführen; Test, dass der alte G7-Name nirgends mehr vorkommt | major | A4, T4 | eingearbeitet (PR-Vorlage, `test_no_old_g7_name_outside_changes`) |
| D10 | Texttests auf feste Formulierungen; Gegenprobe gegen die alten Skills; `tests/test_skills.py` neu | minor | T2, T3, E5 | eingearbeitet (`tests/test_skills.py` mit Gegenprobe) |
| D11 | Capability `change-process` statt `quality-gate` (Regeln betreffen Proposal, Review und Gate); IDs `CP-…` | minor | A5 | eingearbeitet (Capability `change-process`) |
| D12 | Kosten und Dauer je Gate-Lauf: optionales Feld im Gate-Protokoll | minor | O3 | eingearbeitet (Spalte «Dauer (optional)» im Gate-Protokoll) |
