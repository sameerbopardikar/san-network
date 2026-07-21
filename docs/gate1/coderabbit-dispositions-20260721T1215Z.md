# CodeRabbit dispositions 20260721T1215Z

Reviewed head before edits: `d4b7a7af68daa505502e6a68df1955dccfc5b11d`
Latest CR reviews integrated: 2026-07-21T11:56:42Z (11 actionable), 2026-07-21T12:06:12Z (4 actionable + duplicates).

## Fixed this cycle

| Finding | Disposition | Notes |
|---|---|---|
| Released capability must require `no-raw-owner-memory` | fixed | schema `allOf` + negative test asserts `errors(data)` |
| CONTRIBUTING claims schema validates full workflow | fixed | narrowed to bounded data invariants |
| Corpus `released_at` not after retrievals | fixed | `2026-07-21T05:46:00Z` + verifier chronology gate |
| `verify_release` repo_root via `parents[3]` | fixed | uses `SCRIPT_ROOT.parent` |
| network-operating-model missing protocol header | fixed | Protocol ID/Version/Authority |
| privacy-labels machine-enforcement prose | fixed | policy wording; enforcement not claimed from prose alone |
| kernel README root-relative validate paths | fixed | documents root and `cd kernel` forms |
| CLAIMS SAN-006/008/009 Built without immutable receipts | fixed | downgraded to **Specified** with honest evidence boundaries |

## Explicit skips / deferred

| Finding | Disposition | Reason |
|---|---|---|
| `.github/workflows/validate.yml` persist-credentials / SAN_DIFF_BASE | deferred | OAuth lacks `workflow` scope; cannot push workflow YAML |
| Heavy corpus source-card / AgentDojo benchmark lane items already addressed on prior heads | skip | prior dispositions + current wording already staging/external-ref |
| Gideon invite accept | blocked | owner Aakash must accept pending write invite |
| Receipts isolation / adversarial predicates / gideon owner pending | skip | already fixed on d4b7a7a; CR duplicate/stale on older comments |

## Non-claims

Not merged. Not Gate1 GO. Not CodeRabbit SUCCESS on the new head yet. No Discord dual-write. No Multica onboard.
