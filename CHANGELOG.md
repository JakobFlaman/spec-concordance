# Changelog

Format nach [Keep a Changelog](https://keepachangelog.com/de/1.1.0/), Versionierung nach [Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

### Hinzugefügt
- Anforderungskonvention RC-001 bis RC-007 (Change `add-priority-convention`): immer SHALL, MoSCoW-Priorität und ID im Titel, gemischte Prioritäten getrennt, Umpriorisierung als RENAMED; gilt für funktionale und nicht-funktionale Anforderungen
- Prüfskript `scripts/check-conventions.py` (Exitcodes 0/1/2, Übergangsmodus `--warn`) mit 32 Tests; Ausführung in der CI
- Textbaustein `template-project/openspec-context.md`; `project-init` trägt ihn idempotent in `openspec/config.yaml` ein und überführt jetzt Must, Should und Could
- Vorgehensmodell DE/EN: Abschnitt «Anforderungen in OpenSpec» inkl. Migration bestehender Projekte
- Testbefehl in CLAUDE.md; OpenSpec im Plugin-Repository eingerichtet (Dogfooding)

### Geändert
- Befunde tragen einen Schweregrad (`blocker` / `major` / `minor`); ein offener `blocker` verhindert die Freigabe
- Qualitäts-Gate: neuer Punkt G0 (`openspec validate`) und G1a (Rückverfolgbarkeit Task ↔ Anforderung ↔ Szenario); G6 verlangt nur noch `blocker`/`major` erledigt
- Rolle Entwicklung: Prüffragen zu Wartbarkeit und Rückverfolgbarkeit ergänzt
- Ideen übernommen aus dem Copilot-Entwurf (Branch `copilot/process-model-ai-spec-driven-dev`)
- Datei-, Ordner- und Rollennamen auf Englisch umgestellt (z. B. `council-business`, `01-project-brief.md`, `docs/artifacts/`); Inhalte bleiben deutsch. Regel in CLAUDE.md festgehalten

## [0.1.0] – 2026-11-05

### Hinzugefügt
- Grundgerüst als Claude-Code-Plugin auf Basis von OpenSpec
- Vorgehensmodell: acht Phasen, sieben Querschnittsbausteine, elf Artefakte
- Council mit sechs Rollen (Security, Architektur, Support/Betrieb, Entwicklung, Fachbereich, Testmanagement)
- Skills: `project-init`, `change-proposal`, `council-review`, `quality-gate`
- Vorlagen für die elf Projekt-Artefakte (Deutsch)
- Startvorlage `template-project` mit CLAUDE.md
- Issue-Formulare (Fehler, Wunsch), PR-Vorlage, CI-Prüfung für Markdown und Übersetzungen
- README auf Deutsch und Englisch
