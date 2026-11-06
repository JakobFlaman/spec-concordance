# Proposal: Prüfung auf Geheimnisse in Spec-Dateien

## Why
Spec-Dateien sollen keine API-Schlüssel oder Passwörter enthalten. Ein neues Skript `scripts/check-secrets.py` durchsucht `openspec/` nach typischen Mustern (z. B. `sk-…`, `ghp_…`, `password=`) und endet bei einem Fund mit Exit 1. Es läuft in der CI.

- Klassifikation: feature
