# Test-Summary: add-priority-convention

Datum: 2026-11-05 · Umgebung: Linux, Python 3, OpenSpec 1.16.0 (auch mit `--ignore-scripts` installiert geprüft) · Ausgeführt von: umsetzender Agent (Nachprüfung im Qualitäts-Gate durch unabhängigen Agenten)

## Ergebnis (Lauf 10, Revision 2)

| Prüfung | Befehl | Ergebnis |
|---|---|---|
| Unit-Tests mit OpenSpec-CLI | `python3 -m unittest discover -s tests -v` | 41 von 41 grün |
| Unit-Tests ohne CLI, lokal | `PATH` ohne `openspec` | 10 grün, 31 sichtbar übersprungen |
| Unit-Tests ohne CLI, CI | `CI=true`, `PATH` ohne `openspec` | 31 Fehlschläge (gewollt: kein trügerisches Grün) |
| Konvention, eigenes Repo | `python3 scripts/check-conventions.py` | Exit 0, 8 Anforderungen |
| OpenSpec | `openspec validate --all --strict` | gültig |
| Übersetzungen | `python3 scripts/check-i18n.py` | OK |

## Abdeckung der Abnahmekriterien

| Requirement | Szenario | Nachweis |
|---|---|---|
| RC-001 | Should-Anforderung validiert | indirekt: RC-006 ist Should und besteht `openspec validate --strict` (G0) |
| RC-001 | Empfehlungs-Schlüsselwort im Anforderungstext | `test_keyword_in_requirement_text_is_violation` |
| RC-001 | Erwähnung ist kein Verstoss | `test_mentions_in_code_quotes_codeblock_and_scenarios_are_accepted`; Codeblöcke mit Überschriften: `test_headings_inside_code_blocks_do_not_hide_violations` |
| RC-001 | Inline-Code über einen Zeilenumbruch | `test_inline_code_across_line_break_is_mention` |
| RC-001 | Unpaarige Backticks | `test_unpaired_backticks_do_not_hide_keyword` |
| RC-001 | Plugin besteht die eigene Prüfung | `test_plugin_passes_its_own_check` |
| RC-002 | Korrekter Titel | `test_valid_titles_incl_could_nfr_and_scenario_title` |
| RC-002 | Fehlende Priorität | `test_missing_priority` (Datei und Zeile geprüft) |
| RC-002 | Unbekannte Priorität | `test_unknown_priority`; zusätzlich `test_custom_id_pattern`, `test_header_variants_like_openspec`, `test_file_with_bom` |
| RC-003 | Must/Should-Quelle | **manuell, ausgeführt:** Lastenheft Blattwerk LA-F-105 (Must / Should) → `pdf-concordance/openspec/changes/add-viewer-phase-1/specs/viewer-search/spec.md` Zeile 7 «… (LA-F-105, Must)», Zeile 24 «… (LA-F-105, Should)» |
| RC-003 | Regel im Textbaustein | `test_split_rule_and_ask_maintainer` |
| RC-007 | Duplikat in einer Datei | `test_same_id_same_priority_is_violation_on_second_line` (Meldung auf der zweiten Anforderung, Zeile 10); MODIFIED vor ADDED: `test_duplicate_reported_in_file_order_when_modified_precedes_added` |
| RC-007 | Gleiche ID mit zwei Prioritäten | `test_same_id_two_priorities_accepted`; archivierte Changes: `test_archived_changes_are_not_checked`; Capability «changes/archive»: `test_capability_named_changes_archive_is_checked` |
| RC-004 | Should wird Must | `test_renamed_is_accepted`; Zieltitel geprüft: `test_renamed_target_without_priority_is_violation` |
| RC-004 | Umpriorisierung fälschlich als MODIFIED | `test_modified_with_changed_priority_is_violation` |
| RC-004 | Umpriorisieren und ändern im selben Change | `test_renamed_plus_modified_in_same_change_is_accepted`, `test_renamed_without_bullet_plus_modified_is_accepted` |
| RC-005 | Textbaustein vollständig | `test_context_snippet_contains_rules`, `test_project_init_references_snippet`, `test_plugin_config_contains_snippet` |
| RC-005 | Bestehender Kontext (idempotent) | **manuell, ausgeführt** (Lauf 2) und von den Gate-Prüfern in Lauf 3–7 unabhängig nachgestellt: Sprachangabe erhalten, Markierung genau 1×, Lauf 2 byte-identisch, YAML gültig |
| RC-006 | Plugin-CI | **echter CI-Lauf auf GitHub:** Run 42102433660 grün (Commit 0b90fee) mit Node 20, OpenSpec 1.16.0 fixiert, `--ignore-scripts`, `permissions: contents: read`, Aufruf im Stamm. Der vorherige Lauf 42102287287 schlug fehl, weil Git das leere Testprojekt `empty` nicht versionierte – behoben mit `.gitkeep` |
| RC-006 | Übergangsmodus | `test_warn_mode_reports_but_exits_zero`; weitere Bedienung: `test_root_argument`, `test_invalid_pattern_exit_2`, `test_empty_project_exit_2` |
| RC-008 | Verschachtelte Capability | `test_nested_capability_rc004` |
| RC-008 | Basis-Anforderung ohne Präfix | `test_base_requirement_without_prefix` |
| RC-008 | OpenSpec fehlt | `test_openspec_missing` (`OPENSPEC_BIN` auf nicht vorhandenen Pfad) |
| RC-008 | OpenSpec meldet einen Fehler | `test_openspec_error_is_passed_on` (echter Change ohne `proposal.md`), `test_openspec_error_message` (Attrappe) |
| RC-008 | OpenSpec zu alt | `test_openspec_too_old` (Attrappe) |
| RC-008 | Unerwartete Struktur | `test_unexpected_structure` (Attrappe) |
| RC-008 | Ordner ohne openspec/ | `test_folder_without_openspec_exit_2`; zusätzlich `test_missing_path_exit_2` |
| – | Sicherheit Namen (N9) | `test_name_starting_with_dash_is_rejected` (Attrappe) |
| – | Zeilenzuordnung (N11) | Zeile der Kopfzeile in allen Tests geprüft; zweites Vorkommen: RC-007-Test; Codeblock: `test_headings_inside_code_blocks_do_not_hide_violations`; verschachtelte Capability: RC-008-Test; Fallback Zeile 0: `test_line_falls_back_to_zero` (Attrappe) |

## Zuordnung alte → neue Tests (Lauf 7 → Lauf 8)

| Alte Tests (Lauf 7, 38) | Neu |
|---|---|
| RC-001 Schlüsselwort, Erwähnungen, eigene Prüfung | bleiben, Testdaten als OpenSpec-Projekte |
| Codeblock-Tests (Überschriften, geschachtelt, Sprachangabe, eingerückt Öffner/Schliesser) – 5 | **zusammengefasst** in `test_headings_inside_code_blocks_do_not_hide_violations` und `…_accepted`: Codeblöcke erkennt jetzt OpenSpec selbst |
| Inline-Code mit doppelten Backticks | in `valid` aufgenommen |
| RC-002 Titel, Muster, Kopfzeilen-Varianten, BOM | bleiben |
| Hinweis bei leerem Abschnitt | **entfällt**: Struktur kommt von OpenSpec; leeres Projekt → Exit 2 (`test_empty_project_exit_2`) |
| Archiv (`archive/`, Elternordner «archive», `changes/archive` ausserhalb `openspec/`) – 4 | **ersetzt**: OpenSpec liefert nur aktive Changes (`test_archived_changes_are_not_checked`); Capability «changes/archive» bleibt |
| Nicht UTF-8 | **entfällt**: Dateien liest OpenSpec; das Skript liest nur noch zur Zeilenzuordnung (mit Ersatzzeichen) |
| RC-004 RENAMED / MODIFIED / RENAMED+MODIFIED / Stern / ohne Aufzählungszeichen / Zieltitel | bleiben, je eigenes Testprojekt |
| Bedienfehler (Pfad fehlt, keine spec.md, ungültiges Muster, `--warn`) | bleiben bzw. angepasst auf Projektstamm |
| RC-005 Vorlagen – 4 | bleiben unverändert |
| – | **neu:** RC-008 (verschachtelte Capability, ohne Präfix, Fehler weitergeben, Ordner ohne `openspec/`), Attrappe (fehlt, zu alt, Fehler, Struktur, Name, Zeile 0) |

## Praxistest

`pdf-concordance` im Übergangsmodus: 15 RC-002-Verstösse in 5 von 10 Dateien, Exit 0 – identisch zum Ergebnis des alten Parsers. Nachführung als Folge-Change im Pilot.

## Vergleich mit Vorlauf

| Lauf | Tests | Ergebnis | Anlass |
|---|---|---|---|
| 1 | 19 | grün | Umsetzung |
| 2 | 23 | grün | Gate 1 nicht bestanden (G3 RC-003, RC-005; G7 RENAMED+MODIFIED) – behoben |
| 3 | 24 | grün | Gate 2 nicht bestanden (G7: Überschriften in Codeblöcken) – behoben |
| 4 | 28 | grün | Gate 3 nicht bestanden (G7: Codeblöcke, doppelte Backticks) – behoben |
| 5 | 32 | grün | Gate 4 nicht bestanden (G7: Archiv-Ausschluss, RENAMED in design.md) – behoben |
| 6 | 36 | grün | Gate 5 nicht bestanden (G7: Kopfzeilen- und RENAMED-Syntax) – behoben |
| 7 | 38 | grün | Gate 6 nicht bestanden (G7: eingerückte Zäune) – behoben |
| 8 | 38 | grün | Gate 7 nicht bestanden (G7: verschachtelte Capability, Basis ohne Präfix) – **Revision 2:** Erkennung über OpenSpec-CLI, Nachtrags-Review N1–N12 |
| 9 | 39 | grün | Gate 8 nicht bestanden (G6: N1-Text gab S4 falsch wieder – korrigiert; G7: RC-007 in OpenSpec- statt Dateireihenfolge – sortiert) |
| 10 | 41 | grün | Gate 9 nicht bestanden (G7: Inline-Code über Zeilenumbruch) – Inline-Code nach CommonMark |
