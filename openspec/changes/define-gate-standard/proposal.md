# Proposal: Massstab für das Qualitäts-Gate und Grenzen vor der Umsetzung

## Why

Im Trockenlauf mit dem Change `add-priority-convention` brauchte das Qualitäts-Gate 19 Läufe, davon 18 nicht bestanden (Erkenntnisse T1 und T2 in `docs/de/pilot-blattwerk.md`). Jeder Befund war echt, aber zwei Lücken im Vorgehen haben die Schlaufe verlängert:

- **T1:** Der Massstab für Gate-Punkt G7 war offen. Die Skill-Datei sagt nur «Spezifikation nachgeführt – keine Widersprüche». Ein unabhängiger, gezielt angreifender Prüfer findet bei jeder Näherung einen weiteren Randfall. Erst der Entscheid des Maintainers nach Lauf 18 (realistische Durchlässe sind Blocker, absichtliche Verschleierung ist dokumentierte Grenze) hat die Schlaufe beendet.
- **T2:** Absolute Zusagen in Spec und Design («nie ein stiller Durchlass», «in jedem Fall») ohne Vergleichsmassstab und ohne Grenzen haben jeden konstruierten Fall zum Blocker gemacht.

- **Klassifikation:** feature (Lücke im Vorgehensmodell)
- **Quelle:** Trockenlauf am Plugin, Erkenntnisse T1, T2 (Priorität hoch) und Teil von T8 (Eskalation)
- **Schweregrad:** entfällt

## What Changes

Neue Fähigkeit `quality-gate` (ADDED):

- `quality-gate`: G7 heisst neu «Spezifikation stimmt mit dem Verhalten überein» und hat einen festen Massstab. ❌ nur bei einer gebrochenen ausdrücklichen Zusage oder einem realistischen stillen Verstoss. Absichtliche Verschleierung und dokumentierte Grenzen sind Beobachtungen. Befunde werden als *realistisch* oder *konstruiert* eingeordnet.
- `change-proposal`: Changes mit Prüf- oder Automatisierungslogik nennen ihre Grenzen vor der Umsetzung. Absolute Zusagen nur mit Vergleichsmassstab und Grenzen.
- `quality-gate`: Scheitert das Gate dreimal in Folge am selben Punkt, wird vor dem nächsten Lauf der Maintainer zum Massstab befragt.
- Vorgehensmodell (de/en) nennt den Massstab.

## Out of Scope

- Übrige Erkenntnisse T3–T8 und P2–P10 – je eigener Change.
- Rückwirkende Änderung archivierter Changes.
