# Promotion, Demotion, and Rollback Protocol

- Protocol ID: `san.promotion-rollback`
- Version: `0.1.0`
- Authority: kernel normative rule

## Promotion

A capability may become a baseline only when one machine-valid receipt records:

1. the previous baseline exact pin;
2. the candidate exact pin;
3. benchmark ID and exact version;
4. threshold fixed before execution;
5. observed result;
6. distinct executor, reviewer, and verifier identities;
7. destination evidence pointers;
8. the resulting baseline exact pin; and
9. an exact rollback target.

Promotion fails closed when the fixed benchmark does not pass or when any required field, test, independent role, current-head evidence pointer, maturity proof, or rollback preflight is missing. The subject and resulting baseline pins must equal the candidate pin. Popularity, prose review, or source-agent success alone cannot promote a capability.

## Demotion

A current baseline is demoted when monitored evidence invalidates a required claim, the evidence expires, a security or privacy violation occurs, or destination verification no longer passes. Demotion keeps the prior receipt visible, records the reason, and selects either a verified predecessor or explicit `none` as the resulting baseline.

## Rollback

Rollback restores the receipt's exact rollback target, re-runs destination verification, and emits a rollback receipt. A rollback is not complete until `rollback_verified` is true and the resulting baseline equals the rollback target. If restoration fails, emit `rollback-failed` with `rollback_verified: false` and an explicit `none` baseline; no coordinator may silently preserve the failed candidate. Permanent invalidation emits the distinct `revoke` event with a reason and explicit `none` baseline.

## Separation of duties

The executor, reviewer, and verifier must be pairwise distinct for the same event. The verifier decides whether measured evidence meets the fixed threshold. The coordinator may publish the resulting registry update only after receipt validation passes.
