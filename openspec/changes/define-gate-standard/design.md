# Design: Massstab für das Qualitäts-Gate

## Entscheid

| Punkt | Festlegung | Begründung |
|---|---|---|
| Name G7 | «Spezifikation nachgeführt und stimmt mit dem Verhalten überein»; Teil (a) Deltas vollständig und widerspruchsfrei, Teil (b) Verhalten | So wurde G7 im Trockenlauf faktisch geprüft; die formale Prüfung bleibt erhalten (D6) |
| ❌-Kriterium | (a) ausdrückliche Zusage gebrochen oder (b) realistischer stiller Verstoss | Entspricht dem Entscheid des Maintainers nach Gate-Lauf 18 |
| «realistisch» | kann bei der normalen Arbeit entstehen (Tippfehler, übliche Formatierung, verbreitete Muster) | Gegenbegriff «konstruiert»: entsteht nur durch absichtliche Verschleierung |
| Einordnung | Prüfer ordnet jeden G7-Befund ein; im Zweifel «realistisch»; Beobachtung = Befund ohne Schweregrad | Lieber ein Lauf zu viel als ein übersehener Fehler |
| Entscheide des Maintainers | Umstufen oder einen realistischen, seltenen Befund mit Begründung in einen Folge-Change verschieben; immer im Gate-Protokoll | Referenzfall B1 aus Gate-Lauf 19 (Zeilentrennung bei U+2028): wurde verschoben, ohne dass die Regel das vorsah (F1, S2) |
| Gültige Grenzen | nur beim Council-Review vorhandene oder vom Maintainer bestätigte | Sonst liesse sich jede Grenze nach dem Gate-Befund nachtragen (F2) |
| Sicherheitszweck | konstruierte Fälle gelten als realistisch, ausser Grenze dokumentiert und von Security bestätigt | Bei Sicherheitsprüfungen ist absichtliche Umgehung das Bedrohungsmodell (S1) |
| Gate-Protokoll | `openspec/changes/<id>/gate-log.md`; Felder Lauf, Datum, Ergebnis, ❌-Punkte mit Anforderung, Einordnung, Entscheide, optional Dauer; Skill liest es vor jedem Lauf | Unabhängige Prüfer haben kein gemeinsames Gedächtnis (O1, E1, A3) |
| Grenzen | Abschnitt «Grenzen» in `design.md` vor dem Council-Review, Pflicht bei Changes, deren Ergebnis eine automatische Prüfung, Erkennung oder Entscheidung ist; Entscheid im Council, im Zweifel Pflicht | Grenzen nach der Umsetzung festzulegen (Trockenlauf: nach Lauf 18) wirkt wie Nachbessern der Spec |
| Absolute Zusagen | «nie», «immer», «in jedem Fall» nur mit Vergleichsmassstab (wogegen geprüft wird) und Grenzen | T2: ohne Massstab ist jeder konstruierte Fall ein Bruch der Zusage |
| Eskalation | drei Läufe in Folge mit demselben ❌-Punkt, bei G3 und G7 zusätzlich dieselbe Anforderung | Drei Läufe zeigen ein Muster; im Trockenlauf wäre die Frage nach Lauf 12 statt 18 gekommen |
| Wo festgehalten | Skills `quality-gate`, `change-proposal`; Rolle Testmanagement; PR-Vorlage; Vorgehensmodell; Capability `change-process`, weil die Regeln Proposal, Review und Gate betreffen (A5) | Rollen sind Dateien (CLAUDE.md); Regeln stehen dort, wo sie angewendet werden |

## Alternativen

| Alternative | Verworfen, weil |
|---|---|
| G7 ohne Massstab lassen, Maintainer entscheidet fallweise | Genau das hat die Schlaufe verursacht |
| Nur gebrochene Zusagen zählen (kein «realistischer Verstoss») | Ein Change ohne ausdrückliche Zusage wäre nie ❌, obwohl er Fehler durchlässt |
| Feste Höchstzahl an Gate-Läufen | Ein Abbruch ohne Entscheid lässt Qualität offen; die Eskalation erzwingt einen Entscheid |

## Grenzen

- Die Einordnung «realistisch» / «konstruiert» ist ein Urteil des Prüfers und lässt sich nicht automatisch prüfen. Die Tests prüfen nur, dass die Regeln in Skills und Rolle stehen.
- Ob ein Agent die Regeln tatsächlich einhält, prüft kein automatischer Test; Nachweis sind die Proben mit unabhängigen Agenten (Tasks 3.1) und das Gate-Protokoll.
- Die Proben zeigen das Verhalten eines Agenten bei einem Lauf; KI-Agenten antworten nicht deterministisch.
