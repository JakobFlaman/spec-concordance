---
name: quality-gate
description: Prüft, ob ein umgesetzter OpenSpec-Change archiviert werden darf – Tests, Council-Votum, Spezifikation, Doku und Changelog. Verwenden vor jedem Archivieren eines Changes und vor jedem Release.
---

# Qualitäts-Gate

Das Gate ist eine Checkliste mit hartem Ergebnis: **bestanden** oder **nicht bestanden**. Es gibt kein «fast bestanden».

## Prüfpunkte

| Nr. | Prüfpunkt | Wie prüfen |
|---|---|---|
| G0 | Change ist strukturell gültig | `openspec validate <id>` ausführen |
| G1 | Alle Tasks in `tasks.md` erledigt | Checkboxen auswerten |
| G1a | Rückverfolgbarkeit | Jede Task gehört zu einer Anforderung, jede Anforderung hat eine Task und mindestens ein Szenario |
| G2 | Testlauf grün | Testbefehl aus CLAUDE.md ausführen, Ausgabe festhalten |
| G3 | Jedes Abnahmekriterium hat einen Test | Abgleich Spec-Delta ↔ Tests |
| G4 | Bei Bug: Regressionstest vorhanden | Test, der ohne Fix fehlschlägt |
| G5 | Council-Review liegt vor, Ergebnis nicht «nicht freigegeben» | `council-review.md` im Change |
| G6 | Alle Auflagen mit Schweregrad `blocker` und `major` erledigt | Status in der Entscheidungsliste; `minor` darf als eigener Change folgen |
| G7 | Spezifikation nachgeführt | Spec-Deltas vollständig, keine Widersprüche |
| G8 | Doku nachgeführt | Benutzer-/Betriebsdoku betroffen? Dann geändert? |
| G9 | CHANGELOG-Eintrag | Unter `[Unreleased]` |
| G10 | Test-Summary abgelegt | `docs/test-reports/<datum>-<change-id>.md` |
| G11 | Freigabe Maintainer | Ausdrückliche Bestätigung im Chat oder im PR |

## Ablauf

1. Prüfpunkte G0–G10 selbst prüfen. G2 wird **ausgeführt**, nicht aus früheren Ausgaben übernommen.
2. Ergebnis als Tabelle ausgeben: Prüfpunkt, Status (✅/❌), Nachweis.
3. Ist ein Punkt ❌ → **nicht bestanden**, mit Liste der fehlenden Punkte. Kein Archivieren.
4. Sind G0–G10 ✅ → Maintainer um Freigabe (G11) bitten.
5. Erst nach Freigabe: `openspec archive <id>`.

## Regeln

- Das Gate darf nicht vom selben Agenten ausgeführt werden, der den Change umgesetzt hat, wenn ein unabhängiger Agent verfügbar ist.
- Ausnahmen (z. B. Hotfix ohne vollständiges Review) nur mit ausdrücklicher Begründung des Maintainers; die Ausnahme wird im CHANGELOG vermerkt und das Review nachgeholt.
