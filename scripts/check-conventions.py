#!/usr/bin/env python3
"""spec-concordance – Prüfung der Anforderungskonvention in OpenSpec-Spezifikationen.

Regeln (siehe openspec/specs/requirement-conventions):
  RC-001  Anforderungstext ohne Empfehlungs-/Options-Schlüsselwort (nur SHALL)
  RC-002  Titel in der Form «<Titel> (<ID>, <Must|Should|Could>)»
  RC-004  Umpriorisierung als RENAMED, nicht als MODIFIED
  RC-007  ID + Priorität pro Datei eindeutig

Aufruf:
  python3 scripts/check-conventions.py [--warn] [--id-pattern REGEX] [PFAD ...]
  Ohne Pfad: openspec/specs openspec/changes

Exitcodes: 0 = keine Verstösse (oder --warn), 1 = Verstösse, 2 = Bedien-/Eingabefehler.

Das Skript liest nur, schreibt nichts und führt keine Inhalte aus.
Nur Python-Standardbibliothek (>= 3.10).

Copyright (c) 2026 Jakob Flaman · SPDX-License-Identifier: MIT
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

DEFAULT_ID_PATTERN = r"[A-Z][A-Z0-9]*(-[A-Z0-9]+)*-[0-9]+"
PRIORITIES = ("Must", "Should", "Could")
DOC_HINT = "siehe docs/de/process-model.md, Abschnitt «Anforderungen in OpenSpec»"

SECTION_RE = re.compile(r"^##\s+(.*?)\s*$")
REQ_RE = re.compile(r"^###\s+Requirement:\s*(.*?)\s*$")
SCENARIO_RE = re.compile(r"^####\s+Scenario:")
RENAMED_TO_RE = re.compile(r"^\s*-\s*TO:\s*`?###\s+Requirement:\s*(.*?)`?\s*$")
TITLE_FULL_RE = re.compile(r"^(?P<name>.*\S)\s+\((?P<id>[^,()]+),\s*(?P<prio>[^,()]+)\)$")
TITLE_ID_ONLY_RE = re.compile(r"^(?P<name>.*\S)\s+\((?P<id>[^,()]+)\)$")
KEYWORD_RE = re.compile(r"\b(SHOULD|MAY)\b")
MENTION_RE = re.compile(r"`[^`]*`|«[^»]*»|\"[^\"]*\"|“[^”]*”|„[^“”]*[“”]")
FENCE_RE = re.compile(r"^\s*(```|~~~)")

CHECKED = {"requirements", "added requirements", "modified requirements"}


@dataclass
class Violation:
    path: Path
    line: int
    rule: str
    message: str
    title: str

    def format(self) -> str:
        return f"{self.path}:{self.line}: {self.rule}: {self.message} – «{self.title}» – {DOC_HINT}"


def parse_title(title: str) -> tuple[str, str | None, str | None]:
    """Return (name, id, priority); id/priority None if absent."""
    m = TITLE_FULL_RE.match(title)
    if m:
        return m.group("name"), m.group("id").strip(), m.group("prio").strip()
    m = TITLE_ID_ONLY_RE.match(title)
    if m:
        return m.group("name"), m.group("id").strip(), None
    return title, None, None


def check_title(path: Path, line: int, title: str, id_re: re.Pattern) -> list[Violation]:
    name, rid, prio = parse_title(title)
    out: list[Violation] = []
    if rid is None:
        out.append(Violation(path, line, "RC-002", "Titelform ungültig – erwartet «<Titel> (<ID>, <Must|Should|Could>)»", title))
        return out
    if prio is None:
        out.append(Violation(path, line, "RC-002", "Priorität fehlt", title))
    elif prio not in PRIORITIES:
        out.append(Violation(path, line, "RC-002", "Priorität muss Must, Should oder Could sein", title))
    if not id_re.fullmatch(rid):
        out.append(Violation(path, line, "RC-002", f"ID «{rid}» entspricht nicht dem Muster", title))
    return out


def base_spec_for(path: Path) -> Path | None:
    """openspec/changes/<change>/specs/<cap>/spec.md -> openspec/specs/<cap>/spec.md"""
    parts = path.resolve().parts
    try:
        i = len(parts) - 1 - parts[::-1].index("openspec")
    except ValueError:
        return None
    rest = parts[i + 1:]
    if len(rest) >= 5 and rest[0] == "changes" and rest[2] == "specs":
        cap = rest[3]
        return Path(*parts[: i + 1], "specs", cap, "spec.md")
    return None


def fenced_lines(lines: list[str]) -> set[int]:
    """Indizes (0-basiert) aller Zeilen in eingezäunten Codeblöcken, inkl. Zaunzeilen.

    Codeblöcke gelten dateiweit als Erwähnung: Überschriften darin sind weder Abschnitte
    noch Anforderungen, Schlüsselwörter darin keine Verstösse.
    """
    fenced: set[int] = set()
    fence: str | None = None
    for i, raw in enumerate(lines):
        m = FENCE_RE.match(raw)
        if fence is None and m:
            fence = m.group(1)
            fenced.add(i)
        elif fence is not None:
            fenced.add(i)
            if raw.strip().startswith(fence):
                fence = None
    return fenced


def requirement_titles(path: Path) -> list[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    skip = fenced_lines(lines)
    titles = []
    for i, line in enumerate(lines):
        if i in skip:
            continue
        m = REQ_RE.match(line)
        if m:
            titles.append(m.group(1))
    return titles


def renamed_targets(lines: list[str]) -> set[str]:
    """TO-Titel aller RENAMED-Einträge der Datei (für RC-004 «RENAMED plus MODIFIED»)."""
    targets: set[str] = set()
    section = ""
    skip = fenced_lines(lines)
    for i, raw in enumerate(lines):
        if i in skip:
            continue
        sm = SECTION_RE.match(raw)
        if sm:
            section = sm.group(1).strip().lower()
            continue
        if section == "renamed requirements":
            tm = RENAMED_TO_RE.match(raw)
            if tm:
                targets.add(tm.group(1))
    return targets


def check_file(path: Path, id_re: re.Pattern) -> tuple[list[Violation], int]:
    lines = path.read_text(encoding="utf-8").splitlines()
    violations: list[Violation] = []
    seen: dict[tuple[str, str], int] = {}
    section = ""
    current: tuple[int, str] | None = None  # (line, title) while reading requirement text
    in_text = False
    count = 0
    base_titles: list[str] | None = None
    renamed_to = renamed_targets(lines)
    skip = fenced_lines(lines)

    for no, raw in enumerate(lines, start=1):
        if no - 1 in skip:
            continue
        sm = SECTION_RE.match(raw)
        if sm and not raw.startswith("###"):
            section = sm.group(1).strip().lower()
            in_text = False
            continue

        if section == "renamed requirements":
            tm = RENAMED_TO_RE.match(raw)
            if tm:
                count += 1
                violations += check_title(path, no, tm.group(1), id_re)
            continue

        if section not in CHECKED:
            continue

        rm = REQ_RE.match(raw)
        if rm:
            title = rm.group(1)
            count += 1
            current = (no, title)
            in_text = True
            violations += check_title(path, no, title, id_re)
            name, rid, prio = parse_title(title)
            if rid and prio:
                key = (rid, prio)
                if key in seen:
                    violations.append(Violation(path, no, "RC-007",
                        f"ID und Priorität ({rid}, {prio}) schon in Zeile {seen[key]} verwendet", title))
                else:
                    seen[key] = no
            if section == "modified requirements":
                if base_titles is None:
                    base = base_spec_for(path)
                    base_titles = requirement_titles(base) if base and base.exists() else []
                if title not in base_titles and title not in renamed_to:
                    for bt in base_titles:
                        bname, bid, bprio = parse_title(bt)
                        if bname == name and bid == rid and bprio != prio:
                            violations.append(Violation(path, no, "RC-004",
                                f"Nur die Priorität weicht von «{bt}» ab – Umpriorisierung als RENAMED mit FROM/TO erfassen", title))
                            break
            continue

        if SCENARIO_RE.match(raw) or raw.startswith("### "):
            in_text = False
            continue

        if in_text and current:
            stripped = MENTION_RE.sub("", raw)
            km = KEYWORD_RE.search(stripped)
            if km:
                violations.append(Violation(path, no, "RC-001",
                    f"Schlüsselwort {km.group(1)} im Anforderungstext – SHALL verwenden, Priorität steht im Titel", current[1]))

    return violations, count


def find_specs(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        if p.is_file() and p.name == "spec.md":
            candidates = [p]
        else:
            candidates = sorted(p.rglob("spec.md"))
        files += [f for f in candidates if not is_archived(f)]
    return files


def is_archived(path: Path) -> bool:
    """Nur openspec/changes/archive/ ausschliessen, nicht beliebige Ordner namens «archive»."""
    parts = path.resolve().parts
    return any(parts[i] == "changes" and parts[i + 1] == "archive" for i in range(len(parts) - 1))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Prüft die Anforderungskonvention in OpenSpec-Spezifikationen.")
    ap.add_argument("paths", nargs="*", type=Path, help="Dateien oder Ordner (Standard: openspec/specs openspec/changes)")
    ap.add_argument("--warn", action="store_true", help="Verstösse melden, aber mit Exitcode 0 enden (Übergangsmodus)")
    ap.add_argument("--id-pattern", default=DEFAULT_ID_PATTERN, help="Regulärer Ausdruck für Anforderungs-IDs")
    args = ap.parse_args(argv)

    try:
        id_re = re.compile(args.id_pattern)
    except re.error as exc:
        print(f"Fehler: ungültiges ID-Muster: {exc}", file=sys.stderr)
        return 2

    paths = args.paths or [Path("openspec/specs"), Path("openspec/changes")]
    missing = [p for p in paths if not p.exists()]
    if missing:
        print("Fehler: Pfad nicht gefunden: " + ", ".join(map(str, missing)), file=sys.stderr)
        return 2

    files = find_specs(paths)
    if not files:
        print("Fehler: keine spec.md gefunden in " + ", ".join(map(str, paths)), file=sys.stderr)
        return 2

    all_violations: list[Violation] = []
    total = 0
    for f in files:
        v, n = check_file(f, id_re)
        all_violations += v
        total += n

    for v in all_violations:
        print(v.format())
    if all_violations:
        affected = len({v.path for v in all_violations})
        print(f"{len(all_violations)} Verstoss/Verstösse in {affected} von {len(files)} Datei(en); {total} Anforderung(en) geprüft.")
        return 0 if args.warn else 1
    print(f"OK: {total} Anforderung(en) in {len(files)} Datei(en) geprüft.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
