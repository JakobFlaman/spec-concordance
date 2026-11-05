# Projektspezifische Council-Rollen

Lege hier pro Fachrolle eine Datei an, z. B. `erfahrener-handwerker.md`. Sie wird bei `/spec-concordance:council-review` zusätzlich zu den sechs Standardrollen als unabhängiger Prüfer gestartet.

Aufbau wie die Standardrollen im Plugin (`agents/council-*.md`):

```markdown
---
name: rolle-<kurzname>
description: <Blickwinkel in einem Satz>
tools: Read, Grep, Glob
---

# Rolle: <Name>

## Prüffragen
1. ...

## Votum
Rolle: <Name>
Votum: <ZUSTIMMUNG | ZUSTIMMUNG MIT AUFLAGEN | ABLEHNUNG>
Befunde:
- [X1] <Befund> – Fundstelle – Auflage
Begründung: <zwei bis vier Sätze>
```
