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
| G3 | Jedes Abnahmekriterium hat einen Test | Abgleich Spec-Delta ↔ Tests; als «Manueller Test» gekennzeichnete Szenarien brauchen einen ausgeführten, festgehaltenen Nachweis |
| G4 | Bei Bug: Regressionstest vorhanden | Test, der ohne Fix fehlschlägt |
| G5 | Council-Review liegt vor, Ergebnis nicht «nicht freigegeben» | `council-review.md` im Change |
| G6 | Alle Auflagen mit Schweregrad `blocker` und `major` erledigt | Status in der Entscheidungsliste; `minor` darf als eigener Change folgen |
| G7 | Spezifikation nachgeführt und stimmt mit dem Verhalten überein | (a) Spec-Deltas vollständig und widerspruchsfrei; (b) keine ausdrückliche Zusage von Spec oder Design gebrochen und kein Verstoss gegen eine Anforderung, der realistisch und still durchgeht – Massstab siehe unten |
| G8 | Doku nachgeführt | Benutzer-/Betriebsdoku betroffen? Dann geändert? |
| G9 | CHANGELOG-Eintrag | Unter `[Unreleased]` |
| G10 | Test-Summary abgelegt | `docs/test-reports/<datum>-<change-id>.md` |
| G11 | Freigabe Maintainer | Ausdrückliche Bestätigung; bei PR-Pflicht ist das Mergen des Pull Requests die Freigabe |

## Massstab für G7

- **Realistisch** ist ein Fall, der bei der normalen Arbeit entstehen kann (Tippfehler, übliche Formatierung, verbreitete Muster, kopierter Text).
- **Konstruiert** ist ein Fall, der nur durch absichtliche Verschleierung entsteht.
- Jeder G7-Befund wird als «realistisch» oder «konstruiert» eingeordnet. **Im Zweifel gilt «realistisch».**
- Ein realistischer Befund macht G7 ❌. Ein konstruierter Befund und ein Befund innerhalb einer gültigen Grenze ist eine **Beobachtung**: Er hat keinen Schweregrad, wird im Ergebnis aufgeführt und macht G7 nicht ❌.
- **Gültige Grenzen** sind nur solche, die beim Council-Review bereits im Abschnitt «Grenzen» von `design.md` standen, oder die der Maintainer später ausdrücklich als Grenze bestätigt hat (festgehalten im Gate-Protokoll). Eine nach dem Befund nachgetragene Grenze ohne diesen Entscheid zählt nicht.
- **Sicherheitszweck:** Bei Anforderungen mit Sicherheitszweck (Klassifikation `security` oder Befund der Rolle Security) gilt ein konstruierter Fall als realistisch, ausser er ist als Grenze dokumentiert und die Rolle Security hat ihr im Council zugestimmt.
- **Entscheide des Maintainers:** Nur der Maintainer kann eine Einordnung umstufen oder einen realistischen Befund mit Begründung in einen Folge-Change verschieben. Jeder solche Entscheid steht mit Begründung im Gate-Protokoll. Ohne festgehaltenen Entscheid bleibt ein realistischer Befund ❌.

## Gate-Protokoll

Jeder Lauf wird in `openspec/changes/<id>/gate-log.md` festgehalten, damit auch ein neuer, unabhängiger Prüfer den Verlauf kennt:

```markdown
# Gate-Protokoll: <change-id>

| Lauf | Datum | Ergebnis | Nicht erfüllt (Gate-Punkt: Anforderung) | Dauer (optional) |
|---|---|---|---|---|

## Befunde zu G7
| Lauf | Befund | Einordnung | Folge |
|---|---|---|---|

## Entscheide des Maintainers
| Datum | Lauf | Entscheid | Begründung |
|---|---|---|---|
```

## Ablauf

1. **Gate-Protokoll lesen**, falls vorhanden. Eskalation prüfen (siehe unten); greift sie, zuerst den Maintainer fragen und keinen Lauf starten.
2. Prüfpunkte G0–G10 selbst prüfen. G2 wird **ausgeführt**, nicht aus früheren Ausgaben übernommen.
3. Ergebnis als Tabelle ausgeben: Prüfpunkt, Status (✅/❌/n.a.), Nachweis. G7-Befunde mit Einordnung, Beobachtungen getrennt aufführen.
4. Lauf im Gate-Protokoll nachtragen.
5. Ist ein Punkt ❌ → **nicht bestanden**, mit Liste der fehlenden Punkte. Kein Archivieren.
6. Sind G0–G10 ✅ → Maintainer um Freigabe (G11) bitten.
7. Archivieren (`openspec archive <id>`): ohne PR-Pflicht erst nach der Freigabe; mit PR-Pflicht als letzter Commit im Pull Request nach bestandenem Gate – wirksam wird es mit dem Mergen.

## Eskalation

Ist in **drei aufeinanderfolgenden Läufen** derselbe Gate-Punkt ❌ – bei G3 und G7 zusätzlich zur selben Anforderung –, wird vor dem nächsten Lauf der Maintainer gefragt, ob der Massstab gilt, angepasst wird oder Befunde als Grenze bestätigt werden. Die Antwort steht im Gate-Protokoll unter «Entscheide des Maintainers». Ein bestandener Lauf, ein Lauf, in dem dieser Punkt ✅ ist, oder die festgehaltene Antwort des Maintainers setzt die Zählung zurück.

## Regeln

- Das Gate darf nicht vom selben Agenten ausgeführt werden, der den Change umgesetzt hat, wenn ein unabhängiger Agent verfügbar ist.
- Ausnahmen (z. B. Hotfix ohne vollständiges Review) nur mit ausdrücklicher Begründung des Maintainers; die Ausnahme wird im CHANGELOG vermerkt und das Review nachgeholt.
