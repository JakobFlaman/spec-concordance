# Council-Review: add-github-marketplace
Datum: 2026-11-06 · Ergebnis: **freigegeben mit Auflagen**

Einzelvoten: `council-review-votes.md` (gemeinsamer Lauf mit `define-gate-standard`).

## Voten

| Rolle | Votum | Befunde |
|---|---|---|
| Security | Zustimmung mit Auflagen | S1 major, S2–S3 minor |
| Architektur | Zustimmung mit Auflagen | A1–A2 major, A3–A4 minor; ADR nötig |
| Support/Betrieb | Zustimmung mit Auflagen | O1–O2 major, O3–O5 minor |
| Entwicklung | Zustimmung mit Auflagen | E1 major, E2–E5 minor |
| Fachbereich | Zustimmung mit Auflagen | F1 major, F2–F4 minor |
| Testmanagement | Zustimmung mit Auflagen | T1–T2 major, T3–T5 minor |

## Widersprüche

Keine zwischen den Rollen. Gemeinsam gefunden: Pfad zum Plugin ohne Klon (A1, E1, O2, T1) und fehlender Update-Weg (O1, F1, A3).

## Entscheide des Maintainers (2026-11-06)

- **Updates nur über Releases:** `version` bleibt in `plugin.json`; Nutzer erhalten Neues erst bei einem Versionssprung. Nach diesem und dem Change `define-gate-standard` folgt Release 0.2.0 als eigener Schritt.
- **main mit PR-Pflicht und grüner CI:** Änderungen nur über Pull Requests; die Freigabe G11 ist das Mergen. Den Branch-Schutz richtet der Maintainer in GitHub ein.
- Hinweis bei der Prüfung: Das Repository ist zurzeit öffentlich (nicht privat, wie die Changes annahmen). Die Doku beschreibt den Zugriff für beide Fälle.

## Entscheidungsliste

| Nr. | Auflage | Schweregrad | Rolle(n) | Status |
|---|---|---|---|---|
| D1 | Plugin-Pfad über `${CLAUDE_PLUGIN_ROOT}` (in Plugin-Skills von Claude Code ersetzt); jede Plugin-Pfadangabe in `project-init` trägt die Variable; Szenario und Texttest | major | A1, E1, O2, T1 | offen |
| D2 | Update-Weg im README (Befehle, «Neues nur mit Release», automatische Aktualisierung); Proposal-Satz korrigiert; Grenze «0.1.0 bezeichnet bis zum Release keinen eindeutigen Stand» | major | O1, F1, A3 | offen |
| D3 | main als Verteilkanal: PR-Pflicht mit grüner CI (Entscheid Maintainer); CI auf Pull Requests; Arbeitsweise in CLAUDE.md; Einstellungen für den Branch-Schutz beschrieben | major | S1 | offen |
| D4 | ADR «Plugin-Repository als eigener Marktplatz» unter `docs/adr/` | major | A2 | offen |
| D5 | Protokoll für den manuellen Installationstest im Voraus festgelegt (Claude-Code-Version, Commit, Zugang, beide Befehlsvarianten, `claude plugin list`, Dateien im Cache, Prüfskript aus dem Cache); Ergebnis in der Test-Summary | major | T2, O2 | offen |
| D6 | README: Zugriff mit minimalen Rechten (SSH-Schlüssel oder feingranularer Lese-Token), SSH/HTTPS-Verhalten, `CLAUDE_CODE_PLUGIN_PREFER_HTTPS`, nie Tokens in URLs oder Projektdateien | minor | S2, O3 | offen |
| D7 | `owner` nur mit Namen, keine E-Mail-Adresse | minor | S3 | offen |
| D8 | README: Voraussetzungen behalten; Prüfskript ohne Klon über den Skill bzw. Pfad im Plugin-Cache | minor | F2 | offen |
| D9 | README: Umstieg von der Klon-Installation | minor | F3, O4 | offen |
| D10 | README: «Marktplatz» erklären; Zugriff beim Maintainer anfragen; Bestätigungsschritte beim Installieren | minor | F4, O5 | offen |
| D11 | Manuelle Szenarien als «> Manueller Test» kennzeichnen; Nachweis CI-Run-ID und `claude plugin validate .` mit Version | minor | E2, T5 | offen |
| D12 | Marktplatz-Beschreibung; Warnung zu `CLAUDE.md` im Stamm als Grenze | minor | E3 | offen |
| D13 | Pflichtfelder im Test benennen, genau ein Eintrag; Gegenprobe mit Fixture unter `tests/fixtures/`; CI-Prüfung über den bestehenden Testlauf | minor | E4, T3 | offen |
| D14 | README-Test auf den Schnellstart beschränken, Muster festlegen, Gegenprobe gegen das alte README | minor | T4 | offen |
| D15 | Plugin- und Marktplatzname sind stabile Kennungen; Änderungen nur über `renames` | minor | A4 | offen |
| D16 | `source-hash`-Kopf für README.en.md bzw. Prüfung der READMEs durch `check-i18n.py` | minor | E5 | Folge-Change |
