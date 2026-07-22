# SAN Work Method

- Protocol ID: `san.work`
- Version: `0.3.0`
- Authority: kernel normative rule
- Co-design: Expert and Gideon, 2026-07-21

## Purpose

Move one bounded network change from an exact GitHub issue and base commit to independently verified evidence without blurring ownership, authority, or maturity.

GitHub is canonical for work state and code. Discord and any task UI are projections. Private GBrains, credentials, prompts, owner authority, and confidential source material remain local.

## Required work object

Every consequential shared change must validate against `schemas/work-object.schema.json` before writing begins. It binds:

- one GitHub work ID, repository, branch, exact base SHA, and current subject SHA;
- one observable objective and explicit include/exclude paths;
- audience, handling constraints, and rights basis before disclosure;
- one writer lease with principal, paths, generation, expiry, and state;
- coordinator, executor, reviewer, verifier, and merger roles;
- a content-addressed golden fixture and execution environment when comparison or interoperability is claimed;
- focused, full, secret, rights, and rollback checks;
- exact rollback target and procedure;
- maturity, content-addressed evidence, and finding dispositions.

## Role and lease rules

1. Executor, reviewer, and verifier must be pairwise distinct.
2. The merger must not be the executor under the identity registry.
3. Exactly one active writer lease owns every changed path, including lockfiles, generated files, schemas, migrations, and shared indexes.
4. Reassignment increments the lease generation and records release, expiry, or reassignment evidence.
5. An expired, conflicting, or stale-generation lease fails closed.
6. A reviewer or verifier may return `abstain` when access or expertise is insufficient; abstention never satisfies a gate.

## Execution order

1. **Specify:** freeze work object, scope, roles, exact base, checks, rollback, and fixture/environment when required.
2. **Pre-disclosure scan:** apply privacy, secret, and rights checks before any text or artifact reaches a public issue, PR, CodeRabbit, Discord, Multica, logs, or fixtures.
3. **Execute:** one writer changes only leased paths.
4. **Validate:** run focused checks, full deterministic validation, secret scan, rights scan, and rollback test. Classify flaky behavior; a rerun cannot silently erase a failure.
5. **Push:** publish the subject commit and update `subject_sha`.
6. **Automated review:** CodeRabbit reviews the current full SHA.
7. **Independent review:** a different agent reviews the same full SHA.
8. **Destination verification:** a third agent runs the pinned fixture in the pinned destination environment when the claim requires it.
9. **Remediate once:** batch only dispositioned findings. Unrelated work starts a new work object. Any edit invalidates earlier current-head review, verifier, and GO evidence.
10. **Re-review:** repeat current-head automated and independent gates after remediation.
11. **Merge:** only when required checks are green, every finding has a disposition, rollback is explicit, current-head review is GO, and destination evidence exists when required. No self-merge.
12. **Close:** issue a terminal receipt and release the writer lease.

## Evidence and maturity

Mutable comments are pointers, not immutable evidence. Every evidence item binds the current subject SHA, URI, digest, actor, timestamp, environment digest, and verdict.

Maturity is monotonic except through explicit demotion or rollback:

`specified -> built -> tested -> independently-reviewed -> destination-verified -> adopted -> monitored`

Required minimum evidence:

- `built`: build evidence;
- `tested`: test evidence plus fixture and environment digests;
- `independently-reviewed`: current-head CodeRabbit and independent-review evidence;
- `destination-verified`: destination verification evidence;
- `adopted`: destination verification plus adopter evidence;
- `monitored`: adopted state plus monitoring evidence.

A manifest, fixture, comment, or passing local test cannot skip a maturity stage.

## Failure handling

- CodeRabbit unavailable or stale: fail closed or use a documented alternate automated check; never silently skip.
- Reviewer/verifier unavailable: reassign through a new lease/role event or keep the work waiting.
- Force-push, rebase, generated-byte change, or remediation: clear all current-head review and GO evidence.
- Schema/data migration rollback failure: declare irreversibility before execution and pin a forward-recovery plan.
- GitHub/projection conflict: GitHub wins; reconcile reopen, close, delete, and duplicate events explicitly.
- Finding dispositions are only `fixed`, `accepted-risk`, `false-positive`, or `deferred-with-owner-and-gate`.

## Multica boundary

Multica is not part of the authority path. A future pilot may project public GitHub work objects one-way for visibility only. It may not receive private data, credentials, prompts, skills, runtime bindings, agent execution authority, repository write credentials, status authority, squads, or autopilots. Failure to preserve that boundary rejects Multica for SAN.
