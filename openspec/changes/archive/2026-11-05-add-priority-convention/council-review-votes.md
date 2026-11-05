# Council-Review add-priority-convention – Einzelvoten

Datum: 2026-11-05 · Sechs unabhängige Prüfer (KI-Subagenten). Gekürzt auf Befund und Auflage; Konsolidierung in `council-review.md`.

## Security – Zustimmung mit Auflagen
- [S1] minor – Keine Abhängigkeit für Skript und Tests festgelegt; CI heute ohne Paketinstallation. – Nur Standardbibliothek (`re`, `pathlib`, `unittest`), sonst Version fixieren und Lizenz festhalten.
- [S2] minor – Skript liest Markdown aus Pull Requests. – Nur in `openspec/specs/` und `openspec/changes/` lesen, nichts schreiben, nichts ausführen (kein eval/exec/Shell), keine Tokens.

Begründung: keine Personendaten, keine Geheimnisse, keine Berechtigungen; einzig der CI-Schritt ist neu angreifbar, bei nur lesendem Skript ohne Abhängigkeiten vernachlässigbar.

## Architektur – Zustimmung mit Auflagen
- [A1] major – Skript-Schnittstelle unbeschrieben (Argumente, Ausgabe, Exitcodes, ID-Grammatik, Delta-Abschnitte); «entspricht der Kennung» nicht prüfbar. – design.md; Formregel statt Quellabgleich; Szenarien für MODIFIED und RENAMED.
- [A2] major – Priorität im Titel macht sie zur Identität; Umpriorisierung = RENAMED, MODIFIED mit neuem Titel bricht beim Archivieren. – Regel und Szenario «Priorität ändern»; Skript erkennt MODIFIED, das sich nur in der Priorität unterscheidet.
- [A3] major – RC-001 enthält selbst SHOULD/MAY; CI würde am eigenen Change scheitern. – Erkennungsregel festlegen, RC-001 umformulieren, Fixture «Erwähnung in Backticks = gültig».
- [A4] major – Bezugsweg des Skripts für Projekt-CI offen. – festlegen oder RC-005 auf Plugin beschränken und Projekt-CI als eigenen Change.
- [A5] minor – Bestehender `context` in config.yaml, Idempotenz; Wahl `openspec-context.md` unbegründet. – Szenario «ergänzt, nicht überschrieben; idempotent»; Begründung.
- [A6] minor – Konventionsentscheid ohne Begründung/Alternativen. – ADR oder design.md.

ADR nötig: ja (alternativ design.md im Change).

## Support / Betrieb – Zustimmung mit Auflagen
- [B1] major – Selbstwiderspruch RC-001/RC-005; Fehlalarme bei Zitaten und Code. – Erkennungsregel als Szenario; RC-001 umformulieren oder Fixture.
- [B2] major – Bezugsweg für Projekte fehlt; README nennt kein Python. – Bezugsweg festlegen, Python-Version nennen, README in Impact/Tasks.
- [B3] major – Keine Migration bestehender Projekte (z. B. Blattwerk). – Szenario «bestehender context», Migrationsabschnitt mit RENAMED, Warnmodus für Übergang.
- [B4] minor – Meldungen ohne Regel-ID, Zeilennummer, Korrekturhinweis; Exitcodes nur «ungleich 0». – Datei, Zeile, Titel, RC-ID, Hinweis mit Doku-Verweis; Exitcodes 0/1/2; Fall «keine Specs».
- [B5] minor – Versionierung nicht in Tasks. – [Unreleased] sammeln, plugin.json beim Release nachziehen.

## Entwicklung – Zustimmung mit Auflagen · Aufwand S (knapp M)
- [E1] major – Selbstwiderspruch RC-001. – Nur Text zwischen Requirement-Zeile und erstem Szenario, nur Grossschreibung, ohne Inline-Code und Guillemets; Fixture.
- [E2] major – Geltungsbereich der Duplikatprüfung offen (Datei, Change, archive, MODIFIED). – Pro Spec-Datei, archive ausgenommen, nur Basis/ADDED/MODIFIED; Fixtures.
- [E3] minor – ID-Format nicht prüfbar definiert; Plugin hat keine Anforderungsquelle. – Muster `[A-Z]+(-[A-Z]+)*-\d+`, überschreibbar; Quellabgleich manuell; RC-nnn ist die Plugin-Quelle.
- [E4] minor – Keine Task baut das Skript in checks.yml ein; eigene config.yaml ohne Regel; Task 2.4 ohne RC. – Tasks ergänzen.
- [E5] minor – pytest oder unittest offen. – `python3 -m unittest discover tests`; Aufrufvertrag in 1.1.
- [E6] minor – RC-004 nicht automatisiert prüfbar. – Abnahme auf Textbaustein und SKILL-Verweis; End-to-End manuell.

Hinweis: Pilot-Specs tragen bei Must keine Priorität → eigener Change in pdf-concordance.

## Fachbereich – Zustimmung mit Auflagen
- [F1] major – Umpriorisierung nicht geregelt (RENAMED statt MODIFIED). – Szenario, Beispiel in process-model.md.
- [F2] major – Could vs. project-init Schritt 3 (nur Must/Should). – Entscheiden, festhalten, project-init angleichen.
- [F3] minor – Aufteilung gemischter Prioritäten unterbestimmt. – Unklare Zuordnung beim Maintainer erfragen, nicht raten.
- [F4] minor – «Should mit SHALL» wirkt widersprüchlich. – In 04 und process-model erklären; RFC 2119 kurz erklären.
- [F5] minor – NFR nicht erwähnt. – Konvention gilt auch für NFR.

## Testmanagement – Zustimmung mit Auflagen
Abdeckung: 6 von 8 Abnahmekriterien mit geplantem Test · Testlauf: nicht ausgeführt (vor Umsetzung) · `openspec validate --strict`: valid
- [T1] major – Selbstwiderspruch RC-001; «Schlüsselwort» undefiniert. – Erkennungsregel präzisieren, Fixture «zitiert/in Code», Akzeptanztest «Change besteht eigene Prüfung».
- [T2] major – Kein Test für RC-004. – Test auf Textbaustein; Szenario am Baustein prüfbar formulieren.
- [T3] minor – Keine Fixture für «Should validiert». – Validierbare Fixture oder Nachweis über RC-005 in der Test-Summary.
- [T4] minor – Fixtures mit Absicht-Verstössen könnten mitgescannt werden. – CI-Scan auf `openspec/specs/` und `openspec/changes/` begrenzen.

---

# Nachtrags-Review Revision 2 – Einzelvoten

Datum: 2026-11-05 · Fünf Rollen, gekürzt auf Befund und Auflage; Konsolidierung in `council-review.md`, Abschnitt «Nachtrags-Review».

## Security – Zustimmung mit Auflagen
- [S3] major – S1 («nur Standardbibliothek») ohne formellen Ersatz aufgehoben; OpenSpec nur «≥ 1.16», README installiert `@latest`, CI ohne Node/Installation → bei jedem PR ungeprüfter neuester Fremdcode inkl. npm-Install-Skripte. – Exakte Version fixieren (wenn möglich mit Integritätsprüfung), `actions/setup-node` mit fester Version, Installation als Task; S1 in design.md ausdrücklich ersetzen.
- [S4] minor – Workflow ohne Token-Rechte, obwohl jetzt Fremdcode im PR-Kontext läuft. – `permissions: contents: read`; **«Bei `pull_request` bleiben, nie `pull_request_target` verwenden»**; Telemetrie/Netzzugriffe von OpenSpec in der CI abschalten (z. B. `DO_NOT_TRACK=1`).
- [S5] minor – Namen aus der CLI entsprechen Ordnernamen aus dem PR; führendes «-» wäre Argument-Injection; Pfade aus JSON beim Lesen der Zeilennummer. – Namen gegen festes Muster prüfen, sonst Exit 2; `--` wo unterstützt; gelesene Dateien nach `resolve()` unter `<STAMM>/openspec/`; Fixture.
- [S6] minor – `OPENSPEC_BIN` erlaubt beliebiges Programm, Unterprozess ohne Grenzen. – Nur aus der Umgebung lesen und dokumentieren; Timeout; bei Zeitüberschreitung oder ungültigem JSON Exit 2.

## Architektur – Zustimmung mit Auflagen
- [A1] major – Aufrufschnittstelle inkompatibel (Pfade → Stamm); CI, CLAUDE.md, process-model DE/EN, Test-Report verwenden alte Form; kein Tasks-Abschnitt für Revision 2. – Abschnitt 10 anlegen, Aufrufer nachführen; Pfad ohne `openspec/` → klare Meldung.
- [A2] major – CI installiert weder Node noch OpenSpec. – Node einrichten, OpenSpec 1.16.0 fest installieren, getestete Version im Test-Report.
- [A3] minor – JSON wird Schnittstelle ohne Fehlerfall für veränderte Struktur. – Fehlende Felder → Exit 2 mit erwarteter Version; Vertragstest.
- [A4] minor – Zeilensuche «erste Kopfzeile» meldet RC-007-Duplikate auf der ersten statt der zweiten; RC-008 «ausschliesslich CLI» vs. Datei lesen. – n-tes Vorkommen → n-te Fundstelle; RC-008 präzisieren.

ADR nötig: nein (design.md ersetzt ADR); nachtragen, sobald `docs/adr/` existiert.

## Support / Betrieb – Zustimmung mit Auflagen
- [B1] major – CI nach Revision 2 nicht lauffähig (keine Node/OpenSpec; Aufruf mit Unterordnern → Exit 2). – Task für `actions/setup-node` (Node 20) und OpenSpec exakt fixiert (1.16.0); Aufruf umstellen; RC-006 real in der CI grün nachweisen.
- [B2] major – «≥ 1.16» ungeprüft; JSON ist kein versionierter Vertrag. – Version beim Start prüfen (< 1.16 → Exit 2 mit gefundener und benötigter Version); unerwartete Struktur → Exit 2, nie still bestehen; Szenario «OpenSpec zu alt».
- [B3] minor – Betriebsdoku veraltet (README ohne OpenSpec, process-model `[PFAD ...]`, kein `OPENSPEC_BIN`). – Voraussetzung, Aufruf, `OPENSPEC_BIN`, Exit-2-Ursachen mit Handlungsempfehlung dokumentieren.
- [B4] minor – Verhalten von CLI-abhängigen Tests ohne CLI offen. – Lokal sichtbar überspringen, in der CI (`CI=true`) Fehlschlag.

## Entwicklung – Zustimmung mit Auflagen · Aufwand M
- [E1] major – Revision 2 nicht in tasks.md; RC-008 ohne Task. – Abschnitt 10 mit einzeln prüfbaren Tasks.
- [E2] major – Aufruf inkompatibel; CI ohne Node/OpenSpec. – Aufrufe umstellen, CI-Schritt mit fester Version, als Task.
- [E3] minor – Fehlererkennung der CLI nicht festgelegt (JSON auf stdout, `status[]`). – Fehler bei Exitcode ≠ 0 oder `severity: error`, `message` weitergeben; Versionsprüfung über `openspec --version`.
- [E4] minor – Zuordnung JSON → Datei nicht beschrieben. – Pfadableitung und Felder (`requirements[]`, `rename.to`) im Design benennen.

## Testmanagement – Zustimmung mit Auflagen
Abdeckung vor Umsetzung: 18 von 22 Abnahmekriterien automatisch testbar, 4 manuell/Inspektion/indirekt · Testlauf: nicht ausgeführt (vor Umsetzung)
- [T1] major – Aufrufer und Tests verwenden alte Schnittstelle. – CI, CLAUDE.md, Tests umstellen; Test «`openspec/specs` → Exit 2».
- [T2] major – Keine Migrationsregel für Testdaten; Changes ohne `proposal.md` lösen ungewollt Exit 2 aus; keine Zuordnung alt → neu. – Fixtures als Projekte mit `proposal.md` (genau eines ohne); Zuordnung in der Test-Summary.
- [T3] major – «Tests setzen die CLI voraus» offen; stilles Überspringen möglich; kein Weg, CLI abwesend zu machen; Version ohne Szenario. – In der CI kein Überspringen; `OPENSPEC_BIN` auf nicht vorhandenen Pfad; Attrappe für «zu alt» und Fehler; Versionsprüfung als Szenario.
- [T4] minor – Zeilennummer heuristisch, ohne eigenes Szenario. – Tests für korrekte Zeile, Codeblock, verschachtelte Capability, Fallback Zeile 0.
