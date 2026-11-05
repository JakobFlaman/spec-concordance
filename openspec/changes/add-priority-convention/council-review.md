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
| D6 | Migration bestehender Projekte; RC-005 (damals RC-004) idempotent und ergänzend statt überschreibend; Warnmodus | major | Betr. (B3), Arch. (A5) | eingearbeitet (Spec, Tasks) |
| D7 | Geltungsbereich der Duplikatprüfung (pro Datei, `archive/` ausgenommen, nur Basis/ADDED/MODIFIED) | major | Entw. (E2) | eingearbeitet (Spec) |
| D8 | Test für RC-005 (damals RC-004) auf Textbaustein und SKILL.md verlegen; End-to-End als manueller Test | major | Test (T2), Entw. (E6) | eingearbeitet (Spec, Tasks) |
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

---

# Nachtrags-Review: Revision 2 (Erkennung über OpenSpec-CLI)

Datum: 2026-11-05 · Anlass: Design-Änderung nach sieben Gate-Läufen (Entscheid Maintainer: «OpenSpec als Parser») · Ergebnis: **freigegeben mit Auflagen**

Geprüft von den fünf betroffenen Rollen. Fachbereich nicht beteiligt: Die Konvention für Nutzer ändert sich nicht, nur die interne Prüfung.

| Rolle | Votum | major | minor |
|---|---|---|---|
| Security | Zustimmung mit Auflagen | 1 | 3 |
| Architektur | Zustimmung mit Auflagen | 2 | 2 |
| Support/Betrieb | Zustimmung mit Auflagen | 2 | 2 |
| Entwicklung (Aufwand M) | Zustimmung mit Auflagen | 2 | 2 |
| Testmanagement | Zustimmung mit Auflagen | 3 | 1 |

Alle Rollen bestätigen den Entscheid; Architektur, Entwicklung und Testmanagement haben das JSON von OpenSpec 1.16.0 selbst gegengeprüft.

## Entscheidungsliste Revision 2

| Nr. | Auflage | Schweregrad | Rolle(n) | Status |
|---|---|---|---|---|
| N1 | CI: `actions/setup-node` und OpenSpec in exakt fixierter Version (1.16.0); `permissions: contents: read`; nur `pull_request`; Telemetrie aus (`DO_NOT_TRACK=1`) | major | Sec. (S3, S4), Betr. (B1), Entw. (E2), Arch. (A2) | offen |
| N2 | Aufrufer auf Projektstamm umstellen (CI, CLAUDE.md, process-model DE/EN, Test-Summary); Pfad ohne `openspec/` → Exit 2 mit klarer Meldung und Test | major | Arch. (A1), Entw. (E2), Test (T1), Betr. (B3) | offen |
| N3 | Version beim Start prüfen (`openspec --version` < 1.16 → Exit 2 mit gefundener und benötigter Version); fehlende JSON-Felder → Exit 2, nie still bestehen; Szenarien und Vertragstest | major | Betr. (B2), Arch. (A3), Entw. (E3) | offen |
| N4 | Fixtures als OpenSpec-Projekte mit minimaler `proposal.md` (genau eines ohne, für RC-008); Zuordnung alte → neue Tests in der Test-Summary | major | Test (T2) | offen |
| N5 | Tests: in der CI kein stilles Überspringen bei fehlender CLI; «OpenSpec fehlt» über `OPENSPEC_BIN`; Attrappe für «zu alt» und Fehlermeldung | major | Test (T3), Betr. (B4) | offen |
| N6 | Tasks-Abschnitt 10 «Revision 2» mit Rückverfolgung auf RC-008/RC-001 | major | Entw. (E1), Arch. (A1) | offen |
| N7 | S1 in design.md ersetzen: Standardbibliothek + OpenSpec-CLI in fixierter Version (MIT) | major | Sec. (S3) | offen |
| N8 | Fehler von OpenSpec erkennen: Exitcode ≠ 0 oder `status[]` mit `severity: error`; `message` weitergeben | minor | Entw. (E3) | offen |
| N9 | Namen von Specs und Changes gegen festes Muster prüfen (OpenSpec kennt kein `--`); gelesene Dateien nach `resolve()` unter `<STAMM>/openspec/`; Fixture | minor | Sec. (S5) | offen |
| N10 | `OPENSPEC_BIN` nur aus der Umgebung; Unterprozess mit Timeout; OpenSpec-Umgebungsvariablen, die Verzeichnisse umlenken, für den Aufruf entfernen | minor | Sec. (S6) | offen |
| N11 | Pfadableitung und Felder benennen; n-tes Vorkommen eines Namens → n-te Fundstelle; RC-008 präzisieren («Datei nur zur Zeilenzuordnung gelesen»); Tests für Zeile, Codeblock, verschachtelte Capability, Fallback Zeile 0 | minor | Entw. (E4), Arch. (A4), Test (T4) | offen |
| N12 | Doku: OpenSpec als Voraussetzung im README, Aufruf, `OPENSPEC_BIN`, Exit-2-Ursachen mit Handlungsempfehlung | minor | Betr. (B3) | offen |
| N13 | ADR «OpenSpec-CLI als Parser» nachtragen, sobald `docs/adr/` existiert | minor | Arch. | Folge-Change |
