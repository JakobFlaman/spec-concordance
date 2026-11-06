---
name: change-proposal
description: Überführt eine Meldung (Fehler, Verbesserungswunsch, Frage, GitHub-Issue) in einen OpenSpec-Change mit Klassifikation, Bezug zur Spezifikation, Abnahmekriterien und Tasks. Verwenden, wenn etwas am Produkt geändert oder ein Fehler behoben werden soll.
---

# Change-Proposal

## Eingabe

Eine Meldung: Freitext, GitHub-Issue-Nummer oder Meldepaket aus der Anwendung.

## Ablauf

1. **Klassifizieren:** `bug`, `feature`, `frage` oder `security`.
   - `security` → sofort stoppen, nicht öffentlich weiterbearbeiten, Maintainer informieren (siehe SECURITY.md).
   - `frage` → kein Change; prüfen, ob die Doku die Antwort enthält. Fehlt sie, Change vom Typ `docs` anlegen.
2. **Gegen die Spezifikation prüfen:** In `openspec/specs/` die betroffenen Anforderungen suchen.
   - Bug: Welche Anforderung wird verletzt? Fehlt die Anforderung, ist es kein Bug, sondern eine Lücke → `feature`.
   - Feature: Widerspricht es bestehenden Anforderungen oder der Roadmap? Passt es zum Open-Core-Schnitt?
3. **Schweregrad (nur Bug):** `kritisch` (Datenverlust, Sicherheit, kein Arbeiten möglich) · `hoch` · `mittel` · `niedrig`. Kritisch → Hotfix-Pfad.
4. **Change anlegen** mit OpenSpec (`/opsx:propose` bzw. `openspec` CLI) unter `openspec/changes/<id>/`:
   - `proposal.md` – Warum, Klassifikation, Schweregrad, Bezug zur Meldung
   - Spec-Deltas – geänderte oder neue Anforderungen, je mit Abnahmekriterium im Format *Gegeben / Wenn / Dann*
   - `tasks.md` – kleine, einzeln prüfbare Tasks; bei Bugs zuerst: «Regressionstest schreiben, der den Fehler zeigt»
   - `design.md` mit Abschnitt **«Grenzen»** – Pflicht, wenn das Ergebnis des Changes eine automatische Prüfung, Erkennung oder Entscheidung ist (siehe Regeln)
5. **Rückkopplung vormerken:** Notieren, ob Doku, Rollenkonzept, Teststrategie oder Roadmap betroffen sind.
6. **Council-Review anstossen:** `/spec-concordance:council-review` auf den neuen Change.

## Regeln

- Jede Meldung bekommt eine Rückmeldung an den Melder, auch eine Ablehnung – mit Begründung.
- Ein Change behandelt genau ein Thema. Mehrere Themen in einer Meldung → mehrere Changes.
- Abnahmekriterien müssen als automatischer Test formulierbar sein. Wo das nicht geht (z. B. Verhalten eines KI-Agenten, Installation), wird das Szenario mit `> Manueller Test: …` gekennzeichnet und der Nachweis genannt.
- **Grenzen vor der Umsetzung:** Ist das Ergebnis des Changes eine automatische Prüfung, Erkennung oder Entscheidung – zum Beispiel ein Prüfskript, eine Validierungsregel, ein Gate-Kriterium, eine Erkennung von Eingaben –, hat `design.md` vor dem Council-Review einen Abschnitt «Grenzen». Er benennt, was bewusst nicht abgedeckt ist und wogegen geprüft wird. Kein Abschnitt nötig ist bei reiner Doku, Vorlagen oder Umbenennungen. Ob ein Change darunter fällt, entscheidet das Council; im Zweifel gilt die Pflicht.
- **Absolute Zusagen** («nie», «immer», «in jedem Fall», «kein … durchgeht») stehen in Spec und Design nur zusammen mit einem Vergleichsmassstab (wogegen geprüft wird, z. B. ein Referenzparser) und den Grenzen. Grenzen, die erst nach einem Gate-Befund nachgetragen werden, zählen nur mit Entscheid des Maintainers (siehe `quality-gate`).
