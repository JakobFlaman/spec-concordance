#!/usr/bin/env python3
"""Attrappe der OpenSpec-CLI für Fehlerfälle von scripts/check-conventions.py (RC-008).

Verhalten über FAKE_OPENSPEC_MODE:
  old            --version meldet 1.15.0
  error          jeder Aufruf scheitert mit JSON-Fehlermeldung (Exitcode 1)
  missing-field  «list --specs» liefert Einträge ohne «id»
  bad-name       «list --specs» liefert eine Spec «-x» (Argument-Injection)
  unknown-line   liefert eine Anforderung, deren Name nicht in der Datei steht

Copyright (c) 2026 Jakob Flaman · SPDX-License-Identifier: MIT
"""
import json
import os
import sys

mode = os.environ.get("FAKE_OPENSPEC_MODE", "")
args = sys.argv[1:]


def out(obj, code=0):
    print(json.dumps(obj))
    sys.exit(code)


if args == ["--version"]:
    print("1.15.0" if mode == "old" else "1.16.0")
    sys.exit(0)

if mode == "error":
    out({"status": [{"severity": "error", "code": "fake", "message": "Attrappe meldet einen Fehler"}]}, 1)

if args[:2] == ["list", "--specs"]:
    if mode == "missing-field":
        out({"specs": [{"idx": "demo"}]})
    if mode == "bad-name":
        out({"specs": [{"id": "-x"}]})
    out({"specs": [{"id": "demo"}]})

if args[:1] == ["list"]:
    out({"changes": []})

if args[:1] == ["show"]:
    out({"id": "demo", "requirements": [{"name": "Nicht in der Datei (X-1)", "text": "Das System SHALL etwas tun."}]})

out({"status": [{"severity": "error", "message": f"Attrappe kennt den Aufruf nicht: {args}"}]}, 1)
