# Gate1 CodeRabbit dispositions 20260721T1142Z

Head base: d3ac0cb5fc988cf6081a8143776b31c8b852efcc
Review run: 2026-07-21T11:27:02Z (18 actionable + 2 workflow duplicates)

## Applied (non-workflow)

| Finding | Disposition | Notes |
|---|---|---|
| README four-agent pilot | fixed | staging network wording |
| environment_digest prefix compare | fixed | `_norm_digest` in kernel/scripts/validate.py |
| invalid-same-role independent-review actor | fixed | actor=roles.reviewer |
| gitleaks curl timeouts | fixed | connect 15s / max 120s |
| receipts skip path component | fixed | top-level skip_roots only |
| receipts fail-closed probe isolation | fixed | TemporaryDirectory + MODULE.ROOT |
| adversarial fixture predicates | fixed | expected failure map |
| receipts evidence pointer + none baseline docs | fixed | README contract |
| gideon owner_binding verified without pin | fixed | downgraded to pending |
| authority-bands enforcement prose | fixed | softened; destination-local remains authoritative |
| AgentDojo executable lane claim | fixed | pinned external reference only + manifest hash rebind |
| handling_constraints no-raw-owner-memory | fixed | schema enum + draft manifest + test |
| test_draft setUpClass annotation + negatives | fixed | artifacts required + path-focused |
| CLAIMS SAN-006/008/009 Built honesty | fixed | rollback N/A + mutable tip boundary |

## Deferred

| Finding | Reason |
|---|---|
| .github/workflows persist-credentials | OAuth lacks `workflow` scope; cannot push workflow YAML |
| .github/workflows SAN_DIFF_BASE event base | same workflow scope gate |
| full authority-bands machine enforcement | heavy; prose corrected instead |
| verify_release source-card deep bind beyond current | deferred heavy; existing source-card tests remain |
| full none-baseline valid receipt fixtures (reject/rollback-failed/revoke) | deferred medium; docs updated |
| nemertes unbound principal rejection expansion | deferred medium |

## Non-claims
Not merged. Not Gate1 GO. Gideon invite still pending. No Discord dual-write.
