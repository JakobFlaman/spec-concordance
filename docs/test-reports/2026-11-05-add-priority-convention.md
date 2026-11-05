# Test-Summary: add-priority-convention

Datum: 2026-11-05 · Umgebung: Linux, Python 3, OpenSpec 1.16.0 · Ausgeführt von: umsetzender Agent (Nachprüfung im Qualitäts-Gate durch unabhängigen Agenten)

## Ergebnis

| Prüfung | Befehl | Ergebnis |
|---|---|---|
| Unit-Tests | `python3 -m unittest discover -s tests -v` | 36 von 36 grün (Lauf 6, nach Gate-Lauf 5) |
| Konvention, eigene Specs | `python3 scripts/check-conventions.py openspec/specs openspec/changes` | Exit 0, 7 Anforderungen geprüft |
| OpenSpec | `openspec validate --all --strict` | 1 von 1 gültig |
| Übersetzungen | `python3 scripts/check-i18n.py` | OK |

## Abdeckung der Abnahmekriterien

| Requirement | Szenario | Nachweis |
|---|---|---|
| RC-001 | Should-Anforderung validiert | indirekt: RC-006 ist Should und besteht `openspec validate --strict` (G0) |
| RC-001 | Empfehlungs-Schlüsselwort im Anforderungstext | `test_keyword_in_requirement_text_is_violation` |
| RC-001 | Erwähnung ist kein Verstoss | `test_mentions_in_code_quotes_and_scenarios_are_accepted` (Inline-Code, «…», „…“, Codeblock, Szenario) |
| RC-001 | Überschriften in Codeblöcken | `test_headings_inside_code_blocks_do_not_break_parsing`, `test_nested_fences_follow_commonmark`, `test_fence_with_info_string_does_not_close_block` |
| RC-001 | Inline-Code mit doppelten Backticks | `test_inline_code_with_double_backticks_is_mention` |
| RC-002 | Kopfzeilen-Varianten wie OpenSpec | `test_header_variants_like_openspec`, Hinweis bei leerem Abschnitt: `test_section_without_recognised_requirement_is_hinted` |
| RC-002 | Datei mit Byte-Order-Mark | `test_file_with_bom_is_checked` |
| RC-001 | Plugin besteht die eigene Prüfung | `test_plugin_passes_its_own_check` |
| RC-002 | Korrekter Titel | `test_scenario_title_is_accepted` (Titel aus dem Szenario), `test_valid_titles_incl_could_and_nfr` |
| RC-002 | Fehlende Priorität | `test_missing_priority` |
| RC-002 | Unbekannte Priorität | `test_unknown_priority` (zusätzlich `test_custom_id_pattern`) |
| RC-003 | Must/Should-Quelle | **manuell, ausgeführt:** Lastenheft Blattwerk LA-F-105 («muss … ; soll …», Must / Should) ist in `pdf-concordance/openspec/changes/add-viewer-phase-1/specs/viewer-search/spec.md` als «Volltextsuche (LA-F-105, Must)» (Zeile 7) und «Suche über mehrere Dokumente (LA-F-105, Should)» (Zeile 24) überführt |
| RC-003 | Regel im Textbaustein | `test_split_rule_and_ask_maintainer` |
| RC-007 | Duplikat in einer Datei | `test_same_id_same_priority_is_violation` |
| RC-007 | Gleiche ID mit zwei Prioritäten | `test_same_id_two_priorities_accepted`; nur `openspec/changes/archive/` ausgenommen: `test_archive_is_skipped`, `test_parent_folder_named_archive_is_not_skipped`, `test_changes_archive_outside_openspec_is_checked`, `test_capability_named_changes_archive_is_checked` |
| RC-004 | Should wird Must | `test_renamed_is_accepted`; TO-Titel auf RC-002 geprüft: `test_renamed_to_title_is_checked_for_rc002`, `test_renamed_with_star_bullet_is_checked` |
| RC-004 | Umpriorisierung fälschlich als MODIFIED | `test_modified_with_changed_priority_is_violation` |
| RC-004 | Umpriorisieren und ändern im selben Change | `test_renamed_plus_modified_in_same_change_is_accepted`, `test_renamed_without_bullet_plus_modified_is_accepted` |
| RC-005 | Textbaustein vollständig | `test_context_snippet_contains_rules`, `test_project_init_references_snippet`, `test_plugin_config_contains_snippet` |
| RC-005 | Bestehender Kontext (idempotent) | **manuell, ausgeführt:** frisches Projekt mit `openspec init --language German`, Schritt 3 von `project-init` wörtlich zweimal angewendet (vom umsetzenden Agenten): Sprachangabe erhalten (1×), Markierung genau 1×, Lauf 2 byte-identisch zu Lauf 1, YAML gültig |
| RC-006 | Plugin-CI | Inspektion: CI-Schritt in `.github/workflows/checks.yml`, scannt nur `openspec/`; Exit 1 lässt den Schritt fehlschlagen (CI-Lauf auf GitHub folgt mit dem Push) |
| RC-006 | Übergangsmodus | `test_warn_mode_reports_but_exits_zero`; Bedienfehler: `test_missing_path_exit_2`, `test_no_spec_found_exit_2`, `test_invalid_pattern_exit_2`, `test_non_utf8_file_exit_2` |

## Praxistest

Lauf im Übergangsmodus auf `pdf-concordance/openspec/changes`: 15 RC-002-Verstösse in 5 von 10 Dateien (Must-Anforderungen ohne Priorität im Titel, «Phase-1-Teil» statt Priorität), Exit 0. Nachführung als Folge-Change im Pilot.

## Vergleich mit Vorlauf

| Lauf | Tests | Ergebnis | Anlass |
|---|---|---|---|
| 1 | 19 | grün | Umsetzung |
| 2 | 23 | grün | Qualitäts-Gate nicht bestanden (G3 RC-003, RC-005; G7 RC-004 RENAMED+MODIFIED) – behoben; zusätzlich Archiv-Ausschluss präzisiert, Codeblöcke und „…“ als Erwähnung, Tests geschärft |
| 3 | 24 | grün | Qualitäts-Gate Lauf 2 nicht bestanden (G7: Überschriften in Codeblöcken störten die Abschnittserkennung) – behoben |
| 4 | 28 | grün | Qualitäts-Gate Lauf 3 nicht bestanden (G7: Codeblöcke nicht nach CommonMark, doppelte Backticks) – Erkennung nach CommonMark neu umgesetzt; BOM |
| 5 | 32 | grün | Qualitäts-Gate Lauf 4 nicht bestanden (G7: Archiv-Ausschluss nicht an `openspec/` gebunden; RENAMED in design.md ungenau) – behoben; Nicht-UTF-8 → Exit 2 |
| 6 | 36 | grün | Qualitäts-Gate Lauf 5 nicht bestanden (G7: Kopfzeilen und RENAMED strenger erkannt als von OpenSpec) – Muster an OpenSpec-Parser angeglichen; Hinweis bei leerem Abschnitt |
