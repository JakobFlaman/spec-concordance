#!/usr/bin/env python3
"""spec-concordance – Prüfung der Anforderungskonvention in OpenSpec-Projekten.

Regeln (siehe openspec/specs/requirement-conventions):
  RC-001  Anforderungstext ohne Empfehlungs-/Options-Schlüsselwort (nur SHALL)
  RC-002  Titel in der Form «<Titel> (<ID>, <Must|Should|Could>)»
  RC-004  Umpriorisierung als RENAMED, nicht als MODIFIED
  RC-007  ID + Priorität pro Spec-Datei eindeutig
  RC-008  Struktur, Namen und Texte ausschliesslich über die OpenSpec-CLI

Aufruf:
  python3 scripts/check-conventions.py [--warn] [--id-pattern REGEX] [STAMM ...]
  STAMM ist ein Projektordner mit openspec/ (Standard: aktueller Ordner).

Exitcodes: 0 = keine Verstösse (oder --warn), 1 = Verstösse, 2 = Bedien-/Eingabefehler.

Abhängigkeiten: Python-Standardbibliothek (>= 3.10) und OpenSpec-CLI (>= 1.16),
gefunden über die Umgebungsvariable OPENSPEC_BIN oder «openspec» im PATH.
Das Skript liest nur, schreibt nichts und führt keine Inhalte aus.

Copyright (c) 2026 Jakob Flaman · SPDX-License-Identifier: MIT
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

MIN_VERSION = (1, 16, 0)
INSTALL_HINT = "npm install -g @fission-ai/openspec@1.16.0"
TIMEOUT_S = 60
DEFAULT_ID_PATTERN = r"[A-Z][A-Z0-9]*(-[A-Z0-9]+)*-[0-9]+"
PRIORITIES = ("Must", "Should", "Could")
DOC_HINT = "siehe docs/de/process-model.md, Abschnitt «Anforderungen in OpenSpec»"

# Namen von Specs und Changes (aus der CLI-Ausgabe, stammen aber aus Ordnernamen):
# kein führendes «-» (OpenSpec kennt kein «--»), kein «..».
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*$")
TITLE_FULL_RE = re.compile(r"^(?P<name>.*\S)\s+\((?P<id>[^,()]+),\s*(?P<prio>[^,()]+)\)$")
TITLE_ID_ONLY_RE = re.compile(r"^(?P<name>.*\S)\s+\((?P<id>[^,()]+)\)$")
# Ganzes Wort; Unterstrich zählt nicht als Wortzeichen (_SHOULD_ ist Hervorhebung)
KEYWORD_RE = re.compile(r"(?<![^\W_])(SHOULD|MAY)(?![^\W_])")
BACKTICK_RUN_RE = re.compile(r"`+")
UNSAFE_CHARS_RE = re.compile(r"[\\<\[|]")   # siehe strip_mentions; | wegen GFM-Tabellen
# Für die Suche in der Darstellung: Markup, das ein Wort zerteilen kann, ist zwischen den Buchstaben
# erlaubt (Hervorhebung, HTML-Tags, Link-Syntax, Backslash, unsichtbare Zeichen) – nichts wird
# entfernt, damit keine Wörter verschmelzen und Wortgrenzen erhalten bleiben.
_NOISE = r"(?:<[^>\n]*>|\]\([^)\n]*\)|[*_~\\\[\]\u00ad\u200b-\u200d\u2060\ufeff])*"
SPLIT_KEYWORD_RE = re.compile(r"(?<![^\W_])(" + "|".join(_NOISE.join(w) for w in ("SHOULD", "MAY")) + r")(?![^\W_])")
ESCAPE_PAIR_RE = re.compile(r"\\([!-/:-@\[-`{-~])")
# Zitate nur innerhalb einer Zeile; gerade Anführungszeichen zählen nicht (auch Zollzeichen)
QUOTE_CHARS_RE = re.compile(r"[«»“”„]")
QUOTE_RE = re.compile(r"«[^»\n]*»|“[^”\n]*”|„[^“”\n]*[“”]")

# Nur für die Zuordnung der Zeilennummer (RC-008: Struktur kommt aus der CLI).
HEADING_RE = re.compile(r"^###\s*(?:Requirement:\s*)?(?P<name>.+?)\s*$", re.IGNORECASE)
RENAMED_TO_RE = re.compile(r"^\s*[-*+]?\s*TO:\s*`?###\s*Requirement:\s*(?P<name>.+?)`?\s*$", re.IGNORECASE)
CLOSING_HASHES_RE = re.compile(r"[ \t]+#+$")
FENCE_OPEN_RE = re.compile(r"^\s*(?P<fence>`{3,}|~{3,})(?P<info>.*)")   # wie OpenSpec code-fence.js
FENCE_CLOSE_RE = re.compile(r"^\s*(?P<fence>`{3,}|~{3,})\s*$")

# OpenSpec-Umgebungsvariablen, die Verzeichnisse oder Konfiguration umlenken
REDIRECT_ENV_PREFIX = "OPENSPEC_"


class UsageError(Exception):
    """Bedien- oder Eingabefehler → Exitcode 2."""


@dataclass
class Violation:
    path: Path
    line: int
    rule: str
    message: str
    title: str

    def format(self) -> str:
        return f"{display(self.path)}:{self.line}: {self.rule}: {self.message} – «{self.title}» – {DOC_HINT}"


@dataclass
class Entry:
    """Eine Anforderung bzw. ein RENAMED-Ziel, wie OpenSpec sie liefert."""
    kind: str          # base | ADDED | MODIFIED | RENAMED
    name: str
    text: str = ""
    rename_from: str = ""


@dataclass
class SpecFile:
    path: Path
    entries: list[Entry] = field(default_factory=list)


def display(path: Path) -> str:
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


# --------------------------------------------------------------------------- OpenSpec-CLI

def find_cli() -> str:
    cli = os.environ.get("OPENSPEC_BIN") or shutil.which("openspec")
    if not cli or not Path(cli).exists():
        raise UsageError(f"OpenSpec-CLI nicht gefunden – installieren mit «{INSTALL_HINT}» oder OPENSPEC_BIN setzen")
    return cli


def cli_env() -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith(REDIRECT_ENV_PREFIX)}
    env["DO_NOT_TRACK"] = "1"
    return env


def run_cli(cli: str, args: list[str], root: Path, label: str) -> str:
    try:
        p = subprocess.run([cli, *args], cwd=root, capture_output=True, text=True,
                           timeout=TIMEOUT_S, env=cli_env())
    except subprocess.TimeoutExpired:
        raise UsageError(f"OpenSpec antwortet nicht innert {TIMEOUT_S} s ({label})")
    except OSError as exc:
        raise UsageError(f"OpenSpec-CLI nicht ausführbar: {exc}")
    if p.returncode != 0:
        raise UsageError(f"OpenSpec meldet für «{label}»: {error_message(p.stdout, p.stderr)}")
    return p.stdout


def error_message(stdout: str, stderr: str) -> str:
    try:
        data = json.loads(stdout)
        msgs = [s.get("message", "") for s in data.get("status", []) if s.get("severity") == "error"]
        if msgs:
            return "; ".join(msgs)
    except (json.JSONDecodeError, AttributeError):
        pass
    return (stderr or stdout).strip() or "unbekannter Fehler"


def cli_json(cli: str, args: list[str], root: Path, label: str) -> dict:
    out = run_cli(cli, args, root, label)
    try:
        data = json.loads(out)
    except json.JSONDecodeError:
        raise UsageError(f"Unerwartete Ausgabe von OpenSpec für «{label}» (kein JSON)")
    if not isinstance(data, dict):
        raise UsageError(f"Unerwartete Struktur von OpenSpec für «{label}»")
    errors = [s.get("message", "") for s in data.get("status", []) if isinstance(s, dict) and s.get("severity") == "error"]
    if errors:
        raise UsageError(f"OpenSpec meldet für «{label}»: {'; '.join(errors)}")
    return data


def require(obj, key: str, label: str):
    if not isinstance(obj, dict) or key not in obj:
        raise UsageError(f"Unerwartete Struktur von OpenSpec für «{label}»: Feld «{key}» fehlt "
                         f"(getestet mit OpenSpec {'.'.join(map(str, MIN_VERSION))})")
    return obj[key]


def check_version(cli: str, root: Path) -> None:
    out = run_cli(cli, ["--version"], root, "--version").strip()
    m = re.search(r"(\d+)\.(\d+)\.(\d+)", out)
    if not m:
        raise UsageError(f"OpenSpec-Version nicht erkennbar: «{out}»")
    found = tuple(int(x) for x in m.groups())
    if found < MIN_VERSION:
        raise UsageError(f"OpenSpec {'.'.join(map(str, found))} ist zu alt – benötigt ab "
                         f"{'.'.join(map(str, MIN_VERSION))} («{INSTALL_HINT}»)")


def checked_name(name, label: str) -> str:
    if not isinstance(name, str) or not NAME_RE.fullmatch(name) or ".." in name:
        raise UsageError(f"Ungültiger Name von OpenSpec für «{label}»: {name!r}")
    return name


def safe_path(root: Path, *parts: str) -> Path:
    base = (root / "openspec").resolve()
    p = base.joinpath(*parts).resolve()
    if p != base and base not in p.parents:
        raise UsageError(f"Pfad ausserhalb von openspec/: {p}")
    return p


# --------------------------------------------------------------------------- Struktur laden

def load_project(cli: str, root: Path) -> tuple[dict[str, SpecFile], list[tuple[str, dict[str, SpecFile]]]]:
    """Basis-Specs {spec_id: SpecFile} und Changes [(name, {spec_id: SpecFile})]."""
    specs_list = require(cli_json(cli, ["list", "--specs", "--json"], root, "list --specs"), "specs", "list --specs")
    base: dict[str, SpecFile] = {}
    for item in specs_list:
        sid = checked_name(require(item, "id", "list --specs"), "list --specs")
        data = cli_json(cli, ["show", sid, "--type", "spec", "--json"], root, sid)
        sf = SpecFile(safe_path(root, "specs", sid, "spec.md"))
        for r in require(data, "requirements", sid):
            sf.entries.append(Entry("base", require(r, "name", sid), require(r, "text", sid)))
        base[sid] = sf

    changes_list = require(cli_json(cli, ["list", "--json"], root, "list"), "changes", "list")
    changes: list[tuple[str, dict[str, SpecFile]]] = []
    for item in changes_list:
        cname = checked_name(require(item, "name", "list"), "list")
        data = cli_json(cli, ["show", cname, "--json", "--deltas-only"], root, cname)
        files: dict[str, SpecFile] = {}
        for d in require(data, "deltas", cname):
            sid = checked_name(require(d, "spec", cname), cname)
            op = require(d, "operation", cname)
            sf = files.setdefault(sid, SpecFile(safe_path(root, "changes", cname, "specs", sid, "spec.md")))
            if op in ("ADDED", "MODIFIED"):
                for r in require(d, "requirements", cname):
                    sf.entries.append(Entry(op, require(r, "name", cname), require(r, "text", cname)))
            elif op == "RENAMED":
                rn = require(d, "rename", cname)
                sf.entries.append(Entry("RENAMED", require(rn, "to", cname), rename_from=require(rn, "from", cname)))
        changes.append((cname, files))
    return base, changes


# --------------------------------------------------------------------------- Zeilenzuordnung

def fenced_lines(lines: list[str]) -> set[int]:
    """Zeilen in Codeblöcken, erkannt wie OpenSpec (parsers/code-fence.js)."""
    fenced: set[int] = set()
    active: str | None = None
    for i, raw in enumerate(lines):
        if active is None:
            m = FENCE_OPEN_RE.match(raw)
            if m and not (m.group("fence")[0] == "`" and "`" in m.group("info")):
                active = m.group("fence")
                fenced.add(i)
        else:
            fenced.add(i)
            m = FENCE_CLOSE_RE.match(raw)
            if m and m.group("fence")[0] == active[0] and len(m.group("fence")) >= len(active):
                active = None
    return fenced


def normalize(title: str) -> str:
    return CLOSING_HASHES_RE.sub("", title.strip()).strip()


class LineFinder:
    """Ordnet dem n-ten Vorkommen eines Namens die n-te passende Kopfzeile zu; sonst Zeile 0."""

    def __init__(self, path: Path):
        self.headings: dict[str, list[int]] = {}
        self.renamed: dict[str, list[int]] = {}
        self.used: dict[tuple[str, str], int] = {}
        try:
            lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        except OSError:
            return
        skip = fenced_lines(lines)
        for i, raw in enumerate(lines):
            if i in skip:
                continue
            m = RENAMED_TO_RE.match(raw)
            if m:
                self.renamed.setdefault(normalize(m.group("name")), []).append(i + 1)
                continue
            m = HEADING_RE.match(raw)
            if m:
                self.headings.setdefault(normalize(m.group("name")), []).append(i + 1)

    def line(self, name: str, renamed: bool = False) -> int:
        table = self.renamed if renamed else self.headings
        key = ("r" if renamed else "h", name)
        n = self.used.get(key, 0)
        self.used[key] = n + 1
        hits = table.get(name, [])
        return hits[n] if n < len(hits) else 0


# --------------------------------------------------------------------------- Regeln

def parse_title(title: str) -> tuple[str, str | None, str | None]:
    title = normalize(title)
    m = TITLE_FULL_RE.match(title)
    if m:
        return m.group("name"), m.group("id").strip(), m.group("prio").strip()
    m = TITLE_ID_ONLY_RE.match(title)
    if m:
        return m.group("name"), m.group("id").strip(), None
    return title, None, None


def check_title(path: Path, line: int, title: str, id_re: re.Pattern) -> list[Violation]:
    name, rid, prio = parse_title(title)
    if rid is None:
        return [Violation(path, line, "RC-002", "Titelform ungültig – erwartet «<Titel> (<ID>, <Must|Should|Could>)»", title)]
    out: list[Violation] = []
    if prio is None:
        out.append(Violation(path, line, "RC-002", "Priorität fehlt", title))
    elif prio not in PRIORITIES:
        out.append(Violation(path, line, "RC-002", "Priorität muss Must, Should oder Could sein", title))
    if not id_re.fullmatch(rid):
        out.append(Violation(path, line, "RC-002", f"ID «{rid}» entspricht nicht dem Muster", title))
    return out


def pair_code_spans(line: str) -> tuple[str, bool]:
    """Inline-Code einer Zeile entfernen: ein Backtick-Lauf öffnet, der nächste gleich lange Lauf
    derselben Zeile schliesst. Liefert den Rest und ob ein Lauf ohne Gegenstück blieb."""
    runs = list(BACKTICK_RUN_RE.finditer(line))
    keep: list[str] = []
    pos = i = 0
    unpaired = False
    while i < len(runs):
        opener = runs[i]
        closer = next((j for j in range(i + 1, len(runs)) if len(runs[j].group()) == len(opener.group())), None)
        if closer is None:
            unpaired = True
            i += 1
            continue
        keep.append(line[pos:opener.start()] + " ")   # Leerzeichen: keine Wortverschmelzung
        pos = runs[closer].end()
        i = closer + 1
    keep.append(line[pos:])
    return "".join(keep), unpaired


def strip_mentions(text: str) -> str:
    """Erwähnungen (Inline-Code, Zitate) nur dort ausblenden, wo die Code-Grenzen sicher feststehen
    (positiv festgelegt statt Sonderfälle aufzuzählen). Sicher ist ein Anforderungstext, wenn
    - er keines der Zeichen \\ < [ enthält: nur Backslash-Maskierung, Autolinks/HTML und
      Link-Ziele/-Titel können nach CommonMark Backticks vor Inline-Code verbrauchen, und
    - jeder Backtick-Lauf ein Gegenstück auf derselben Zeile hat: dann paart CommonMark die Läufe
      genauso, und Absatzgrenzen (die OpenSpec nicht liefert) spielen keine Rolle.
    Zitate gelten zusätzlich nur, wenn der Text keine Zeichenreferenz enthält (kein &, sonst kann
    ein Anführungszeichen erst in der Darstellung entstehen) und nach dem Ausblenden kein
    Anführungszeichen ohne Gegenstück übrig bleibt (auch nicht auf einer anderen Zeile).
    Sonst gilt keine Erwähnung – im Zweifel melden: selten ein Fehlalarm, nie ein stiller Durchlass."""
    if UNSAFE_CHARS_RE.search(text):
        return text
    lines = [pair_code_spans(line) for line in text.split("\n")]
    if any(unpaired for _, unpaired in lines):
        return text
    code_free = "\n".join(rest for rest, _ in lines)
    if "&" in code_free:
        return code_free
    quote_free = "\n".join(QUOTE_RE.sub(" ", rest) for rest, _ in lines)
    if QUOTE_CHARS_RE.search(quote_free):
        return code_free
    return quote_free


def find_keyword(text: str) -> re.Match | None:
    """Schlüsselwort ausserhalb von Erwähnungen suchen – im Quelltext und in einer Näherung der
    Darstellung (Zeichenreferenzen aufgelöst; Hervorhebung, HTML-Tags, Link-Syntax und unsichtbare
    Zeichen zwischen den Buchstaben zugelassen), damit z. B. &#83;HOULD oder SH*OUL*D nicht durchgehen."""
    rest = strip_mentions(text)
    # Backslash-Maskierung paarweise wie CommonMark (ASCII-Satzzeichen): \\& ist keine Zeichenreferenz
    rendered = html.unescape(ESCAPE_PAIR_RE.sub(lambda m: "\\&amp;" if m.group(1) == "&" else m.group(0), rest))
    return KEYWORD_RE.search(rest) or SPLIT_KEYWORD_RE.search(rendered)


def fence_blocks(lines: list[str]) -> list[tuple[int, int]]:
    """Codeblöcke wie OpenSpec (parsers/code-fence.js): (Öffner, Schliesser oder len(lines))."""
    blocks: list[tuple[int, int]] = []
    active: str | None = None
    start = 0
    for i, raw in enumerate(lines):
        if active is None:
            m = FENCE_OPEN_RE.match(raw)
            if m and not (m.group("fence")[0] == "`" and "`" in m.group("info")):
                active, start = m.group("fence"), i
        else:
            m = FENCE_CLOSE_RE.match(raw)
            if m and m.group("fence")[0] == active[0] and len(m.group("fence")) >= len(active):
                blocks.append((start, i))
                active = None
    if active is not None:
        blocks.append((start, len(lines)))
    return blocks


def check_hidden_fences(path: Path, lines: list[str], owner) -> list[Violation]:
    """OpenSpec blendet jeden Codeblock aus (Zaun bei beliebigem Einzug, in jedem Umfeld). Sicher
    ist das nur, wenn CommonMark ihn ebenfalls als Codeblock liest – positiv festgelegt:
    - der Öffner steht ohne Einzug in Spalte 1: dann beendet er jede Liste und jedes Blockzitat
      und ist nie Fortsetzung eines Absatzes, und
    - keine frühere Zeile der Datei (auch in Codeblöcken) beginnt mit < oder [: sonst könnte ein
      HTML-Block oder ein mehrzeiliger Link-Titel den Zaun umschliessen.
    Den Schliesser erkennt CommonMark nie später als OpenSpec, der ausgeblendete Bereich ist also
    höchstens kleiner. Steht in einem unsicheren Codeblock SHOULD/MAY, wird gemeldet."""
    out: list[Violation] = []
    blocks = fence_blocks(lines)
    for a, b in blocks:
        # auch Zeilen in früheren Codeblöcken zählen: OpenSpec und CommonMark könnten sie verschieden lesen
        risky_before = any(re.match(r"\s*[<\[]", lines[k]) for k in range(a))
        safe = not lines[a][:1].isspace() and not risky_before
        if safe or not find_keyword("\n".join(lines[a + 1:b])):
            continue
        reason = ("eingerückt (Liste, Einzug)" if lines[a][:1].isspace()
                  else "nach HTML oder Link-Syntax")
        out.append(Violation(path, a + 1, "RC-001",
                             f"Codeblock {reason}: OpenSpec blendet ihn aus, CommonMark liest ihn womöglich als Text, "
                             "und darin steht SHOULD/MAY – Zaun ohne Einzug und ausserhalb von HTML setzen",
                             owner(a + 1)))
    return out


def check_text(path: Path, line: int, title: str, text: str) -> list[Violation]:
    m = find_keyword(text)
    if m:
        return [Violation(path, line, "RC-001",
                          f"Schlüsselwort {m.group(1)} im Anforderungstext – SHALL verwenden, Priorität steht im Titel"
                          " (Erwähnung in Code oder Zitat: auf eine Zeile setzen)", title)]
    return []


def check_spec_file(sf: SpecFile, id_re: re.Pattern, base_names: list[str]) -> list[Violation]:
    finder = LineFinder(sf.path)
    out: list[Violation] = []
    seen: dict[tuple[str, str], int] = {}
    renamed_to = {e.name for e in sf.entries if e.kind == "RENAMED"}
    # OpenSpec liefert ADDED vor MODIFIED, unabhängig von der Datei: für RC-007
    # («für die zweite Anforderung») in Dateireihenfolge prüfen; Zeile 0 ans Ende.
    located = [(finder.line(e.name, renamed=(e.kind == "RENAMED")), i, e) for i, e in enumerate(sf.entries)]
    located.sort(key=lambda t: (t[0] == 0, t[0], t[1]))
    for line, _, e in located:
        if e.kind == "RENAMED":
            out += check_title(sf.path, line, e.name, id_re)
            continue
        out += check_title(sf.path, line, e.name, id_re)
        out += check_text(sf.path, line, e.name, e.text)
        name, rid, prio = parse_title(e.name)
        if rid and prio:
            key = (rid, prio)
            if key in seen:
                out.append(Violation(sf.path, line, "RC-007",
                                     f"ID und Priorität ({rid}, {prio}) schon in Zeile {seen[key]} verwendet", e.name))
            else:
                seen[key] = line
        if e.kind == "MODIFIED" and e.name not in base_names and e.name not in renamed_to:
            for bt in base_names:
                bname, bid, bprio = parse_title(bt)
                if bname == name and bid == rid and bprio != prio:
                    out.append(Violation(sf.path, line, "RC-004",
                                         f"Nur die Priorität weicht von «{bt}» ab – Umpriorisierung als RENAMED mit FROM/TO erfassen", e.name))
                    break
    try:
        lines = sf.path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    except OSError:
        lines = []
    starts = sorted((ln, e.name) for ln, _, e in located if ln > 0)
    def owner(ln: int) -> str:
        before = [name for start, name in starts if start <= ln]
        return before[-1] if before else "–"
    out += check_hidden_fences(sf.path, lines, owner)
    return out


def check_root(cli: str, root: Path, id_re: re.Pattern) -> tuple[list[Violation], int, int]:
    if not (root / "openspec").is_dir():
        raise UsageError(f"«{root}» enthält kein openspec/ – den Projektstamm angeben, nicht openspec/specs oder openspec/changes")
    check_version(cli, root)
    base, changes = load_project(cli, root)
    violations: list[Violation] = []
    count = files = 0
    for sid, sf in base.items():
        violations += check_spec_file(sf, id_re, [])
        count += len(sf.entries)
        files += 1
    for _, spec_files in changes:
        for sid, sf in spec_files.items():
            base_names = [e.name for e in base[sid].entries] if sid in base else []
            violations += check_spec_file(sf, id_re, base_names)
            count += len(sf.entries)
            files += 1
    return violations, count, files


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Prüft die Anforderungskonvention in OpenSpec-Projekten.")
    ap.add_argument("roots", nargs="*", type=Path, help="Projektordner mit openspec/ (Standard: aktueller Ordner)")
    ap.add_argument("--warn", action="store_true", help="Verstösse melden, aber mit Exitcode 0 enden (Übergangsmodus)")
    ap.add_argument("--id-pattern", default=DEFAULT_ID_PATTERN, help="Regulärer Ausdruck für Anforderungs-IDs")
    args = ap.parse_args(argv)

    try:
        id_re = re.compile(args.id_pattern)
        cli = find_cli()
        violations: list[Violation] = []
        total = files = 0
        for root in args.roots or [Path(".")]:
            if not root.exists():
                raise UsageError(f"Pfad nicht gefunden: {root}")
            v, n, f = check_root(cli, root.resolve(), id_re)
            violations += v
            total += n
            files += f
        if total == 0:
            raise UsageError("keine Anforderungen gefunden")
    except re.error as exc:
        print(f"Fehler: ungültiges ID-Muster: {exc}", file=sys.stderr)
        return 2
    except UsageError as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 2

    for v in violations:
        print(v.format())
    if violations:
        affected = len({v.path for v in violations})
        print(f"{len(violations)} Verstoss/Verstösse in {affected} von {files} Datei(en); {total} Anforderung(en) geprüft.")
        return 0 if args.warn else 1
    print(f"OK: {total} Anforderung(en) in {files} Datei(en) geprüft.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
