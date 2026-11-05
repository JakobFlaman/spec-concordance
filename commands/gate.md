---
description: Check hard quality gates for an OpenSpec change
argument-hint: <change-id>
---
Evaluate the hard quality gates for the OpenSpec change `$ARGUMENTS`. All gates must pass; any failure stops the process.

1. Proposal, specs, design and tasks exist and `openspec validate $ARGUMENTS` succeeds.
2. Every requirement has at least one scenario.
3. Council review result is PASSED (no BLOCK verdicts, no open blocker findings).
4. Every task maps to a requirement, and every requirement has a task.
5. Tests exist for all scenarios and pass (checked before archiving).

Report each gate as PASS or FAIL with evidence.
