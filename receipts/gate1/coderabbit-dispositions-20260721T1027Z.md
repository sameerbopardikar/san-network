# Gate1 CodeRabbit dispositions (20260721T1027Z)

- Reviewed head (pre-fix): `a49b61331a0cf5344276f19a8c2803e7bcc8f794`
- Post-fix head: (see latest commit; CI fix removes PyYAML dependency from relation parser)
- CodeRabbit prior review submitted_at: 2026-07-21T10:10:18Z

## Applied (this commit)

| Finding | Disposition | Notes |
|---|---|---|
| test_draft latest pin under invalid kind | fixed | uses `git-commit` + value `latest`; asserts pattern failure |
| capability-manifest evidence attribution | fixed | require actor/timestamp/verdict on evidence items |
| work-object evidence.actor free string | fixed | agent_id or github: login patterns |
| adoption demote explicit none | fixed | oneOf: verified predecessor (`rollback_verified` true) OR none baseline (false) |
| adoption pairwise distinct roles | fixed | `adoption_receipt_errors` + unit test |
| corpora front-matter relations targets | fixed | validate_links resolves relation targets; negative test |
| source card metadata mismatch | fixed | optional `source_cards` field-for-field vs provenance; negative test |
| expert verified identity mutable URL | fixed | evidence_uri pinned to immutable commit `a49b613…` |

## Deferred / not fixed

| Finding | Disposition | Notes |
|---|---|---|
| workflow persist-credentials | deferred | OAuth lacks `workflow` scope; non-claim |
| workflow SAN_DIFF_BASE event SHA | deferred | same workflow scope gate |
| workflow job name cosmetic | skip | trivial/low value |
| exclusive writer leases across objects | deferred heavy | needs lease registry beyond Gate1 |
| ISSUE_TEMPLATE excluded/gates/rollback | already satisfied | fields already required on current template |
| deeper capability maturity evidence gates | partial | attribution required; fuller maturity ladder later |

## Non-claims

Not merged; not Gate1 GO; Gideon invite still pending `AakashSrinivasan`; no Discord dual-write; workflow YAML untouched.
