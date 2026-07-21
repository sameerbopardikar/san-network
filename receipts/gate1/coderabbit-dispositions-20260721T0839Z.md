# Gate1 CodeRabbit dispositions (HEAD pending commit)

Executor: Expert (controller recovery). Not a merge. Gideon independent review still required on post-push HEAD.

## Fixed this cycle
1. `.github/CODEOWNERS` — replace `@Aakashsrini` with authenticated `@AakashSrinivasan`; keep `.coderabbit.yaml` ownership.
2. `kernel/README.md` — finish line names pairwise-distinct executor, reviewer, verifier.
3. `corpora/tests/test_release.py` — portable `tempfile.TemporaryDirectory` cwd.
4. `corpora/scripts/verify_release.py` — require `included_raw_body is False`.
5. `corpora/.../manifest.json` — `released_at` after latest provenance retrieval; draft `corpus_pin` rebound to new manifest sha256.
6. `kernel/scripts/validate.py` — merger/executor check fails closed when executor is not a verified registry identity.
7. `receipts/scripts/validate_receipts.py` — also validate non-fixture operational receipt JSON under `receipts/`.
8. `capabilities/tests/test_draft.py` — assert intended rejection messages (not any error).
9. `ROADMAP.md` — normative-rule scope exempts governance docs; points at maturity fixture.

## Explicit skips (still open / deferred)
| Path | Verdict | Reason |
|---|---|---|
| `ci/github-actions-validate.yml.pending` | outdated | File removed; live workflow is `.github/workflows/validate.yml`. |
| bootstrap deps `>=0.1.0` | outdated | Draft manifest has no floating dependency range. |
| `work-contract.md` lease metadata | defer-heavy | Requires protocol+schema expansion; tracked post-Gate1. |
| adoption-receipt extra pattern tightening | skip-already | `agent_id` already pattern-constrained via `$defs`. |
| corpora source-card full metadata bind | defer-heavy | Existence bind present; full card equality is next corpus gate. |
| work-object FormatChecker tooling note | skip | CI installs jsonschema FormatChecker; valid fixtures pass. |
| validate.yml event diff base | defer-auth | OAuth token lacks `workflow` scope; cannot push workflow edits. Local/CI still use `SAN_DIFF_BASE` when set. |
| validate.yml persist-credentials | skip-ok | checkout@pinned; contents:read only. |
| capabilities README operational claims | skip-status | Status remains `planned-not-released` with explicit non-claims. |
| CLAIMS evidence contract for Built rows | defer | Status vocabulary already canonical; richer immutable receipts are Gate2+. |
| blobs.lock missing | outdated | `blobs.lock` present and verified. |
| privacy composable labels schema | defer-heavy | Audience+constraints fields exist on draft; full enum split later. |
| work-method merger prose | skip | Validator enforces merger≠executor fail-closed now. |
| receipts only fixtures historically | fixed | Operational path added. |
| concept evidence-basis name drift | defer | Public doctrine language; provenance IDs remain authoritative. |
| capabilities README rollback contract | skip-status | Draft rollback is local-manifest only; destination state non-claim explicit. |

## Non-claims
- Not merged to main
- Not Gate1 GO
- Not Gideon accepted invite / exact-head review complete
- Not workflow YAML change live
- Not peer adoption
