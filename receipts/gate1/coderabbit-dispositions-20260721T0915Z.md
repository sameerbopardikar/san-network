# Gate1 CodeRabbit dispositions

- Reviewed commit (immutable): `5bc5452328bf322698867d8373c29a6b0037beb7`
- PR: https://github.com/sameerbopardikar/san-network/pull/1
- Review evidence: CodeRabbit SUCCESS context on head `5bc5452` (submitted 2026-07-21T09:27:07Z); Actions run `29817587990` validate SUCCESS.
- Executor: Expert SAN controller (origin idle after tool-ceiling recovery). Not a merge.
- Gideon independent review still required on this SHA and any later HEAD.


## Fixed this cycle (2026-07-21T09:15Z)
1. All ten concept `## Evidence basis` sections now name exactly the manifest `source_ids` for that artifact (stable ids + display labels).
2. `capabilities/README.md` — present-tense adoption/rollback claims gated on destination authority, sandbox, conformance, receipts.
3. `capabilities/skills/bootstrap-agent-from-kernel/README.md` + `manifest.draft.json` rollback — no destination mutation while `planned-not-released`.
4. `kernel/requirements-dev.txt` — add `rfc3986-validator` and `rfc3339-validator` so `FormatChecker` enforces `uri` / `uri-reference` / `date-time`.
5. `CLAIMS.md` — SAN-006/008/009 Built rows get explicit evidence-boundary non-claims (no fabricated immutable receipts).
6. Regenerated concept artifact sha256 values and rebound draft `corpus_pin` to manifest sha256 `a12ce0d6d9cf5c19cadfa16b1414563d893e720a9a3b659767da74049db6cfd3`.

## Explicit skips / already true
| Finding | Verdict | Reason |
|---|---|---|
| `blobs.lock` missing | already-true | File present and inventory-matched. |
| merger≠executor validator | already-true | `kernel/scripts/validate.py` fail-closed via identity registry. |
| `persist-credentials: false` on checkout | defer-auth | Token scopes are `gist,read:org,repo` — no `workflow`; cannot push workflow YAML edits. |
| event-specific `SAN_DIFF_BASE` | defer-auth | Same workflow-scope gate. |
| full source-card metadata equality bind | defer-heavy | Existence bind present; full card equality is next corpus gate. |
| composable privacy audience/constraints enum split completion | defer-heavy | Audience+constraints fields already on draft objects; broader adversarial matrix later. |
| outdated threads on 9c33170/913ad15 | outdated | Superseded by later heads. |

## Non-claims
- Not merged to main
- Not Gate1 GO
- Not Gideon invite accepted / exact-head GO
- Not workflow YAML change live
- Not peer adoption / Multica onboarded
