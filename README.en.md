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
.claude-plugin/       Plugin manifest and marketplace file for Claude Code
agents/               Council roles (one file per role)
skills/               Workflows: project init, council review, change, quality gate
templates/de/         Templates for the eleven artefacts (German = source)
templates/en/         English translations (derived from the German source)
template-project/     Starter for a new project
docs/de/              Process model in detail (German)
docs/adr/             Architecture decisions (German)
docs/en/              English documentation
scripts/              Helper scripts (e.g. stale-translation check)
```

## Quick start

Requirements: [Claude Code](https://code.claude.com/docs) (one-step installation from version 2.1.275), Node.js 20+, Git, Python 3.10+ (for the check scripts) and the OpenSpec CLI 1.16 or later.

### 1. Install OpenSpec

```bash
npm install -g @fission-ai/openspec@1.16.0
```

### 2. Install the plugin straight from GitHub

This repository is also a *marketplace* – a plugin catalogue Claude Code installs plugins from. No clone needed. In Claude Code, enter:

```
/plugin install spec-concordance --marketplace JakobFlaman/spec-concordance
```

Claude Code asks for confirmation and shows the plugin's details; confirm the installation there.

Older Claude Code versions (before 2.1.275) need two steps:

```
/plugin marketplace add JakobFlaman/spec-concordance
/plugin install spec-concordance@spec-concordance
```

In a terminal instead of Claude Code: `claude plugin marketplace add JakobFlaman/spec-concordance`, then `claude plugin install spec-concordance@spec-concordance`.

**Access.** As long as the repository is public, nothing else is needed. If it is private, Claude Code uses this machine's git credentials and does not prompt:

- **SSH** (tried first): a key that works without a passphrase prompt, e.g. loaded in `ssh-agent`.
- **HTTPS:** a credential stored in the credential helper. With minimal rights via a fine-grained GitHub token that can only read this repository. `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` skips the SSH attempt.

Never put tokens in a URL or a project file. No read access: ask the maintainer for access.

### 3. Start a new project

```bash
mkdir my-project && cd my-project && git init
```

Then run `/spec-concordance:project-init` in Claude Code. The skill takes the templates and the starter from the installed plugin, sets up OpenSpec and runs the convention check itself.

To run the check scripts by hand, use the plugin's install directory; `claude plugin list --json` shows it as `installPath`, e.g. `python3 <installPath>/scripts/check-conventions.py` in the project root.

### Update

New versions arrive only with a release, i.e. a higher version in `plugin.json` (see [CHANGELOG](CHANGELOG.md)). Update in two steps – first reload the catalogue, then the plugin:

```
/plugin marketplace update spec-concordance
/plugin update spec-concordance@spec-concordance
```

In a terminal: `claude plugin marketplace update spec-concordance`, then `claude plugin update spec-concordance@spec-concordance`. The update takes effect after restarting Claude Code.

Automatically: in `/plugin`, under *Marketplaces*, select `spec-concordance` and turn on *Enable auto-update*.

### Moving from the clone installation

If you added the plugin from a local clone so far, remove that local plugin in `/plugin` and install from GitHub as above. The clone is only needed to contribute to the plugin.

### Commands

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
