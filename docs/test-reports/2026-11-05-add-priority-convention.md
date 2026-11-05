# Test-Summary: add-priority-convention

Datum: 2026-11-05 · Umgebung: Linux, Python 3, OpenSpec 1.16.0 (auch mit `--ignore-scripts` installiert geprüft) · Ausgeführt von: umsetzender Agent (Nachprüfung im Qualitäts-Gate durch unabhängigen Agenten)

## Ergebnis (Lauf 19, Revision 2) – Gate bestanden

| Prüfung | Befehl | Ergebnis |
|---|---|---|
| Unit-Tests mit OpenSpec-CLI | `python3 -m unittest discover -s tests -v` | 61 von 61 grün |
| Unit-Tests ohne CLI, lokal | `PATH` ohne `openspec` | 10 grün, 51 sichtbar übersprungen |
| Unit-Tests ohne CLI, CI | `CI=true`, `PATH` ohne `openspec` | 51 Fehlschläge (gewollt: kein trügerisches Grün) |
| Konvention, eigenes Repo | `python3 scripts/check-conventions.py` | Exit 0, 8 Anforderungen |
| OpenSpec | `openspec validate --all --strict` | gültig |
| Vergleich RC-001 mit CommonMark | `tests/fuzz/rc001_cases.py <seed> 40000 \| node tests/fuzz/rc001_oracle.js <markdown-it>` (markdown-it 14.2.0; Seeds 91–100 je 40 000, mit gezielten Bausteinen für zerteilte Schlüsselwörter, Zeichenreferenzen, Zitate und unsichtbare Zeichen) | 400 000 Zufallsfälle, 0 stille Durchlässe. Gegenproben auf 40 000 Fälle: Erkennung vor Lauf 15 214, Stand Lauf 15 72, Stand Lauf 17 7 stille Durchlässe – der Vergleich ist also empfindlich |
| Vergleich RC-001 auf Blockebene | `tests/fuzz/rc001_blocks.py <ordner> <seed> 120` und `node tests/fuzz/rc001_blocks_oracle.js …` (Seeds 11–16, mit Bausteinen für versetzte Zäune) | 720 ganze Spec-Dateien durch Skript und OpenSpec-CLI, 0 stille Durchlässe. Gegenproben: Stand Lauf 16 6, Stand Lauf 17 3 stille Durchlässe auf 120 Fälle |
| Übersetzungen | `python3 scripts/check-i18n.py` | OK |

## Abdeckung der Abnahmekriterien

| Requirement | Szenario | Nachweis |
|---|---|---|
| RC-001 | Should-Anforderung validiert | indirekt: RC-006 ist Should und besteht `openspec validate --strict` (G0) |
| RC-001 | Empfehlungs-Schlüsselwort im Anforderungstext | `test_keyword_in_requirement_text_is_violation` |
| RC-001 | Erwähnung ist kein Verstoss | `test_mentions_in_code_quotes_codeblock_and_scenarios_are_accepted`; Codeblöcke mit Überschriften: `test_headings_inside_code_blocks_do_not_hide_violations` |
| RC-001 | Inline-Code oder Zitat über einen Zeilenumbruch | `test_inline_code_across_line_break_is_checked`, `test_quote_across_paragraph_is_checked` |
| RC-001 | Unsichere Code-Grenzen | `test_escaped_backticks_do_not_hide_keyword`, `test_code_across_lines_shifting_pairing_does_not_hide_keyword`, `test_html_attribute_does_not_hide_keyword`, `test_keyword_directly_before_code_is_violation`, `test_table_pipe_makes_code_boundaries_unsafe`; Hervorhebung: `test_keyword_in_underscore_emphasis_is_violation` |
| RC-001 | Unsichere Code-Grenzen (Fortsetzung) | `test_backslash_inside_code_span_does_not_hide_keyword`, `test_mixed_escape_and_backslash_in_code_does_not_hide_keyword`, `test_backtick_in_autolink_does_not_hide_keyword` |
| RC-001 | Unsichere Zitatgrenzen | `test_quote_from_character_reference_does_not_hide_keyword`, `test_unpaired_quote_on_previous_line_does_not_hide_keyword` |
| RC-001 | Schlüsselwort erst in der Darstellung | `test_keyword_from_character_reference_is_violation`, `test_keyword_split_by_emphasis_is_violation`, `test_keyword_split_by_invisible_format_character_is_violation`, `test_keyword_in_underscore_emphasis_is_violation` |
| RC-001 | Unsicherer Codeblock | `test_fence_after_desynchronised_fence_is_violation`, `test_indented_fence_hiding_keyword_is_violation`, `test_fence_in_list_item_hiding_keyword_is_violation`, `test_fence_in_html_block_hiding_keyword_is_violation`; Vergleich auf Blockebene |
| RC-001 | Gerade Anführungszeichen | `test_straight_quotes_are_not_mentions` |
| RC-001 | Kein stiller Durchlass gegenüber CommonMark | Vergleichstest `tests/fuzz/` (siehe Ergebnis) |
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
| 11 | 43 | grün | Gate 10 nicht bestanden (G7: maskierte Backticks, Code über Absatzgrenze) – Entscheid Maintainer «im Zweifel melden»: Erwähnungen nur innerhalb einer Zeile |
| 12 | 44 | grün | Gate 11 nicht bestanden (G7: Backslash innerhalb von Inline-Code) – beide Lesarten prüfen |
| 13 | 47 | grün | Gate 12 nicht bestanden (G7: Mischfall maskierter Backtick + Backslash in Code; Autolink/HTML) – Grundregel «mehrdeutige Zeile = keine Erwähnung»; gerade Anführungszeichen kein Zitat |
| 14 | 51 | grün | Gate 13 nicht bestanden (G7: verschobene Paarung über Zeilen, HTML-Attribut, HTML über zwei Zeilen) – Erwähnungen positiv festgelegt, Vergleichstest gegen CommonMark |
| 15 | 55 | grün | Gate 14 nicht bestanden (G7: Zeichenreferenzen, eingerückter Zaun) – Schlüsselwort in der Darstellung, Zaun-Einzug, `|`; Grenzen dokumentiert |
| 16 | 57 | grün | Gate 15 nicht bestanden (G7: Anführungszeichen als Zeichenreferenz, offenes Zitat auf der Vorzeile) – sichere Grenzen auch für Zitate |
| 17 | 59 | grün | Gate 16 nicht bestanden (G7: Zaun unter Listenpunkt, Zaun im HTML-Block) – Codeblöcke positiv festgelegt, Vergleich auf Blockebene |
| 18 | 61 | grün | Gate 17 nicht bestanden (G7: versetzte Zäune nach eingerücktem Schliesser) – alle früheren Zäune in Spalte 1; unsichtbare Zeichen Kategorie Cf |
| 19 | 61 | grün | Gate 18 nicht bestanden (G7: nur konstruierte Fälle – absichtlich durch komplexes Markup zerteilte Schlüsselwörter) – Entscheid Maintainer: als Grenze dokumentiert |
