# Council-Review: add-priority-convention

Datum: 2026-11-05 · Ergebnis: **freigegeben mit Auflagen**

## Voten

| Rolle | Votum | blocker | major | minor |
|---|---|---|---|---|
| Security | Zustimmung mit Auflagen | 0 | 0 | 2 |
| Architektur | Zustimmung mit Auflagen | 0 | 4 | 2 |
| Support/Betrieb | Zustimmung mit Auflagen | 0 | 3 | 2 |
| Entwicklung (Aufwand S, knapp M) | Zustimmung mit Auflagen | 0 | 2 | 4 |
| Fachbereich | Zustimmung mit Auflagen | 0 | 2 | 3 |
| Testmanagement | Zustimmung mit Auflagen | 0 | 2 | 2 |

Abdeckung laut Testmanagement: 6 von 8 Abnahmekriterien mit geplantem Test; Testlauf vor Umsetzung nicht ausgeführt; `openspec validate --strict` gültig.

## Widersprüche

| Nr. | Gegenstand | Positionen | Entscheid |
|---|---|---|---|
| W1 | Bezugsweg des Prüfskripts für Projekte | Architektur (A4): festlegen *oder* RC-005 auf Plugin beschränken; Betrieb (B2): Bezugsweg festlegen | RC-005 auf das Plugin-Repo beschränkt; Projekt-CI als eigener Folge-Change (ein Change = ein Thema) |

## Entscheidungsliste

| Nr. | Auflage | Schweregrad | Rolle(n) | Status |
|---|---|---|---|---|
| D1 | Erkennungsregel für SHOULD/MAY festlegen (nur Anforderungstext vor dem ersten Szenario, nur Grossschreibung als ganzes Wort, ohne Inline-Code und Zitate); RC-001 so formulieren, dass der Change die eigene Prüfung besteht; Fixture «Erwähnung» | major | Test (T1), Arch. (A3), Betr. (B1), Entw. (E1) | eingearbeitet (Spec) |
| D2 | Umpriorisierung regeln: RENAMED mit FROM/TO; Skript meldet MODIFIED, dessen Titel nur in der Priorität von der Basis abweicht | major | Fach (F1), Arch. (A2) | eingearbeitet (Spec) |
| D3 | Schnittstelle des Skripts in `design.md`: Argumente, Ausgabe, Exitcodes 0/1/2, ID-Muster, Delta-Abschnitte; Begründung des Konventionsentscheids (ADR-Ersatz) | major | Arch. (A1, A6), Betr. (B4), Entw. (E3, E5) | eingearbeitet (design.md) |
| D4 | Bezugsweg für Projekte (siehe W1); Python-Voraussetzung im README | major | Arch. (A4), Betr. (B2) | eingearbeitet (Spec, Tasks) |
| D5 | Could-Anforderungen: Entscheid, ob in OpenSpec; `project-init` Schritt 3 angleichen | major | Fach (F2) | eingearbeitet (Spec, Tasks) |
| D6 | Migration bestehender Projekte; RC-004 idempotent und ergänzend statt überschreibend; Warnmodus | major | Betr. (B3), Arch. (A5) | eingearbeitet (Spec, Tasks) |
| D7 | Geltungsbereich der Duplikatprüfung (pro Datei, `archive/` ausgenommen, nur Basis/ADDED/MODIFIED) | major | Entw. (E2) | eingearbeitet (Spec) |
| D8 | Test für RC-004 auf Textbaustein und SKILL.md verlegen; End-to-End als manueller Test | major | Test (T2), Entw. (E6) | eingearbeitet (Spec, Tasks) |
| D9 | Nur Standardbibliothek (`unittest`), nur lesend, keine Ausführung von Inhalten | minor | Sec. (S1, S2), Entw. (E5) | eingearbeitet (design.md) |
| D10 | Scan-Umfang der CI auf `openspec/specs/` und `openspec/changes/` begrenzen (Fixtures nicht mitscannen) | minor | Test (T4) | eingearbeitet (Tasks) |
| D11 | CI-Task für das Skript; eigene `config.yaml` erhält die Regel (Dogfooding); Task 2.4 zuordnen | minor | Entw. (E4) | eingearbeitet (Tasks) |
| D12 | Unklare Aufteilung gemischter Prioritäten beim Maintainer erfragen, nicht raten | minor | Fach (F3) | eingearbeitet (Spec) |
| D13 | SHALL vs. Verbindlichkeit für Lastenheft-Gewohnte erklären; RFC 2119 erklären | minor | Fach (F4) | eingearbeitet (Tasks) |
| D14 | Konvention gilt auch für nicht-funktionale Anforderungen | minor | Fach (F5) | eingearbeitet (Spec) |
| D15 | Nachweis «Should validiert» über eigene Spec (RC-005) in der Test-Summary benennen | minor | Test (T3) | eingearbeitet (Tasks) |
| D16 | Versionierung: unter [Unreleased] sammeln, `plugin.json` beim Release | minor | Betr. (B5) | eingearbeitet (Tasks) |

Hinweis Entwicklung, ausserhalb dieses Changes: Die Pilot-Specs in `pdf-concordance` tragen bei Must-Anforderungen noch keine Priorität im Titel → Folge-Change dort.

## Einzelvoten

Vollständig in `council-review-votes.md`.
