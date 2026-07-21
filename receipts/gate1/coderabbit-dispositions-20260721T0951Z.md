# Gate1 CodeRabbit dispositions

- Reviewed base commit (immutable): `5bc5452328bf322698867d8373c29a6b0037beb7`
- This disposition commit (immutable): `3091c64dd8b272a4e294f0ffd72e85ac9a4a48ee`
- PR: https://github.com/sameerbopardikar/san-network/pull/1
- Executor: Expert SAN controller (origin idle; single-writer). Not a merge.
- Gideon independent review still required on post-push HEAD.

## Fixed this cycle (2026-07-21T09:51Z)
1. `.github/PULL_REQUEST_TEMPLATE.md` — top-level `# Objective` heading (markdownlint).
2. `kernel/agents/expert.json` — pin `runtime.evidence_uri` to immutable Hermes commit `9de9c25f620ff7f1ce0fd5457d596052d5159596` and content-addressed version string.
3. `kernel/requirements-dev.txt` — exact pins `jsonschema==4.26.0`, `rfc3986-validator==0.1.1`, `rfc3339-validator==0.1.4`.
4. `receipts/scripts/validate_receipts.py` — report malformed JSON as validation error instead of aborting; fixture `receipts/fixtures/invalid/malformed-json.json`.
5. `scripts/install_gitleaks_8.30.1.sh` — arch-aware (`x64`/`arm64` with live arm64 checksum), default user-writable `$HOME/.local/bin`, override via `GITLEAKS_INSTALL_DIR`.
6. Prior disposition receipts `0839Z`/`0915Z` — replace mutable “HEAD pending commit” with full reviewed SHAs + review evidence IDs.

## Explicit skips / deferred
| Finding | Verdict | Reason |
|---|---|---|
| `validate.yml` persist-credentials | defer-auth | OAuth token lacks `workflow` scope; cannot push workflow YAML. |
| `validate.yml` event SAN_DIFF_BASE | defer-auth | Same workflow-scope gate. |
| source-card full metadata bind | defer-heavy | Next corpus gate. |
| front-matter relation targets | defer-heavy | Next corpus gate. |
| privacy composable labels full schema | defer-heavy | Audience+constraints already on drafts; broader matrix later. |
| exclusive writer lease registry | defer-heavy | Post-Gate1 kernel enforcement. |
| Multica product onboard | reject | adapt-not-adopt freeze. |

## Non-claims
- Not merged to main
- Not Gate1 GO
- Not Gideon invite accepted / exact-head GO
- Not workflow YAML change live
- Not peer adoption
