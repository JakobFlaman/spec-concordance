# Test-Summary: add-github-marketplace

Datum: 2026-11-06 · Umgebung: Linux, Python 3, OpenSpec 1.16.0, Claude Code 2.1.318 · Ausgeführt von: umsetzender Agent (Nachprüfung im Qualitäts-Gate durch unabhängigen Agenten)

## Ergebnis (Lauf 1)

| Prüfung | Befehl | Ergebnis |
|---|---|---|
| Unit-Tests | `python3 -m unittest discover -s tests -v` | 73 von 73 grün (davon 12 neu in `tests/test_distribution.py`) |
| Gegenprobe gegen den Stand von `main` vor dem Change | neue Tests auf altes README, alten Skill, alte CLAUDE.md | 19 Fehlschläge (gewollt) |
| Marktplatz | `python3 scripts/check-marketplace.py` | Exit 0 |
| Claude Code | `claude plugin validate .` (2.1.318) | «Validation passed with warnings»: `CLAUDE.md` im Stamm wird nicht als Kontext geladen (Grenze in design.md), kein Icon (nur für das Anthropic-Verzeichnis relevant) |
| Konvention, OpenSpec, Übersetzungen | `check-conventions.py`, `openspec validate --all --strict`, `check-i18n.py` | Exit 0, gültig, OK |
| CI | Pull Request #2 | siehe Abschnitt CI |

## Abdeckung der Abnahmekriterien

| Requirement | Szenario | Nachweis |
|---|---|---|
| DI-001 | Validierung mit Claude Code | **manuell, ausgeführt:** `claude plugin validate .`, siehe oben |
| DI-001 | Marktplatz-Datei passt zum Manifest | `test_marketplace_matches_manifest`, `test_further_violations_are_reported` (zwei Einträge, Version im Eintrag, andere Quelle, E-Mail im owner, owner ohne Name, ohne Beschreibung) |
| DI-001 | Name weicht ab | `test_name_mismatch_is_reported` (Fixture `tests/fixtures/marketplace/name-mismatch.json`), `test_script_exit_codes` |
| DI-002 | Befehle im README | `test_install_commands_in_both_readmes` |
| DI-002 | Installation in sauberer Umgebung | **manuell, ausgeführt** (Protokoll unten) |
| DI-003 | Kein Kopieren aus dem Klon | `test_quickstart_needs_no_clone`, Gegenprobe `test_old_quickstart_would_fail` |
| DI-003 | project-init nutzt das Installationsverzeichnis | `test_project_init_uses_plugin_root` |
| DI-003 | Dateien im installierten Plugin | **manuell, ausgeführt** (Protokoll unten) |
| DI-004 | CI-Lauf | `test_ci_runs_on_push_and_pull_request`; Run-ID siehe Abschnitt CI |
| DI-005 | Update-Anleitung | `test_update_instructions`, `test_version_only_in_plugin_json` |
| DI-006 | Regel in CLAUDE.md | `test_claude_md_describes_pr_workflow` |
| DI-006 | Branch-Schutz aktiv | **offen:** wartet auf die Einrichtung durch den Maintainer (Stand 2026-11-06: `main` nicht geschützt) |

## Protokoll manueller Installationstest (Task 4.1)

- Claude Code 2.1.318, Commit `fb99f48` auf Branch `change/add-github-marketplace`
- Git-Zugang: HTTPS ohne Anmeldung (Repository zurzeit öffentlich)
- Saubere Umgebungen: je eigenes `HOME` ohne vorhandene Claude-Code-Einstellungen
- **Einschritt-Befehl** (Shell-Form, Branch-Ref statt `main`): `claude plugin install spec-concordance --marketplace "JakobFlaman/spec-concordance#change/add-github-marketplace"` → «Successfully added marketplace: spec-concordance», «Successfully installed plugin: spec-concordance@spec-concordance (scope: user)»
- **Zwei-Schritt-Variante** in zweiter Umgebung: `claude plugin marketplace add "JakobFlaman/spec-concordance#change/add-github-marketplace"`, dann `claude plugin install spec-concordance@spec-concordance` → beide erfolgreich
- `claude plugin list`: in beiden Umgebungen `spec-concordance@spec-concordance`, Version 0.1.0, Status enabled
- `claude plugin details spec-concordance`: 4 Skills, 6 Agenten
- Installationsverzeichnis (`installPath` aus `claude plugin list --json`): `templates/de/`, `template-project/` und `scripts/check-conventions.py` vorhanden
- Prüfskript aus dem Installationsverzeichnis: Testprojekt `valid` → Exit 0, «5 Anforderung(en)»; Testprojekt `missing-priority` → 1 Verstoss gemeldet
- Nicht geprüft: die Slash-Befehle in einer interaktiven Sitzung (`/plugin install …`) und ein vollständiger Lauf von `/spec-concordance:project-init`; die Shell-Form nutzt dieselbe Installationslogik (Claude-Code-Doku), `${CLAUDE_PLUGIN_ROOT}` belegt die Doku «Skills»

## CI

Run-ID wird nach dem Lauf zu diesem Pull Request eingetragen.
