---
description: Run the six-role council review on an OpenSpec change
argument-hint: <change-id>
---
Run a council review of the OpenSpec change `$ARGUMENTS`.

Invoke each of these agents on the change: council-product, council-architect, council-security, council-qa, council-ops, council-maintainer.

Then summarize all verdicts in a table. The council result is BLOCKED if any role returned BLOCK, otherwise PASSED.
