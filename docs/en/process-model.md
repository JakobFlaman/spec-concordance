---
source: docs/de/vorgehensmodell.md
source-hash: 50eba6f9fda1
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

## 5. Principles

1. **The specification is the truth.** Code that does not match the spec is a defect – or the spec is changed through a change.
2. **No self-approval.** Whoever implements does not review.
3. **Hard gates.** Red stays red.
4. **Humans decide at the gates.** The AI prepares, the maintainer approves.
5. **Every report gets an answer.**

## 6. How it relates to OpenSpec, Spec Kit and BMAD

| | OpenSpec | Spec Kit | BMAD | spec-concordance |
|---|---|---|---|---|
| Living specs, change cycle | ✅ | – | – | ✅ (via OpenSpec) |
| Early phases (market, business model) | – | – | ✅ | ✅ |
| Role-based reviews | – | – | ✅ (agents build) | ✅ (agents review) |
| Hard quality gates | – | partly | – | ✅ |
| Feedback loop | – | – | – | ✅ |
