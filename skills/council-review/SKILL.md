---
name: council-review
description: Prüft eine Spezifikation oder einen OpenSpec-Change aus allen sechs Council-Rollen und erstellt ein Protokoll mit Voten, Befunden und Entscheidungsliste. Verwenden, wenn ein Change bereit zur Prüfung ist oder die ganze Spezifikation geprüft werden soll.
---

# Council-Review

## Eingabe

- Pfad zu einem Change (`openspec/changes/<id>/`) **oder** zur Gesamtspezifikation (`openspec/specs/`)
- Optional: zusätzliche Projektrollen aus `.spec-concordance/roles/`

## Ablauf

1. **Kontext laden:** Projektsteckbrief (`docs/artefakte/01-projektsteckbrief.md`), Rollen- und Berechtigungskonzept, CLAUDE.md und den zu prüfenden Change lesen.
2. **Rollen unabhängig prüfen lassen:** Für jede Rolle einen eigenen Subagenten starten – `council-security`, `council-architektur`, `council-betrieb`, `council-entwicklung`, `council-fachbereich`, `council-testmanagement` sowie projektspezifische Rollen. Alle parallel, ohne dass sie die Voten der anderen sehen.
3. **Voten einsammeln** im vorgegebenen Format jeder Rolle.
4. **Konsolidieren:**
   - Widersprüche zwischen Rollen ausdrücklich benennen, nicht glätten.
   - Doppelte Befunde zusammenführen, beide Rollen nennen.
   - Jeder Befund trägt einen Schweregrad: `blocker` (muss vor der Umsetzung behoben sein), `major` (vor dem Archivieren), `minor` (darf als eigener Change folgen).
   - Entscheidungsliste: jede Auflage als Punkt mit Verantwortung (Maintainer) und Status `offen`.
5. **Gesamtergebnis bestimmen:**
   - Ein `VETO` (Security), eine `ABLEHNUNG` oder ein offener Befund mit Schweregrad `blocker` → **nicht freigegeben**
   - Nur Zustimmungen → **freigegeben**
   - Sonst → **freigegeben mit Auflagen**
6. **Protokoll schreiben** nach `openspec/changes/<id>/council-review.md` (bei Gesamtprüfung nach `docs/council-review.md`).

## Protokollformat

```markdown
# Council-Review: <Change-ID oder «Gesamtspezifikation»>
Datum: <JJJJ-MM-TT> · Ergebnis: <freigegeben | freigegeben mit Auflagen | nicht freigegeben>

## Voten
| Rolle | Votum | Befunde |
|---|---|---|

## Widersprüche
## Entscheidungsliste
| Nr. | Auflage | Schweregrad | Rolle(n) | Status |
|---|---|---|---|---|

## Einzelvoten
<vollständige Voten der Rollen>
```

## Regeln

- Der Agent, der den Change umgesetzt hat, darf ihn nicht selbst reviewen.
- Das Review ersetzt die Freigabe durch den Maintainer nicht; es bereitet sie vor.
- Stille Zustimmung gilt nur bei menschlichen Reviewern nach Ablauf der Frist (Standard: fünf Arbeitstage), nie bei KI-Rollen.
