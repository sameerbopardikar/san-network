# CodeRabbit dispositions 20260721T1250Z

Reviewed head before edits: `07190e820505d1659d7c6b322bd5ca572732433f`
Latest CR review integrated: 2026-07-21T12:32:35Z (4 actionable + duplicates on head 07190e8).

## Fixed this cycle

| Finding | Disposition | Notes |
|---|---|---|
| `fail_commit_status: false` | fixed | set `true` so unavailable/stale CR fails closed |
| Relation target traversal / concepts strip alias | fixed | reject `..`, absolute paths; bare slug under concepts only |
| `released_at` string sort | fixed | parse ISO → UTC instants before compare |
| Source card must be in artifact `source_ids` | fixed | membership gate + negative test |
| Source card `revision_url` binding | fixed | added to meta_fields + mismatch test |
| invalid-evidence-format empty URI | fixed | valid URI; sole invalid field remains bad sha256 |
| Receipts URI-only evidence | fixed | structured `{uri,sha256,subject_pin}` schema + semantic pin match |
| Self-merge targeted assertion | fixed | asserts exact merger/executor error |
| setUpClass ANN206 | fixed | `-> None` |

## Explicit skips / deferred

| Finding | Disposition | Reason |
|---|---|---|
| `.github/workflows/validate.yml` persist-credentials / SAN_DIFF_BASE / gitleaks install | deferred | OAuth lacks `workflow` scope; cannot push workflow YAML |
| Old disposition MD separator nits | skip | historical docs; low value |
| Nemertes unbound reviewer/verifier (older thread) | skip/observe | needs identity-registry expansion beyond this quick-win slice; not in 12:32 actionable set |
| Gideon invite accept | blocked | owner Aakash must accept pending write invite |

## Non-claims

Not merged. Not Gate1 GO. Not CodeRabbit SUCCESS on the new head yet. No Discord dual-write. No Multica onboard. CI workflow pin still deferred.
