# Design: Massstab für das Qualitäts-Gate

## Entscheid

| Punkt | Festlegung | Begründung |
|---|---|---|
| Name G7 | «Spezifikation stimmt mit dem Verhalten überein» | So wurde G7 im Trockenlauf faktisch geprüft; «nachgeführt» deckt nur die Form ab |
| ❌-Kriterium | (a) ausdrückliche Zusage gebrochen oder (b) realistischer stiller Verstoss | Entspricht dem Entscheid des Maintainers nach Gate-Lauf 18 |
| «realistisch» | kann bei der normalen Arbeit entstehen (Tippfehler, übliche Formatierung, verbreitete Muster) | Gegenbegriff «konstruiert»: entsteht nur durch absichtliche Verschleierung |
| Einordnung | Prüfer ordnet jeden G7-Befund ein; im Zweifel «realistisch» | Lieber ein Lauf zu viel als ein übersehener Fehler; der Maintainer kann umstufen |
| Grenzen | Abschnitt «Grenzen» in `design.md` vor dem Council-Review, Pflicht bei Prüf-, Erkennungs- und Automatisierungslogik | Grenzen nach der Umsetzung festzulegen (Trockenlauf: nach Lauf 18) wirkt wie Nachbessern der Spec |
| Absolute Zusagen | «nie», «immer», «in jedem Fall» nur mit Vergleichsmassstab (wogegen geprüft wird) und Grenzen | T2: ohne Massstab ist jeder konstruierte Fall ein Bruch der Zusage |
| Eskalation | nach drei nicht bestandenen Läufen in Folge am selben Gate-Punkt und derselben Anforderung | Drei Läufe zeigen ein Muster; im Trockenlauf wäre die Frage nach Lauf 12 statt 18 gekommen |
| Wo festgehalten | Skills `quality-gate`, `change-proposal`; Rolle Testmanagement; Vorgehensmodell | Rollen sind Dateien (CLAUDE.md); Regeln stehen dort, wo sie angewendet werden |

## Alternativen

| Alternative | Verworfen, weil |
|---|---|
| G7 ohne Massstab lassen, Maintainer entscheidet fallweise | Genau das hat die Schlaufe verursacht |
| Nur gebrochene Zusagen zählen (kein «realistischer Verstoss») | Ein Change ohne ausdrückliche Zusage wäre nie ❌, obwohl er Fehler durchlässt |
| Feste Höchstzahl an Gate-Läufen | Ein Abbruch ohne Entscheid lässt Qualität offen; die Eskalation erzwingt einen Entscheid |

## Grenzen

- Die Einordnung «realistisch» / «konstruiert» ist ein Urteil des Prüfers und lässt sich nicht automatisch prüfen. Die Tests prüfen nur, dass die Regeln in Skills und Rolle stehen.
- Ob ein Agent die Eskalation tatsächlich einhält, prüft kein Test; Nachweis ist die Dokumentation im Change.
