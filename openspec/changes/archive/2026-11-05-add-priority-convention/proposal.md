# Proposal: Prioritätskonvention MoSCoW in OpenSpec-Anforderungen

## Why

OpenSpec verlangt in jeder Anforderung das Schlüsselwort SHALL oder MUST (RFC 2119) und meldet bei SHOULD oder MAY eine Warnung; mit `--strict` schlägt die Validierung fehl. Projekte nach spec-concordance priorisieren Anforderungen aber nach MoSCoW (Must / Should / Could / Won't), siehe Vorlage `04-requirements.md`. Im Pilot Blattwerk musste die Konvention deshalb ad hoc erfunden werden (Erkenntnis P1 in `docs/de/pilot-blattwerk.md`). Ohne feste Regel formuliert jedes Projekt anders, und Gate G0 (`openspec validate`) scheitert an korrekt priorisierten Should-Anforderungen.

- **Klassifikation:** feature (Lücke – es gibt keine Anforderung dazu; das Plugin hat noch keine Basis-Spezifikation)
- **Quelle:** Pilot Blattwerk, Erkenntnis P1, Priorität hoch
- **Schweregrad:** entfällt (kein Bug)

## What Changes

Neue Fähigkeit `requirement-conventions` (ADDED):

- Jede Anforderung in einer OpenSpec-Spezifikation ist mit SHALL formuliert, unabhängig von ihrer Priorität.
- Die MoSCoW-Priorität steht im Titel der Anforderung, zusammen mit einer stabilen Anforderungs-ID: `### Requirement: <Titel> (<ID>, <Must|Should|Could>)`.
- Eine Quellanforderung mit gemischter Priorität («Must / Should») wird in zwei Anforderungen getrennt.
- `project-init` trägt die Regel beim Projektstart in `openspec/config.yaml` ein, damit OpenSpec-Agenten sie kennen.
- Eine Umpriorisierung erfolgt als RENAMED-Delta.
- Eine automatische Prüfung (`scripts/check-conventions.py`) meldet Verstösse; sie läuft in der CI des Plugins.

Nach dem Council-Review überarbeitet (Entscheidungsliste D1–D16 in `council-review.md`); Schnittstelle und Begründung in `design.md`.

## Out of Scope

- Won't-Anforderungen werden nicht als OpenSpec-Requirement geführt, sondern in der Roadmap (Artefakt 10) unter «Bewusst abgelehnt» bzw. «Später».
- Bereitstellung der Prüfung für die CI von Projekten – eigener Folge-Change (W1 im Council-Review).
- Nachführung der Titel im Pilotprojekt pdf-concordance – eigener Change dort.
- Keine Änderung an OpenSpec selbst.
- Übrige Pilot-Erkenntnisse P2–P10 – je eigener Change.

## Abweichungen von der Quelle

Keine. Die Regel entspricht der im Pilot verwendeten Lösung (`pdf-concordance/openspec/config.yaml`).

## Impact

- Skill `project-init` (Schritt 3, neuer Schritt für `config.yaml`)
- Vorlage `templates/de/04-requirements.md` (Hinweis zur Überführung)
- Vorgehensmodell `docs/de/process-model.md` und englische Fassung
- CI `.github/workflows/checks.yml` (neue Prüfung)
- Rückkopplung: Teststrategie des Plugins (bisher keine Testbefehle in CLAUDE.md – siehe Tasks)
