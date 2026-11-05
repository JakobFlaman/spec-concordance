# Teststrategie: <Projektname>

Stand: <JJJJ-MM-TT> · Querschnittsbaustein

## Testebenen
| Ebene | Werkzeug | Was wird geprüft | Wann läuft es |
|---|---|---|---|
| Unit | | | bei jedem Commit |
| Integration | | | bei jedem PR |
| End-to-End | | | vor Release |
| Sicherheit | | | vor Release |
| Usability | | | je Phase, mit Fachbereichsrollen |
| Performance | | Grenzwerte aus N-xxx | periodisch |

## Testbefehl
```bash
# Wird von quality-gate (G2) ausgeführt
<befehl>
```

## Definition of Done
- [ ] Abnahmekriterien als Tests umgesetzt
- [ ] Alle Tests grün
- [ ] Bei Bugfix: Regressionstest vorhanden
- [ ] Test-Summary abgelegt

## Testdaten
<!-- Herkunft, Kennzeichnung als synthetisch, Stufen (z. B. 10k / 100k / 1M), Reproduzierbarkeit -->

## Test-Reporting
<!-- Ablage unter docs/test-reports/, Format, Vergleich mit Vorlauf, Historie je Themengebiet -->
