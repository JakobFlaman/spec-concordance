# Tasks: Installation direkt aus GitHub

## 1. Marktplatz

- [x] 1.1 `.claude-plugin/marketplace.json` anlegen: `name`, `description`, `owner.name`, ein Eintrag mit `name`, `source` `./`, `description` (DI-001; D7, D12)
- [x] 1.2 Prüffunktion und Test `tests/test_distribution.py`: Pflichtfelder (`name`, `owner.name`, `plugins[].name`, `plugins[].source`), genau ein Eintrag, Name gleich, Quelle `./`, keine `version`, keine E-Mail im `owner`; Gegenprobe mit Fixture `tests/fixtures/marketplace/name-mismatch.json` (DI-001, DI-004; D13)
- [x] 1.3 CI: `pull_request` als Auslöser bestätigen; Prüfung läuft über den bestehenden Testlauf (DI-004, DI-006; D13)
- [x] 1.4 `claude plugin validate .` ausführen, Ausgabe mit Version festhalten (DI-001; D11)

## 2. Dokumentation

- [x] 2.1 README.md: Marktplatz erklären; Einschritt-Befehl, Zwei-Schritt-Variante, Bestätigung; Zugriff (öffentlich / privat mit minimalen Rechten, SSH/HTTPS); Aktualisieren über Releases; Umstieg von der Klon-Installation; Voraussetzungen; neues Projekt mit `project-init`; Zugriff beim Maintainer anfragen (DI-002, DI-003, DI-005; D2, D6, D8, D9, D10)
- [x] 2.2 README.en.md aus der deutschen Fassung nachführen (DI-002, DI-003, DI-005)
- [x] 2.3 Test: README de/en enthalten die Befehle und die Update-Anleitung, keinen `<owner>`; der Abschnitt Schnellstart enthält weder `git clone` noch `cp … template-project`; Gegenprobe gegen das bisherige README (DI-002, DI-003, DI-005; D14)
- [x] 2.4 `skills/project-init/SKILL.md`: alle Plugin-Pfade mit `${CLAUDE_PLUGIN_ROOT}/`; Test (DI-003; D1)
- [x] 2.5 ADR `docs/adr/0001-plugin-repository-als-marktplatz.md` (D4)
- [x] 2.6 CLAUDE.md: PR-Pflicht, G11 = Mergen, Einstellungen für den Branch-Schutz; Test (DI-006; D3)

## 3. Abschluss

- [x] 3.1 CHANGELOG unter [Unreleased]
- [x] 3.2 Test-Summary `docs/test-reports/2026-11-06-add-github-marketplace.md` mit CI-Run-ID und Ausgabe von `claude plugin validate .` (D11)
- [x] 3.3 Folge-Change notieren: `source-hash` für README.en.md bzw. READMEs in `check-i18n.py` (D16)

## 4. Manueller Nachweis (im Qualitäts-Gate, nach dem Push des Branches)

- [x] 4.1 Installationstest nach Protokoll: Claude-Code-Version und Commit-SHA notieren; Art des Git-Zugangs; zwei saubere Umgebungen (je eigenes `HOME`); Einschritt-Befehl bzw. Zwei-Schritt-Variante mit `#<branch>` des Pull Requests; Ausgabe `claude plugin list`; im Installationsverzeichnis `templates/de/`, `template-project/`, `scripts/check-conventions.py` vorhanden; Prüfskript aus dem Installationsverzeichnis auf ein Testprojekt angewendet (DI-002, DI-003; D5)
- [ ] 4.2 Branch-Schutz abfragen, sobald eingerichtet (DI-006)

## 5. Nach Qualitäts-Gate (Lauf 1 nicht bestanden)

- [x] 5.1 G6: Status D1–D16 in `council-review.md` nachgeführt
- [x] 5.2 G7 / DI-005: Update-Anleitung um `/plugin update spec-concordance@spec-concordance` und Neustart ergänzt (Katalog-Update allein hebt die Version nicht); Spec, Design, README de/en, Test
- [x] 5.3 Beobachtungen: Versionsangabe in den Voraussetzungen widerspruchsfrei; `check-marketplace.py` verlangt genau `./`; Nachweis `${CLAUDE_PLUGIN_ROOT}` aus dem Gate in die Test-Summary; CI-Läufe nachgeführt

