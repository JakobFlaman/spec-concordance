"""Blockebene: zufällige Spec-Dateien (Listen, Blockzitate, HTML, Zäune mit Einzug, Link-Titel)
durch das ganze Prüfskript (inkl. OpenSpec-CLI) und Vergleich mit CommonMark (markdown-it).

Nicht Teil von unittest (braucht OpenSpec-CLI, Node und markdown-it; ca. 1 s pro Fall). Aufruf:
    python3 tests/fuzz/rc001_blocks.py <arbeitsordner> <seed> <anzahl>
    node tests/fuzz/rc001_blocks_oracle.js <arbeitsordner>/cases-<seed>.json [pfad/zu/markdown-it]
Erwartung: 0 stille Durchlässe.
Copyright (c) 2026 Jakob Flaman · SPDX-License-Identifier: MIT
"""
import json
import random
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "check-conventions.py"
S = Path(sys.argv[1]); seed = int(sys.argv[2]); N = int(sys.argv[3]); random.seed(seed)
BLOCKS=["Das System SHALL a.", "- Punkt", "  - Unterpunkt", "1. Nummer", "> Zitat", "<div>", "</div>", "<!--", "-->",
        "```", "~~~", "  ```", "   ```", "    ```", "```text", "", "Text SHOULD hier.", "Es MAY auch.", "    eingerückt SHOULD",
        "[x]: /u \"Titel", "\"", "| a | b |", "|---|---|", "<script>", "</script>", "    ~~~", "- ```", "> ```", "SHALL b",
        "- Format:\n  ```json\n  {}\n```", "```\nText SHOULD hier.\n```", "    ```\nx\n```", "\t```", "  ~~~\n~~~"]
proj=S/"p"; cases=[]
for n in range(N):
    body=[random.choice(BLOCKS) for _ in range(random.randint(2,9))]
    if not any("SHOULD" in b or "MAY" in b for b in body): body.insert(random.randrange(len(body)+1), "Text SHOULD hier.")
    body=["Das System SHALL x."]+body
    text="## Purpose\n\nTestdaten.\n\n## Requirements\n\n### Requirement: R (AB-1, Must)\n"+"\n".join(body)+"\n\n#### Scenario: S\n- **WHEN** x\n- **THEN** y\n"
    if proj.exists(): shutil.rmtree(proj)
    (proj/"openspec/specs/cap").mkdir(parents=True); (proj/"openspec/specs/cap/spec.md").write_text(text)
    r=subprocess.run([sys.executable,"-I",str(SCRIPT)],cwd=proj,capture_output=True,text=True)
    req="\n".join(body)
    cases.append({"t":req,"rc":r.returncode,"out":r.stdout[:200]})
json.dump(cases,open(S/f"cases-{seed}.json","w"))
