#!/usr/bin/env python3
"""spec-concordance – Prüfung veralteter Übersetzungen.

Englische Dateien tragen im YAML-Kopf `source:` (Pfad der deutschen Quelle)
und `source-hash:` (SHA-256 der Quelle, erste 12 Zeichen). Stimmt der Hash
nicht mehr, ist die Übersetzung veraltet.

Aufruf:
  python3 scripts/check-i18n.py           # prüfen, Exitcode 1 bei Abweichung
  python3 scripts/check-i18n.py --update  # Hashes nach erfolgter Übersetzung setzen

Copyright (c) 2026 Jakob Flaman · SPDX-License-Identifier: MIT
"""
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRANSLATED_DIRS = [ROOT / "docs" / "en", ROOT / "templates" / "en"]
HEADER = re.compile(r"^---\n(.*?)\n---\n", re.S)


def source_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def parse_header(text: str) -> dict:
    m = HEADER.match(text)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip()
    return out


def main() -> int:
    update = "--update" in sys.argv
    problems = 0
    for d in TRANSLATED_DIRS:
        for f in sorted(d.glob("*.md")) if d.exists() else []:
            text = f.read_text(encoding="utf-8")
            head = parse_header(text)
            if "source" not in head:
                continue
            src = ROOT / head["source"]
            rel = f.relative_to(ROOT)
            if not src.exists():
                print(f"FEHLT   {rel}: Quelle {head['source']} existiert nicht")
                problems += 1
                continue
            current = source_hash(src)
            if head.get("source-hash") == current:
                print(f"OK      {rel}")
                continue
            if update:
                text = re.sub(r"source-hash: .*", f"source-hash: {current}", text, count=1)
                f.write_text(text, encoding="utf-8")
                print(f"GESETZT {rel} -> {current}")
            else:
                print(f"VERALTET {rel}: Quelle {head['source']} wurde geändert")
                problems += 1
    return 1 if problems and not update else 0


if __name__ == "__main__":
    sys.exit(main())
