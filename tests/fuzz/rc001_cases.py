"""Zufallsfälle für den Vergleich der RC-001-Erkennung mit CommonMark (markdown-it).

Nicht Teil von unittest (braucht Node und markdown-it). Aufruf:
    python3 tests/fuzz/rc001_cases.py <seed> <anzahl> | node tests/fuzz/rc001_oracle.js [pfad/zu/markdown-it]
Gibt jeden Fall aus, in dem SHOULD nach CommonMark ausserhalb von Inline-Code und «…»/“…”/„…“
steht, das Prüfskript es aber nicht meldet (stiller Durchlass). Erwartung: 0.
Copyright (c) 2026 Jakob Flaman · SPDX-License-Identifier: MIT
"""
import importlib.util
import json
import random
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check-conventions.py"
spec = importlib.util.spec_from_file_location("check_conventions", SCRIPT)
mod = importlib.util.module_from_spec(spec)
sys.modules["check_conventions"] = mod
spec.loader.exec_module(mod)

ATOMS = ["`", "``", "`", "\\", "<", ">", "[", "]", "(", ")", '"', "«", "»", "“", "”", "„", " ", "a",
         " x ", "SHOULD", "\n", "http://a.b/", '<span title="', '">', "</span>", "]: /u ", "](u ",
         "&#96;", "*", "_", "    ", "> ", "- "]


def main() -> None:
    random.seed(int(sys.argv[1]))
    for _ in range(int(sys.argv[2])):
        text = "SHALL " + "".join(random.choice(ATOMS) for _ in range(random.randint(3, 14)))
        if "SHOULD" not in text:
            text += " SHOULD"
        text = "\n".join(line for line in text.split("\n") if line.strip())   # OpenSpec: keine Leerzeilen
        flagged = bool(mod.KEYWORD_RE.search(mod.strip_mentions(text)))
        print(json.dumps({"t": text, "flag": flagged}, ensure_ascii=False))


if __name__ == "__main__":
    main()
