# CodeRabbit dispositions 20260721T1325Z

Reviewed head before edits: `0b04d61a12861f7b0f8b6004f42ad79cd9647282`
Latest CR review integrated: 2026-07-21T13:04:04Z (7 actionable on head 0b04d61).
CodeRabbit commit status at open: SUCCESS (still treating as review input, not Gate1 GO).

## Fixed this cycle

| Finding | Disposition | Notes |
|---|---|---|
| `test_cross_plane_artifact_path` fallback `or self.errors` | fixed | assert path-targeted errors only |
| Excluded-source substantive claims in agentic-engineering.md | fixed | boundary disclosure only; rebind concept sha256 |
| kernel README unittest PYTHONPATH | fixed | root and cd-kernel paths |
| corpus-release `handling_constraints` missing `no-raw-owner-memory` | fixed | enum parity with capability-manifest |
| `golden_fixture.required:false` forces fabricated fields | fixed | allOf if/then + inapplicable_reason |
| latest_retrieval lexical max with mixed offsets | fixed | max by parsed UTC instant + regression test |

## Explicit skips / deferred

| Finding | Disposition | Reason |
|---|---|---|
| `.github/workflows/validate.yml` SAN_REQUIRE_GITLEAKS / persist-credentials / SAN_DIFF_BASE | deferred | OAuth lacks `workflow` scope; cannot push workflow YAML |
| Historical disposition MD blank-line nits (0839Z) | skip | historical docs; low value |
| CLAIMS free-form status composites / Built evidence completeness | deferred | heavy claim-register rewrite; not in 7-item actionable primary set without large prose churn |
| Gideon invite accept | blocked | pending write invite for AakashSrinivasan |

## Non-claims

Not merged. Not Gate1 GO. Independent Gideon exact-head review still required. No Discord dual-write. No Multica onboard. CI workflow pin still deferred.
