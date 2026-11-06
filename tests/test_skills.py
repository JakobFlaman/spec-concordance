"""Tests für die Regeln zum Change-Ablauf (Change define-gate-standard, CP-001 bis CP-007).

Die Tests prüfen feste Formulierungen in Skills, Rolle und PR-Vorlage. Ob ein Agent die Regeln
einhält, belegen die manuellen Proben in der Test-Summary (siehe design.md, «Grenzen»).

Ausführen: python3 -m unittest discover -s tests -v
Copyright (c) 2026 Jakob Flaman · SPDX-License-Identifier: MIT
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GATE = ROOT / "skills" / "quality-gate" / "SKILL.md"
PROPOSAL = ROOT / "skills" / "change-proposal" / "SKILL.md"
ROLE = ROOT / "agents" / "council-test-management.md"
PR_TEMPLATE = ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md"
G7_NAME = "Spezifikation nachgeführt und stimmt mit dem Verhalten überein"
OLD_G7_RE = re.compile(r"G7[ |]*Spezifikation nachgeführt(?! und stimmt)")


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def g7_row(gate: str) -> str:
    m = re.search(r"^\| G7 \|.*$", gate, re.M)
    return m.group(0) if m else ""


# Erwartete Formulierungen je Anforderung; die Gegenprobe wendet sie auf die alten Skills an.
GATE_PHRASES = {
    "CP-001": ["(a) Spec-Deltas vollständig und widerspruchsfrei", "(b) keine ausdrückliche Zusage",
               "**Realistisch** ist ein Fall, der bei der normalen Arbeit entstehen kann"],
    "CP-002": ["als «realistisch» oder «konstruiert» eingeordnet", "**Im Zweifel gilt «realistisch».**",
               "**Beobachtung**: Er hat keinen Schweregrad"],
    "CP-003": ["**Gültige Grenzen**", "beim Council-Review bereits im Abschnitt «Grenzen»", "**Sicherheitszweck:**"],
    "CP-004": ["**Entscheide des Maintainers:**", "Folge-Change verschieben",
               "Ohne festgehaltenen Entscheid bleibt ein realistischer Befund ❌"],
    "CP-006": ["`openspec/changes/<id>/gate-log.md`", "**Gate-Protokoll lesen**", "| Lauf | Datum | Ergebnis |"],
    "CP-007": ["**drei aufeinanderfolgenden Läufen**", "bei G3 und G7 zusätzlich zur selben Anforderung",
               "setzt die Zählung zurück"],
}
PROPOSAL_PHRASES = ["Abschnitt «Grenzen»", "automatische Prüfung, Erkennung oder Entscheidung",
                    "entscheidet das Council; im Zweifel gilt die Pflicht", "**Absolute Zusagen**",
                    "Vergleichsmassstab", "> Manueller Test: …"]


def missing(content: str, phrases: list[str]) -> list[str]:
    return [p for p in phrases if p not in content]


class TestGateSkill(unittest.TestCase):
    def test_g7_row_has_both_parts(self):  # CP-001
        row = g7_row(text(GATE))
        self.assertIn(G7_NAME, row)
        self.assertIn("(a)", row)
        self.assertIn("(b)", row)

    def test_gate_phrases_per_requirement(self):  # CP-001 bis CP-004, CP-006, CP-007
        gate = text(GATE)
        for rid, phrases in GATE_PHRASES.items():
            with self.subTest(rid):
                self.assertEqual(missing(gate, phrases), [])


class TestProposalAndRole(unittest.TestCase):
    def test_proposal_requires_limits(self):  # CP-005
        self.assertEqual(missing(text(PROPOSAL), PROPOSAL_PHRASES), [])

    def test_role_asks_for_limits_as_major(self):  # CP-005
        role = text(ROLE)
        m = re.search(r"^\d+\. \*\*Grenzen:\*\*.*$", role, re.M)
        self.assertIsNotNone(m)
        self.assertIn("`major`", m.group(0))


class TestOldG7NameGone(unittest.TestCase):
    def test_no_old_g7_name_outside_changes(self):  # CP-001, Auflage D9
        hits = []
        for path in ROOT.rglob("*.md"):
            rel = path.relative_to(ROOT).as_posix()
            if rel.startswith(("openspec/changes/", ".git/", "docs/test-reports/")):
                continue
            if OLD_G7_RE.search(text(path)):
                hits.append(rel)
        self.assertEqual(hits, [])
        self.assertIn(G7_NAME, text(PR_TEMPLATE))


class TestCounterProbe(unittest.TestCase):
    """Gegenprobe: die Prüfungen schlagen auf dem Stand vor dem Change fehl."""

    OLD_GATE = "| G7 | Spezifikation nachgeführt | Spec-Deltas vollständig, keine Widersprüche |\n"
    OLD_PROPOSAL = "- Abnahmekriterien müssen als automatischer Test formulierbar sein.\n"

    def test_old_texts_fail(self):
        self.assertNotIn(G7_NAME, g7_row(self.OLD_GATE))
        self.assertIsNotNone(OLD_G7_RE.search(self.OLD_GATE))
        for rid, phrases in GATE_PHRASES.items():
            with self.subTest(rid):
                self.assertNotEqual(missing(self.OLD_GATE, phrases), [])
        self.assertNotEqual(missing(self.OLD_PROPOSAL, PROPOSAL_PHRASES), [])


if __name__ == "__main__":
    unittest.main()
