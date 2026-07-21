# Contributing

The authoritative network workflow is [`kernel/protocols/work-method.md`](kernel/protocols/work-method.md), validated by `kernel/schemas/work-object.schema.json`. This file is a contributor-facing summary only; if it conflicts with the kernel, the kernel fails the change.

## One work object, one writer

Every consequential shared change starts from one GitHub issue and a schema-valid SAN work object. It names the exact base and subject commits, scope, rights basis, writer lease, coordinator, executor, independent reviewer, verifier, merger, checks, evidence, findings, and rollback.

Only one active writer lease owns each changed path. Other agents review, test, or provide bounded input without editing that writer's branch.

## Pull requests

A pull request must state:

- canonical issue;
- executor, reviewer, verifier, merger, and writer lease;
- confidentiality and rights basis;
- validation commands and exact results;
- CodeRabbit and independent-review evidence bound to the current full SHA;
- finding dispositions;
- rollback or rejection path;
- evidence maturity and explicit non-claims.

## Data boundaries

Do not commit secrets, credentials, private memory, raw personal context, confidential source material, or third-party bodies lacking a network distribution basis. Corpus doctrine must bind to a versioned release and provenance set.

## Completion

Close with one terminal receipt and release the writer lease. Do not count a merge as installation, destination adoption, task proof, monitoring, or outcome improvement without separate evidence.
