#!/usr/bin/env python3
"""Prüft, ob .claude-plugin/marketplace.json zum Plugin-Manifest passt (Change add-github-marketplace, DI-001).

Aufruf:  python3 scripts/check-marketplace.py [MARKTPLATZ.json [PLUGIN.json]]
Exitcodes: 0 = passt, 1 = Widerspruch, 2 = Datei fehlt oder ist kein gültiges JSON.
Nur Standardbibliothek. Copyright (c) 2026 Jakob Flaman · SPDX-License-Identifier: MIT
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")


def check(marketplace: dict, manifest: dict) -> list[str]:
    """Liefert die Widersprüche als Liste lesbarer Meldungen (leer = passt)."""
    errors: list[str] = []
    for field in ("name", "description"):
        if not isinstance(marketplace.get(field), str) or not marketplace[field].strip():
            errors.append(f"Marktplatz: Feld «{field}» fehlt")
    owner = marketplace.get("owner")
    if not isinstance(owner, dict) or not isinstance(owner.get("name"), str) or not owner["name"].strip():
        errors.append("Marktplatz: Feld «owner.name» fehlt")
    elif any(EMAIL_RE.search(str(v)) for v in owner.values()):
        errors.append("Marktplatz: «owner» enthält eine E-Mail-Adresse – nur den Namen angeben")
    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        errors.append("Marktplatz: «plugins» muss genau einen Eintrag haben")
        return errors
    entry = plugins[0]
    if not isinstance(entry, dict):
        return errors + ["Marktplatz: Eintrag ist kein Objekt"]
    if entry.get("name") != manifest.get("name"):
        errors.append(f"Eintrag «{entry.get('name')}» heisst anders als plugin.json «{manifest.get('name')}»")
    if entry.get("source") not in ("./", "."):
        errors.append(f"Eintrag: «source» muss «./» sein, nicht «{entry.get('source')}»")
    if "version" in entry:
        errors.append("Eintrag: keine «version» – die Version steht nur in plugin.json")
    if not manifest.get("version"):
        errors.append("plugin.json: Feld «version» fehlt")
    return errors


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if not isinstance(data, dict):
        raise ValueError("kein JSON-Objekt")
    return data


def main(argv: list[str]) -> int:
    mp = Path(argv[1]) if len(argv) > 1 else ROOT / ".claude-plugin" / "marketplace.json"
    pj = Path(argv[2]) if len(argv) > 2 else ROOT / ".claude-plugin" / "plugin.json"
    try:
        errors = check(load(mp), load(pj))
    except (OSError, ValueError) as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 2
    for e in errors:
        print(e)
    print("OK: Marktplatz passt zum Plugin-Manifest." if not errors else f"{len(errors)} Widerspruch/Widersprüche.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
