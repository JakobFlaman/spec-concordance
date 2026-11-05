---
source: docs/de/process-model.md
source-hash: 9e6f9f075e5e
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

**Check:** `python3 scripts/check-conventions.py [PATH ...]` reports violations with file, line, rule and title. Exit codes: 0 = ok, 1 = violations, 2 = usage or input error.

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
