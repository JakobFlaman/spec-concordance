"""Tests für scripts/check-conventions.py (Change add-priority-convention, Revision 2).

Die Prüfung liest die Struktur über die OpenSpec-CLI (RC-008). Tests mit echter CLI
werden lokal ohne CLI sichtbar übersprungen; in der CI (CI=true) schlagen sie fehl.
Fehlerfälle der CLI laufen über die Attrappe tests/fixtures/fake-openspec.py.

Ausführen: python3 -m unittest discover -s tests -v
Copyright (c) 2026 Jakob Flaman · SPDX-License-Identifier: MIT
"""
import os
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check-conventions.py"
FIX = ROOT / "tests" / "fixtures" / "conventions"
FAKE = ROOT / "tests" / "fixtures" / "fake-openspec.py"
HAS_CLI = shutil.which("openspec") is not None


def run(*args, cwd=ROOT, env=None):
    e = dict(os.environ)
    e.pop("OPENSPEC_BIN", None)
    e.update(env or {})
    p = subprocess.run([sys.executable, "-I", str(SCRIPT), *map(str, args)],
                       cwd=cwd, capture_output=True, text=True, env=e)
    return p.returncode, p.stdout + p.stderr


def project(name, *args, **kw):
    """Prüfung im Stamm des Testprojekts tests/fixtures/conventions/<name>."""
    return run(*args, cwd=FIX / name, **kw)


def fake(mode, name="fake-root"):
    return project(name, env={"OPENSPEC_BIN": str(FAKE), "FAKE_OPENSPEC_MODE": mode})


class CliTestCase(unittest.TestCase):
    """Benötigt die OpenSpec-CLI; in der CI ist eine fehlende CLI ein Fehlschlag."""

    def setUp(self):
        if not HAS_CLI:
            if os.environ.get("CI"):
                self.fail("OpenSpec-CLI fehlt in der CI")
            self.skipTest("OpenSpec-CLI nicht installiert (lokal übersprungen)")


class TestRC001Keyword(CliTestCase):
    def test_keyword_in_requirement_text_is_violation(self):
        code, out = project("keyword")
        self.assertEqual(code, 1)
        self.assertIn("openspec/specs/demo/spec.md:7: RC-001", out)
        self.assertIn("Darstellungsmodi (LA-F-110, Should)", out)

    def test_mentions_in_code_quotes_codeblock_and_scenarios_are_accepted(self):
        # Inline-Code (einfache und doppelte Backticks), «…», „…“, Codeblock, Szenario mit SHOULD
        code, out = project("valid")
        self.assertEqual(code, 0, out)
        self.assertNotIn("RC-001", out)

    def test_inline_code_across_line_break_is_checked(self):
        # im Zweifel melden: Inline-Code zählt nur innerhalb einer Zeile als Erwähnung
        code, out = project("code-span-wrap")
        self.assertEqual(code, 1)
        self.assertIn("spec.md:7: RC-001", out)

    def test_quote_across_paragraph_is_checked(self):
        code, out = project("quote-wrap")
        self.assertEqual(code, 1)
        self.assertIn("spec.md:7: RC-001", out)

    def test_escaped_backticks_do_not_hide_keyword(self):
        code, out = project("code-span-escaped")
        self.assertEqual(code, 1)
        self.assertIn("spec.md:7: RC-001", out)

    def test_unpaired_backticks_do_not_hide_keyword(self):
        code, out = project("code-span-unpaired")
        self.assertEqual(code, 1)
        self.assertIn("spec.md:7: RC-001", out)

    def test_headings_inside_code_blocks_do_not_hide_violations(self):
        code, out = project("fenced-headings")
        self.assertEqual(code, 1)
        self.assertIn("2 Anforderung(en)", out)
        self.assertIn("spec.md:3: RC-001", out)        # SHOULD nach dem Codeblock
        self.assertIn("spec.md:20: RC-002", out)       # Anforderung nach dem Codeblock erkannt
        self.assertNotIn("Im Code (X)", out)

    def test_plugin_passes_its_own_check(self):
        code, out = run()
        self.assertEqual(code, 0, out)


class TestRC002Title(CliTestCase):
    def test_valid_titles_incl_could_nfr_and_scenario_title(self):
        code, out = project("valid")
        self.assertEqual(code, 0, out)
        self.assertIn("5 Anforderung(en)", out)
        text = (FIX / "valid/openspec/specs/demo/spec.md").read_text(encoding="utf-8")
        self.assertIn("### Requirement: Darstellungsmodi (LA-F-110, Should)", text)

    def test_missing_priority(self):
        code, out = project("missing-priority")
        self.assertEqual(code, 1)
        self.assertIn("openspec/specs/demo/spec.md:7: RC-002: Priorität fehlt", out)
        self.assertIn("Seitenleiste (LA-F-104)", out)

    def test_unknown_priority(self):
        code, out = project("unknown-priority")
        self.assertEqual(code, 1)
        self.assertIn("Priorität muss Must, Should oder Could sein", out)

    def test_custom_id_pattern(self):
        code, out = project("valid", "--id-pattern", r"X-[0-9]+")
        self.assertEqual(code, 1)
        self.assertIn("entspricht nicht dem Muster", out)

    def test_header_variants_like_openspec(self):
        code, out = project("header-variants")
        self.assertEqual(code, 1)
        self.assertIn("2 Anforderung(en)", out)
        self.assertIn("spec.md:3: RC-002", out)
        self.assertIn("spec.md:3: RC-001", out)
        self.assertIn("spec.md:10: RC-002", out)

    def test_file_with_bom(self):
        code, out = project("bom")
        self.assertEqual(code, 1)
        self.assertIn("spec.md:7: RC-002", out)


class TestRC003And007Duplicates(CliTestCase):
    def test_same_id_two_priorities_accepted(self):
        code, out = project("valid")
        self.assertEqual(code, 0, out)

    def test_same_id_same_priority_is_violation_on_second_line(self):
        code, out = project("duplicate")
        self.assertEqual(code, 1)
        self.assertIn("spec.md:10: RC-007", out)
        self.assertIn("schon in Zeile 3", out)

    def test_duplicate_reported_in_file_order_when_modified_precedes_added(self):
        # OpenSpec liefert ADDED vor MODIFIED; die Meldung gehört zur zweiten Anforderung der Datei
        code, out = project("duplicate-modified-first")
        self.assertEqual(code, 1)
        self.assertIn("spec.md:12: RC-007", out)
        self.assertIn("schon in Zeile 3", out)
        self.assertIn("«Zweit (B-1, Must)»", out)

    def test_archived_changes_are_not_checked(self):
        code, out = project("with-archive")
        self.assertEqual(code, 0, out)

    def test_capability_named_changes_archive_is_checked(self):
        code, out = project("archive-capability")
        self.assertEqual(code, 1)
        self.assertIn("openspec/specs/changes/archive/spec.md:7: RC-002", out)


class TestRC004Reprioritisation(CliTestCase):
    def test_renamed_is_accepted(self):
        code, out = project("reprio-renamed-ok")
        self.assertEqual(code, 0, out)

    def test_renamed_target_without_priority_is_violation(self):
        code, out = project("reprio-star-bad")
        self.assertEqual(code, 1)
        self.assertIn("spec.md:4: RC-002", out)

    def test_modified_with_changed_priority_is_violation(self):
        code, out = project("reprio-modified-bad")
        self.assertEqual(code, 1)
        self.assertIn("spec.md:3: RC-004", out)
        self.assertIn("RENAMED", out)

    def test_renamed_plus_modified_in_same_change_is_accepted(self):
        code, out = project("reprio-renamed-modified")
        self.assertEqual(code, 0, out)

    def test_renamed_without_bullet_plus_modified_is_accepted(self):
        code, out = project("reprio-nobullet-ok")
        self.assertEqual(code, 0, out)


class TestRC006Cli(CliTestCase):
    def test_warn_mode_reports_but_exits_zero(self):
        code, out = project("missing-priority", "--warn")
        self.assertEqual(code, 0)
        self.assertIn("RC-002", out)

    def test_root_argument(self):
        code, out = run(FIX / "missing-priority")
        self.assertEqual(code, 1)
        self.assertIn("RC-002", out)

    def test_invalid_pattern_exit_2(self):
        code, _ = project("valid", "--id-pattern", "(")
        self.assertEqual(code, 2)

    def test_empty_project_exit_2(self):
        code, out = project("empty")
        self.assertEqual(code, 2)
        self.assertIn("keine Anforderungen gefunden", out)


class TestRC008OpenSpec(CliTestCase):
    def test_nested_capability_rc004(self):
        code, out = project("nested-capability")
        self.assertEqual(code, 1)
        self.assertIn("openspec/changes/repri/specs/area/cap/spec.md:3: RC-004", out)

    def test_base_requirement_without_prefix(self):
        code, out = project("base-no-prefix")
        self.assertEqual(code, 1)
        self.assertIn("spec.md:7: RC-002: Priorität fehlt", out)

    def test_openspec_error_is_passed_on(self):
        code, out = project("no-proposal")
        self.assertEqual(code, 2)
        self.assertIn("«np»", out)
        self.assertIn("proposal.md", out)

    def test_folder_without_openspec_exit_2(self):
        code, out = run(ROOT / "openspec" / "specs")
        self.assertEqual(code, 2)
        self.assertIn("Projektstamm angeben", out)

    def test_missing_path_exit_2(self):
        code, out = run(FIX / "does-not-exist")
        self.assertEqual(code, 2)
        self.assertIn("Pfad nicht gefunden", out)


class TestRC008Fake(unittest.TestCase):
    """Fehlerfälle über die Attrappe – brauchen keine echte CLI."""

    def test_openspec_missing(self):
        code, out = project("fake-root", env={"OPENSPEC_BIN": "/nicht/vorhanden"})
        self.assertEqual(code, 2)
        self.assertIn("OpenSpec-CLI nicht gefunden", out)

    def test_openspec_too_old(self):
        code, out = fake("old")
        self.assertEqual(code, 2)
        self.assertIn("1.15.0 ist zu alt", out)
        self.assertIn("1.16.0", out)

    def test_openspec_error_message(self):
        code, out = fake("error")
        self.assertEqual(code, 2)
        self.assertIn("Attrappe meldet einen Fehler", out)

    def test_unexpected_structure(self):
        code, out = fake("missing-field")
        self.assertEqual(code, 2)
        self.assertIn("Feld «id» fehlt", out)

    def test_name_starting_with_dash_is_rejected(self):
        code, out = fake("bad-name")
        self.assertEqual(code, 2)
        self.assertIn("Ungültiger Name", out)

    def test_line_falls_back_to_zero(self):
        code, out = fake("unknown-line")
        self.assertEqual(code, 1)
        self.assertIn("spec.md:0: RC-002", out)


class TestRC005Template(unittest.TestCase):
    MARKER = "spec-concordance:requirement-conventions"

    def test_context_snippet_contains_rules(self):
        text = (ROOT / "template-project" / "openspec-context.md").read_text(encoding="utf-8")
        self.assertIn(self.MARKER, text)
        for rule in ("RC-001", "RC-002", "RC-003", "RC-004", "RC-007"):
            self.assertIn(rule, text)

    def test_split_rule_and_ask_maintainer(self):
        snippet = (ROOT / "template-project" / "openspec-context.md").read_text(encoding="utf-8")
        skill = (ROOT / "skills" / "project-init" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("ask the maintainer instead of guessing", snippet)
        self.assertIn("beim Maintainer nachfragen", skill)

    def test_project_init_references_snippet(self):
        text = (ROOT / "skills" / "project-init" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("openspec-context.md", text)
        self.assertIn(self.MARKER, text)

    def test_plugin_config_contains_snippet(self):
        text = (ROOT / "openspec" / "config.yaml").read_text(encoding="utf-8")
        self.assertIn(self.MARKER, text)


if __name__ == "__main__":
    unittest.main()
