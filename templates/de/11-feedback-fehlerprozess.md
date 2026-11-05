# Feedback- und Fehlerprozess: <Projektname>

Stand: <JJJJ-MM-TT> · Querschnittsbaustein

## Eingangskanäle
| Kanal | Für | Öffentlich |
|---|---|---|
| GitHub Issues (Formulare) | Fehler, Wünsche | ja |
| Meldepaket aus der Anwendung | Fehler mit Diagnose | ja (ohne Personendaten) |
| SECURITY.md | Sicherheitslücken | nein |

## Klassifikation
`bug` · `feature` · `frage` · `security` · `docs`

## Schweregrade (Bug)
| Stufe | Bedeutung | Erstreaktion | Behebung |
|---|---|---|---|
| kritisch | Datenverlust, Sicherheit, kein Arbeiten möglich | 1 Arbeitstag | Hotfix |
| hoch | Kernfunktion gestört, Umgehung schwierig | 3 Arbeitstage | nächstes Release |
| mittel | Funktion gestört, Umgehung möglich | 5 Arbeitstage | geplant |
| niedrig | Schönheitsfehler | 10 Arbeitstage | bei Gelegenheit |

## Ablauf
Meldung → Klassifikation → `/spec-concordance:change-proposal` → Council-Review → Umsetzung → `/spec-concordance:quality-gate` → Release → Rückmeldung an Melder

## Rückkopplung
| Erkenntnis | fliesst in |
|---|---|
| Behobener Fehler | Regressionstest (08) |
| Wiederkehrende Frage | Dokumentation |
| Berechtigungsproblem | Rollenkonzept (05) |
| Wunsch | Roadmap (10), ggf. Open-Core-Modell (03) |

## Rollen
Melder (jeder) · Maintainer (Triage, Entscheid) · Reviewer (Vier-Augen) · Council (jede Änderung)
