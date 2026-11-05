"""Tests für scripts/check-conventions.py (Change add-priority-convention).

Ausführen: python3 -m unittest discover -s tests -v
Copyright (c) 2026 Jakob Flaman · SPDX-License-Identifier: MIT
"""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check-conventions.py"
FIX = ROOT / "tests" / "fixtures" / "conventions"


def run(*args, cwd=ROOT):
    p = subprocess.run([sys.executable, "-I", str(SCRIPT), *map(str, args)],
                       cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


class TestRC001Keyword(unittest.TestCase):
    def test_keyword_in_requirement_text_is_violation(self):
        code, out = run(FIX / "keyword")
        self.assertEqual(code, 1)
        self.assertIn("RC-001", out)
        self.assertIn("spec.md:4:", out)
        self.assertIn("Darstellungsmodi (LA-F-110, Should)", out)

    def test_mentions_in_code_quotes_and_scenarios_are_accepted(self):
        # Fixture enthält Inline-Code, «…», „…“, einen Codeblock und ein Szenario mit SHOULD
        code, out = run(FIX / "valid")
        self.assertEqual(code, 0, out)
        self.assertNotIn("RC-001", out)

    def test_headings_inside_code_blocks_do_not_break_parsing(self):
        # Codeblock enthält «## RENAMED Requirements» und eine «### Requirement:»-Zeile
        code, out = run(FIX / "fenced-headings")
        self.assertEqual(code, 1)
        self.assertIn("2 Anforderung(en)", out)            # Überschrift im Code zählt nicht
        self.assertIn("spec.md:15: RC-001", out)           # SHOULD nach dem Codeblock wird erkannt
        self.assertIn("spec.md:21: RC-002", out)           # nächste Anforderung wird erkannt
        self.assertIn("spec.md:22: RC-001", out)
        self.assertNotIn("Beispiel ohne Priorität", out)

    def test_nested_fences_follow_commonmark(self):
        # ````-Block mit innerem ``` und «## REMOVED Requirements»: Block endet erst beim ````-Zaun
        code, out = run(FIX / "fences-nested")
        self.assertEqual(code, 1)
        self.assertIn("2 Anforderung(en)", out)
        self.assertIn("spec.md:18: RC-002", out)
        self.assertIn("spec.md:19: RC-001", out)
        self.assertNotIn("Im Code (X)", out)

    def test_fence_with_info_string_does_not_close_block(self):
        code, out = run(FIX / "fences-info")
        self.assertEqual(code, 0, out)
        self.assertIn("1 Anforderung(en)", out)

    def test_indented_closing_fence_like_openspec(self):
        # OpenSpec (code-fence.js) erkennt Zäune bei beliebigem Einzug
        code, out = run(FIX / "fences-indented-close")
        self.assertEqual(code, 1)
        self.assertIn("2 Anforderung(en)", out)
        self.assertIn("spec.md:14: RC-002", out)
        self.assertIn("spec.md:15: RC-001", out)

    def test_indented_opening_fence_like_openspec(self):
        code, out = run(FIX / "fences-indented-open")
        self.assertEqual(code, 1)
        self.assertIn("2 Anforderung(en)", out)
        self.assertIn("spec.md:14: RC-002", out)
        self.assertNotIn("Im Code (X)", out)

    def test_inline_code_with_double_backticks_is_mention(self):
        code, out = run(FIX / "inline-double")
        self.assertEqual(code, 0, out)

    def test_file_with_bom_is_checked(self):
        code, out = run(FIX / "bom")
        self.assertEqual(code, 1)
        self.assertIn("RC-002: Priorität fehlt", out)

    def test_plugin_passes_its_own_check(self):
        code, out = run(ROOT / "openspec" / "specs", ROOT / "openspec" / "changes")
        self.assertEqual(code, 0, out)


class TestRC002Title(unittest.TestCase):
    def test_valid_titles_incl_could_and_nfr(self):
        code, out = run(FIX / "valid")
        self.assertEqual(code, 0, out)
        self.assertIn("5 Anforderung(en)", out)

    def test_scenario_title_is_accepted(self):
        text = (FIX / "valid" / "openspec" / "specs" / "demo" / "spec.md").read_text(encoding="utf-8")
        self.assertIn("### Requirement: Darstellungsmodi (LA-F-110, Should)", text)
        code, out = run(FIX / "valid")
        self.assertEqual(code, 0, out)

    def test_missing_priority(self):
        code, out = run(FIX / "missing-priority")
        self.assertEqual(code, 1)
        self.assertIn("missing-priority/spec.md:3: RC-002: Priorität fehlt", out)
        self.assertIn("Seitenleiste (LA-F-104)", out)

    def test_unknown_priority(self):
        code, out = run(FIX / "unknown-priority")
        self.assertEqual(code, 1)
        self.assertIn("Priorität muss Must, Should oder Could sein", out)

    def test_custom_id_pattern(self):
        code, out = run("--id-pattern", r"X-[0-9]+", FIX / "valid")
        self.assertEqual(code, 1)
        self.assertIn("entspricht nicht dem Muster", out)


    def test_header_variants_like_openspec(self):
        # «### requirement:» und «###Requirement:» sind für OpenSpec Anforderungen
        code, out = run(FIX / "header-variants")
        self.assertEqual(code, 1)
        self.assertIn("2 Anforderung(en)", out)
        self.assertIn("spec.md:3: RC-002", out)
        self.assertIn("spec.md:4: RC-001", out)
        self.assertIn("spec.md:10: RC-002", out)

    def test_section_without_recognised_requirement_is_hinted(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "spec.md"
            f.write_text("## ADDED Requirements\n\n#### Requirement: Falsche Ebene (X-1, Must)\nText\n", encoding="utf-8")
            code, out = run(f)
            self.assertIn("ohne erkannte Anforderung", out)


class TestRC003And007Duplicates(unittest.TestCase):
    def test_same_id_two_priorities_accepted(self):
        code, out = run(FIX / "valid")
        self.assertEqual(code, 0, out)

    def test_same_id_same_priority_is_violation(self):
        code, out = run(FIX / "duplicate")
        self.assertEqual(code, 1)
        self.assertIn("RC-007", out)
        self.assertIn("schon in Zeile 3", out)

    def test_archive_is_skipped(self):
        code, out = run(FIX / "with-archive")
        self.assertEqual(code, 0, out)
        self.assertIn("1 Datei(en)", out)

    def test_parent_folder_named_archive_is_not_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "archive" / "proj"
            shutil.copytree(FIX / "valid", target)
            code, out = run(target)
            self.assertEqual(code, 0, out)
            self.assertIn("5 Anforderung(en)", out)


    def test_changes_archive_outside_openspec_is_checked(self):
        code, out = run(FIX / "archive-outside")
        self.assertEqual(code, 1)
        self.assertIn("RC-002", out)

    def test_capability_named_changes_archive_is_checked(self):
        code, out = run(FIX / "archive-capability")
        self.assertEqual(code, 1)
        self.assertIn("RC-002", out)


class TestRC004Reprioritisation(unittest.TestCase):
    def test_renamed_is_accepted(self):
        code, out = run(FIX / "reprio" / "openspec" / "changes" / "renamed-ok")
        self.assertEqual(code, 0, out)

    def test_renamed_plus_modified_in_same_change_is_accepted(self):
        code, out = run(FIX / "reprio" / "openspec" / "changes" / "renamed-and-modified")
        self.assertEqual(code, 0, out)

    def test_renamed_to_title_is_checked_for_rc002(self):
        code, out = run(FIX / "renamed-to-invalid")
        self.assertEqual(code, 1)
        self.assertIn("spec.md:4: RC-002: Priorität fehlt", out)

    def test_renamed_with_star_bullet_is_checked(self):
        # OpenSpec akzeptiert -, *, + oder kein Aufzählungszeichen vor FROM/TO
        code, out = run(FIX / "renamed-bullets" / "openspec" / "changes" / "star-bad")
        self.assertEqual(code, 1)
        self.assertIn("spec.md:4: RC-002", out)

    def test_renamed_without_bullet_plus_modified_is_accepted(self):
        code, out = run(FIX / "renamed-bullets" / "openspec" / "changes" / "nobullet-ok")
        self.assertEqual(code, 0, out)
        self.assertIn("2 Anforderung(en)", out)

    def test_modified_with_changed_priority_is_violation(self):
        code, out = run(FIX / "reprio" / "openspec" / "changes" / "modified-bad")
        self.assertEqual(code, 1)
        self.assertIn("RC-004", out)
        self.assertIn("RENAMED", out)


class TestRC006Cli(unittest.TestCase):
    def test_warn_mode_reports_but_exits_zero(self):
        code, out = run("--warn", FIX / "missing-priority")
        self.assertEqual(code, 0)
        self.assertIn("RC-002", out)

    def test_missing_path_exit_2(self):
        code, out = run(FIX / "does-not-exist")
        self.assertEqual(code, 2)
        self.assertIn("Pfad nicht gefunden", out)

    def test_no_spec_found_exit_2(self):
        code, out = run(FIX / "with-archive" / "openspec" / "changes")
        self.assertEqual(code, 2)
        self.assertIn("keine spec.md", out)

    def test_non_utf8_file_exit_2(self):
        code, out = run(FIX / "latin1")
        self.assertEqual(code, 2)
        self.assertIn("nicht UTF-8", out)

    def test_invalid_pattern_exit_2(self):
        code, out = run("--id-pattern", "(", FIX / "valid")
        self.assertEqual(code, 2)


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
