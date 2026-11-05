# spec-concordance:requirement-conventions
Requirement conventions (spec-concordance, see docs/de/process-model.md «Anforderungen in OpenSpec»):
- RC-001: Every requirement text uses SHALL only, regardless of priority. Do not use the RFC 2119 keywords for recommendation or option in requirement text.
- RC-002: Every requirement title has the form "<Title> (<ID>, <Must|Should|Could>)", e.g. "Darstellungsmodi (LA-F-110, Should)". The ID is the stable identifier from the project's requirements source (functional and non-functional). Won't items go to the roadmap, not to OpenSpec.
- RC-003: A source requirement with mixed priority ("Must / Should") is split into one requirement per priority with the same ID. If the split is not clear from the source, ask the maintainer instead of guessing.
- RC-004: A priority change is a RENAMED delta (FROM/TO), not MODIFIED.
- RC-007: Within one spec file, each combination of ID and priority appears only once.
Check: run python3 <spec-concordance>/scripts/check-conventions.py in the project root; needs OpenSpec CLI >= 1.16 (exit 0 = ok, 1 = violations, 2 = usage error; --warn for transition).
