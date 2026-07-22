# Capability Adoption Protocol

- Protocol ID: `san.capability-adoption`
- Version: `0.1.0`
- Authority: kernel normative rule

The lifecycle is:

`discovered -> quarantined -> schema-validated -> provenance-verified -> policy-evaluated -> sandbox-tested -> locally-active -> task-proven -> monitored`

Each destination may reject at any stage. The destination agent remains authoritative over local activation. Network popularity, CodeRabbit review, and source-agent success are evidence, not local authority.

Activation must be atomic, preserve the prior exact pin, and emit a machine-valid adoption receipt. The receipt binds the previous and candidate exact pins, benchmark ID and exact version, threshold fixed before execution, observed result, destination evidence, resulting baseline, and exact rollback target. It identifies pairwise-distinct executor, reviewer, and verifier roles.

`adopt` and `promote` fail closed unless the benchmark passes, the resulting and subject pins equal the candidate, rollback has been preflight-verified, and evidence supports the claimed maturity. A failed candidate retains the previous baseline and emits `reject`.

Rollback re-runs destination verification. Successful restoration emits `rollback` with `rollback_verified: true` and the rollback target as the resulting baseline. Failed restoration emits `rollback-failed`, `rollback_verified: false`, and an explicit `none` baseline. Revocation is a distinct `revoke` event with a reason and an explicit `none` baseline; it is not silently represented as rejection or demotion.
