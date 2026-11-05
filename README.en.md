# spec-concordance

> 🇩🇪 [Deutsche Version](README.md) (source language)

**A process model for AI-driven, specification-first development – with role-based reviews and hard quality gates.**

The name refers to the Swiss principle of *concordance*: every relevant perspective has a seat at the table before a decision is made.

`spec-concordance` builds on [OpenSpec](https://github.com/Fission-AI/OpenSpec) and adds what existing spec-driven development tools lack:

| Building block | What it does |
|---|---|
| **Phase model** | The same phases for every project: idea & value → market analysis → business model → requirements → architecture → implementation → QA → operations |
| **Council** | Six roles (security, architecture, support/operations, development, business, test management) review every specification and every change and cast a reasoned vote |
| **Quality gates** | No change is archived without passing tests, a council vote and an updated specification |
| **Templates** | Eleven project artefacts, from the project brief to the feedback and defect process |
| **Feedback loop** | Defects → regression tests, recurring questions → docs, requests → roadmap |

## Why

AI agents produce plausible code fast. Without a specification it drifts away from intent; without gates, quality erodes unnoticed. `spec-concordance` makes the specification the living source of truth and never lets the AI sign off its own work.

## Layout

```
.claude-plugin/       Plugin manifest for Claude Code
agents/               Council roles (one file per role)
skills/               Workflows: project init, council review, change, quality gate
templates/de/         Templates for the eleven artefacts (German = source)
templates/en/         English translations (derived from the German source)
template-project/     Starter for a new project
docs/de/              Process model in detail (German)
docs/en/              English documentation
scripts/              Helper scripts (e.g. stale-translation check)
```

## Quick start

Requirements: [Claude Code](https://docs.claude.com/en/docs/claude-code/overview), Node.js 20+, Git, Python 3.10+ (for the check scripts).

```bash
# 1. Install OpenSpec
npm install -g @fission-ai/openspec@latest

# 2. Add the plugin to Claude Code (local clone)
git clone https://github.com/<owner>/spec-concordance.git
# in Claude Code: /plugin → add local plugin from ./spec-concordance

# 3. Start a new project from the starter
cp -r spec-concordance/template-project my-project
cd my-project && git init && openspec init
```

Then in Claude Code:

| Command | Purpose |
|---|---|
| `/spec-concordance:project-init` | Guided pass from "idea & value" to "requirements", creating the artefacts |
| `/spec-concordance:change-proposal` | Turn a report, request or defect into an OpenSpec change |
| `/spec-concordance:council-review` | Review a specification or change from all six roles |
| `/spec-concordance:quality-gate` | Check whether a change may be archived |

## Status

Early stage (0.1). See [CHANGELOG](CHANGELOG.md).

## Languages

German is the source language; English is derived from it. `scripts/check-i18n.py` reports stale translations.

## License

[MIT](LICENSE) © 2026 Jakob Flaman

Builds on OpenSpec (MIT) and is inspired by GitHub Spec Kit (MIT) and BMAD-METHOD (MIT). "BMAD" is a trademark of BMad Code, LLC; this project is not affiliated with it.
