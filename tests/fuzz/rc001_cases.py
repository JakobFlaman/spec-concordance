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
         "&#96;", "*", "_", "    ", "> ", "- ", "SH", "OULD", "&#83;", "&#x4F;", "&amp;", "|", "~~",
         "\u200b", "\u00ad", "**", "MAY", "M", "AY", "&#171;", "&#187;", "&ldquo;", "&rdquo;", "&bdquo;",
         "&laquo;", "&raquo;"]


NOISE = ["*", "**", "_", "~~", "&#83;", "&#x4F;", "&amp;", "\u200b", "\u00ad", "<b>", "</b>", "[", "]", "](u)", "`", "\\"]
ENTITY = {"S": "&#83;", "H": "&#72;", "O": "&#x4F;", "U": "&#85;", "L": "&#76;", "D": "&#68;", "M": "&#77;", "A": "&#65;", "Y": "&#89;"}


def split_keyword() -> str:
    """Schlüsselwort, an zufälliger Stelle durch Markup zerteilt oder teilweise als Zeichenreferenz."""
    word = random.choice(["SHOULD", "MAY"])
    if random.random() < 0.5:
        k = random.randrange(len(word))
        return word[:k] + ENTITY[word[k]] + word[k + 1:]
    k = random.randint(1, len(word) - 1)
    noise = "".join(random.choice(NOISE) for _ in range(random.randint(1, 2)))
    m = random.randint(k, len(word) - 1) if random.random() < 0.5 else k
    return word[:k] + noise + word[k:m] + noise[::-1] + word[m:]


QUOTES = [("«", "»"), ("“", "”"), ("„", "“"), ("„", "”")]
QUOTE_ENTITY = {"«": "&#171;", "»": "&raquo;", "“": "&ldquo;", "”": "&#8221;", "„": "&bdquo;"}


def quoted_keyword() -> str:
    """Schlüsselwort zwischen zwei Zitaten, Anführungszeichen teils als Zeichenreferenz oder auf
    die Vorzeile verteilt – nach der Darstellung steht es ausserhalb der Zitate."""
    def q(ch: str) -> str:
        return QUOTE_ENTITY[ch] if random.random() < 0.4 else ch
    (o1, c1), (o2, c2) = random.choice(QUOTES), random.choice(QUOTES)
    sep = random.choice([" ", "\n", " x "])
    return f"{q(o1)}a{q(c1)}{sep}{random.choice(['SHOULD', 'MAY'])} {q(o2)}b{q(c2)}"


def main() -> None:
    random.seed(int(sys.argv[1]))
    for _ in range(int(sys.argv[2])):
        atoms = ATOMS + [split_keyword()] * 3 + [quoted_keyword()] * 2
        text = "SHALL " + "".join(random.choice(atoms) for _ in range(random.randint(3, 14)))
        if "SHOULD" not in text:
            text += " SHOULD"
        text = "\n".join(line for line in text.split("\n") if line.strip())   # OpenSpec: keine Leerzeilen
        flagged = bool(mod.find_keyword(text))
        print(json.dumps({"t": text, "flag": flagged}, ensure_ascii=False))


if __name__ == "__main__":
    main()
