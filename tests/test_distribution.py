"""Tests für die Installation aus GitHub (Change add-github-marketplace, DI-001 bis DI-006).

Ausführen: python3 -m unittest discover -s tests -v
Copyright (c) 2026 Jakob Flaman · SPDX-License-Identifier: MIT
"""
import importlib.util
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check-marketplace.py"
FIX = ROOT / "tests" / "fixtures" / "marketplace"
READMES = [ROOT / "README.md", ROOT / "README.en.md"]
QUICKSTART = {"README.md": "## Schnellstart", "README.en.md": "## Quick start"}

_spec = importlib.util.spec_from_file_location("check_marketplace", SCRIPT)
cm = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cm)


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def quickstart(path: Path) -> str:
    """Abschnitt Schnellstart bis zur nächsten Überschrift der Ebene 2."""
    text = path.read_text(encoding="utf-8")
    start = text.index(QUICKSTART[path.name])
    rest = text[start + 3:]
    m = re.search(r"^## ", rest, re.M)
    return text[start:start + 3 + (m.start() if m else len(rest))]


class TestDI001Marketplace(unittest.TestCase):
    def setUp(self):
        self.mp = load(ROOT / ".claude-plugin" / "marketplace.json")
        self.pj = load(ROOT / ".claude-plugin" / "plugin.json")

    def test_marketplace_matches_manifest(self):
        self.assertEqual(cm.check(self.mp, self.pj), [])
        self.assertEqual(len(self.mp["plugins"]), 1)
        self.assertEqual(self.mp["plugins"][0]["source"], "./")
        self.assertNotIn("version", self.mp["plugins"][0])

    def test_name_mismatch_is_reported(self):
        errors = cm.check(load(FIX / "name-mismatch.json"), self.pj)
        self.assertTrue(any("heisst anders" in e for e in errors), errors)

    def test_script_exit_codes(self):
        ok = subprocess.run([sys.executable, "-I", str(SCRIPT)], capture_output=True, text=True)
        self.assertEqual(ok.returncode, 0, ok.stdout + ok.stderr)
        bad = subprocess.run([sys.executable, "-I", str(SCRIPT), str(FIX / "name-mismatch.json")],
                             capture_output=True, text=True)
        self.assertEqual(bad.returncode, 1)
        missing = subprocess.run([sys.executable, "-I", str(SCRIPT), str(FIX / "fehlt.json")],
                                 capture_output=True, text=True)
        self.assertEqual(missing.returncode, 2)

    def test_further_violations_are_reported(self):
        cases = {
            "zwei Einträge": dict(self.mp, plugins=self.mp["plugins"] * 2),
            "Version im Eintrag": dict(self.mp, plugins=[dict(self.mp["plugins"][0], version="1.0.0")]),
            "andere Quelle": dict(self.mp, plugins=[dict(self.mp["plugins"][0], source="./plugins/x")]),
            "Quelle . statt ./": dict(self.mp, plugins=[dict(self.mp["plugins"][0], source=".")]),
            "E-Mail im owner": dict(self.mp, owner={"name": "X", "email": "x@example.org"}),
            "owner ohne Name": dict(self.mp, owner={}),
            "ohne Beschreibung": {k: v for k, v in self.mp.items() if k != "description"},
        }
        for label, data in cases.items():
            with self.subTest(label):
                self.assertNotEqual(cm.check(data, self.pj), [])


class TestDI002Readme(unittest.TestCase):
    COMMANDS = ("/plugin install spec-concordance --marketplace JakobFlaman/spec-concordance",
                "/plugin marketplace add JakobFlaman/spec-concordance",
                "/plugin install spec-concordance@spec-concordance",
                "2.1.275", "CLAUDE_CODE_PLUGIN_PREFER_HTTPS")

    def test_install_commands_in_both_readmes(self):
        for path in READMES:
            text = path.read_text(encoding="utf-8")
            for cmd in self.COMMANDS:
                with self.subTest(file=path.name, cmd=cmd):
                    self.assertIn(cmd, text)
            self.assertNotIn("<owner>", text)


class TestDI003NoClone(unittest.TestCase):
    CLONE_RE = re.compile(r"git clone|cp\s+-r\s+\S*template-project")

    def test_quickstart_needs_no_clone(self):
        for path in READMES:
            with self.subTest(file=path.name):
                section = quickstart(path)
                self.assertIn("/spec-concordance:project-init", section)
                self.assertIsNone(self.CLONE_RE.search(section), self.CLONE_RE.search(section))

    def test_old_quickstart_would_fail(self):
        # Gegenprobe: der bisherige Schnellstart enthielt Klon und Kopie der Startvorlage
        old = "git clone https://github.com/<owner>/spec-concordance.git\ncp -r spec-concordance/template-project mein-projekt"
        self.assertIsNotNone(self.CLONE_RE.search(old))

    def test_project_init_uses_plugin_root(self):
        text = (ROOT / "skills" / "project-init" / "SKILL.md").read_text(encoding="utf-8")
        refs = re.findall(r"(\S*)(?:templates/|template-project/|scripts/|docs/(?:de|en)/)", text)
        self.assertTrue(refs)
        for prefix in refs:
            with self.subTest(prefix=prefix):
                self.assertTrue(prefix.endswith("${CLAUDE_PLUGIN_ROOT}/"), prefix)


class TestDI004CI(unittest.TestCase):
    def test_ci_runs_on_push_and_pull_request(self):
        text = (ROOT / ".github" / "workflows" / "checks.yml").read_text(encoding="utf-8")
        self.assertRegex(text, r"push:\s*\n\s*branches: \[main\]")
        self.assertIn("pull_request:", text)
        self.assertNotIn("pull_request_target", text)
        self.assertIn("python3 -m unittest discover -s tests", text)


class TestDI005Update(unittest.TestCase):
    def test_update_instructions(self):
        for path in READMES:
            text = path.read_text(encoding="utf-8")
            for cmd in ("/plugin marketplace update spec-concordance", "/plugin update spec-concordance@spec-concordance",
                        "claude plugin update spec-concordance@spec-concordance"):
                with self.subTest(file=path.name, cmd=cmd):
                    self.assertIn(cmd, text)

    def test_version_only_in_plugin_json(self):
        self.assertTrue(load(ROOT / ".claude-plugin" / "plugin.json").get("version"))
        self.assertNotIn("version", load(ROOT / ".claude-plugin" / "marketplace.json"))


class TestDI006ProtectedMain(unittest.TestCase):
    def test_claude_md_describes_pr_workflow(self):
        text = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
        for phrase in ("Keine direkten Commits auf `main`", "Freigabe G11 = Mergen",
                       "Require a pull request before merging", "Require status checks to pass"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
