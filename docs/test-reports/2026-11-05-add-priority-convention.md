# Test-Summary: add-priority-convention

Datum: 2026-11-05 · Umgebung: Linux, Python 3, OpenSpec 1.16.0 · Ausgeführt von: umsetzender Agent (Nachprüfung im Qualitäts-Gate durch unabhängigen Agenten)

## Ergebnis

| Prüfung | Befehl | Ergebnis |
|---|---|---|
| Unit-Tests | `python3 -m unittest discover -s tests -v` | 19 von 19 grün |
| Konvention, eigene Specs | `python3 scripts/check-conventions.py openspec/specs openspec/changes` | Exit 0, 7 Anforderungen geprüft |
| OpenSpec | `openspec validate --all --strict` | 1 von 1 gültig |
| Übersetzungen | `python3 scripts/check-i18n.py` | OK |

## Abdeckung der Abnahmekriterien

| Requirement | Szenario | Nachweis |
|---|---|---|
| RC-001 | Should-Anforderung validiert | indirekt: RC-006 ist Should und besteht `openspec validate --strict` (G0) |
| RC-001 | Empfehlungs-Schlüsselwort im Anforderungstext | `test_keyword_in_requirement_text_is_violation` |
| RC-001 | Erwähnung ist kein Verstoss | `test_mentions_in_code_quotes_and_scenarios_are_accepted` |
| RC-001 | Plugin besteht die eigene Prüfung | `test_plugin_passes_its_own_check` |
| RC-002 | Korrekter Titel | `test_valid_titles_incl_could_and_nfr` |
| RC-002 | Fehlende Priorität | `test_missing_priority` |
| RC-002 | Unbekannte Priorität | `test_unknown_priority` (zusätzlich `test_custom_id_pattern`) |
| RC-003 | Must/Should-Quelle | Fixture `valid` (gleiche ID, zwei Prioritäten) – Aufteilung selbst ist Arbeitsregel, Prüfung im Council |
| RC-007 | Duplikat in einer Datei | `test_same_id_same_priority_is_violation` |
| RC-007 | Gleiche ID mit zwei Prioritäten | `test_same_id_two_priorities_accepted`; `archive/` ausgenommen: `test_archive_is_skipped` |
| RC-004 | Should wird Must | `test_renamed_is_accepted` |
| RC-004 | Umpriorisierung fälschlich als MODIFIED | `test_modified_with_changed_priority_is_violation` |
| RC-005 | Textbaustein vollständig | `test_context_snippet_contains_rules`, `test_project_init_references_snippet`, `test_plugin_config_contains_snippet` |
| RC-005 | Bestehender Kontext (idempotent) | **manuell, offen** – erfordert KI-Lauf von `project-init`; im Plugin-Repo selbst einmalig angewendet, Sprachangabe erhalten |
| RC-006 | Plugin-CI | CI-Schritt in `.github/workflows/checks.yml`; scannt nur `openspec/` |
| RC-006 | Übergangsmodus | `test_warn_mode_reports_but_exits_zero`; Bedienfehler: `test_missing_path_exit_2`, `test_no_spec_found_exit_2`, `test_invalid_pattern_exit_2` |

## Praxistest

Lauf im Übergangsmodus auf `pdf-concordance/openspec/changes`: 15 RC-002-Verstösse in 5 von 10 Dateien (Must-Anforderungen ohne Priorität im Titel, «Phase-1-Teil» statt Priorität), Exit 0. Nachführung als Folge-Change im Pilot.

## Vergleich mit Vorlauf

Erster Lauf – kein Vorlauf vorhanden.
