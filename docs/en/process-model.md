---
source: docs/de/process-model.md
source-hash: d0bbf701922e
status: translated
---

# The process model

The same phases, building blocks and templates for every project.

## 1. Phases

| Phase | Goal | Artefact | Gate |
|---|---|---|---|
| Idea & value | Why? For whom? | 01 Project brief | – |
| Market analysis | What exists, where is the gap? | 02 Market analysis | – |
| Business model | How is value created? Open-core split | 03 Open-core model | – |
| Requirements | What must it do? | 04 Requirements → OpenSpec specs | **Phase gate 1** (council + maintainer) |
| Architecture & design | How do we build it? | 07 ADRs | **Phase gate 2** |
| Implementation | Build iteratively | OpenSpec changes | Quality gate per change |
| Quality assurance | Does it work, is it safe? | 08 Test strategy, test reports | Quality gate per release |
| Operations & evolution | Does it keep running? | 09 Operations, 10 Roadmap | – |

The first four phases are completed once, properly. From implementation onwards the project works in changes: every modification is an OpenSpec change with a council review and a quality gate.

## 2. Cross-cutting building blocks

Active in every phase rather than being a phase themselves:

- **Roles and permissions** (05) – roles in the product and in the project
- **Audit and traceability** (06) – what is logged and who may see it
- **Testing** (08) – strategy per level, acceptance criteria from the requirements phase on
- **Open source + added value** (03) – licence, split, contribution rules
- **Documentation** – Markdown as the single source
- **Security and privacy** – threat model, Swiss FADP / GDPR
- **Feedback and defect handling** (11) – intake, classification, feedback loop

## 3. The council

Six roles review every specification and every change independently:

| Role | Perspective | Special rule |
|---|---|---|
| Security | Permissions, privacy, attack surface | Veto right |
| Architecture | Layers, interfaces, ADRs | – |
| Support/operations | Error messages, diagnostics, updates | – |
| Development | Feasibility, effort, testability | – |
| Business | Value, clarity | Extensible with domain roles |
| Test management | Coverage, regression, reporting | Red = no archiving |

The roles are implemented as subagents (`agents/`). They do not see each other's votes. Contradictions are named in the record, not smoothed over.

## 4. The change cycle

```
Report ─▶ change-proposal ─▶ council-review ─▶ implement ─▶ quality-gate ─▶ archive
   ▲                                                                         │
   └────────── feedback: tests · docs · role model · roadmap ◀───────────────┘
```

**Limits before implementation.** If a change's result is an automatic check, detection or decision, `design.md` names in a section "Grenzen" (limits), before the council review, what is deliberately not covered and what it is checked against. Promises such as "never" or "in every case" appear only with a reference standard and limits.

**Quality gate standard.** Gate item G7 checks that the specification is updated and matches the behaviour. It fails on a broken explicit promise or on a violation that passes silently and is *realistic* (can arise in normal work). *Constructed* cases (deliberate obfuscation) and cases within valid limits are observations; when in doubt, "realistic" applies. For requirements with a security purpose, constructed cases count too, unless Security agreed to the limit.

**Gate log and escalation.** Every gate run is recorded in `gate-log.md` in the change, as is every maintainer decision (reclassifying, deferring to a follow-up change, confirming a limit). If the gate fails three times in a row on the same item – for G3 and G7 on the same requirement –, the maintainer is asked about the standard before the next run. Background: in the dry run on the plugin, the gate needed 19 runs without a fixed standard (`docs/de/pilot-blattwerk.md`, T1–T8).

## 5. Requirements in OpenSpec

OpenSpec requires the keyword SHALL or MUST in every requirement. These keywords come from RFC 2119, a standard for levels of obligation in specifications (SHALL = mandatory, SHOULD = recommended, MAY = optional). Requirements specifications, however, prioritise with MoSCoW. To reconcile both, the following applies to functional and non-functional requirements:

| Rule | Content |
|---|---|
| RC-001 | The requirement text always uses SHALL. This is only the syntax OpenSpec requires – the obligation is defined solely by the priority in the title. |
| RC-002 | Title in the form `<Title> (<ID>, <Must\|Should\|Could>)`, e.g. `Display modes (LA-F-110, Should)`. The ID is the stable identifier from the requirements source. Won't items go to the roadmap, not to OpenSpec. |
| RC-003 | A source requirement with mixed priority ("Must / Should") is split into one requirement per priority with the same ID. If the split is unclear, the maintainer decides. |
| RC-004 | A change of priority is a rename: RENAMED with FROM/TO, not MODIFIED. |
| RC-007 | Within one spec file, each combination of ID and priority appears only once. |

**Example of a priority change** (Should becomes Must):

```markdown
## RENAMED Requirements

- FROM: `### Requirement: Display modes (LA-F-110, Should)`
- TO: `### Requirement: Display modes (LA-F-110, Must)`
```

**Check:** `python3 scripts/check-conventions.py [ROOT ...]` in the project root (folder containing `openspec/`) reports violations with file, line of the requirement, rule and title. It reads the structure through the OpenSpec CLI (1.16 or later) so that it sees exactly the requirements OpenSpec sees; the CLI is found via `OPENSPEC_BIN` or `openspec` on the `PATH`. Exit codes: 0 = ok, 1 = violations, 2 = usage or input error.

| Message (exit 2) | Remedy |
|---|---|
| OpenSpec CLI not found / too old | `npm install -g @fission-ai/openspec@1.16.0` or set `OPENSPEC_BIN` |
| contains no openspec/ | run in the project root, not in `openspec/specs` |
| OpenSpec reports for «…» | fix the OpenSpec message, e.g. missing `proposal.md`; `openspec validate --all --strict` shows details |
| Unexpected structure from OpenSpec | check the OpenSpec version; 1.16.0 is tested |

**Migrating existing projects:** First add the rules to `openspec/config.yaml` using `project-init` (step "Initialise OpenSpec"). Then run the check with `--warn` – it reports all violations without failing. Rename the titles of existing requirements in a separate change via RENAMED; afterwards run the check without `--warn`.

## 6. Principles

1. **The specification is the truth.** Code that does not match the spec is a defect – or the spec is changed through a change.
2. **No self-approval.** Whoever implements does not review.
3. **Hard gates.** Red stays red.
4. **Humans decide at the gates.** The AI prepares, the maintainer approves.
5. **Every report gets an answer.**

## 7. How it relates to OpenSpec, Spec Kit and BMAD

| | OpenSpec | Spec Kit | BMAD | spec-concordance |
|---|---|---|---|---|
| Living specs, change cycle | ✅ | – | – | ✅ (via OpenSpec) |
| Early phases (market, business model) | – | – | ✅ | ✅ |
| Role-based reviews | – | – | ✅ (agents build) | ✅ (agents review) |
| Hard quality gates | – | partly | – | ✅ |
| Feedback loop | – | – | – | ✅ |
