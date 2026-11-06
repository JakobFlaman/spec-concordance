# Tasks: Installation direkt aus GitHub

## 1. Marktplatz

- [ ] 1.1 `.claude-plugin/marketplace.json` anlegen (DI-001)
- [ ] 1.2 Test `tests/test_distribution.py`: Pflichtfelder, gleicher Name, Quelle `./`, keine Version im Eintrag; Gegenprobe mit abweichendem Namen (DI-001, DI-004)
- [ ] 1.3 CI-Schritt «Marktplatz prüfen» in `.github/workflows/checks.yml` (DI-004)
- [ ] 1.4 `claude plugin validate .` lokal ausführen, Ergebnis festhalten (DI-001)

## 2. Dokumentation

- [ ] 2.1 README.md: Schnellstart mit Einschritt-Befehl, Zwei-Schritt-Variante, Zugriff auf das private Repository, neues Projekt mit `project-init` (DI-002, DI-003)
- [ ] 2.2 README.en.md aus der deutschen Fassung nachführen (DI-002, DI-003)
- [ ] 2.3 Test: README de/en enthalten die Befehle, keinen `<owner>`-Platzhalter, kein `git clone` und kein Kopieren von `template-project` (DI-002, DI-003)
- [ ] 2.4 `skills/project-init/SKILL.md`: Pfade ausdrücklich auf das Plugin-Verzeichnis beziehen (DI-003)

## 3. Abschluss

- [ ] 3.1 Manueller Installationstest aus GitHub in sauberer Umgebung (DI-002)
- [ ] 3.2 CHANGELOG unter [Unreleased]
- [ ] 3.3 Test-Summary `docs/test-reports/<datum>-add-github-marketplace.md`
