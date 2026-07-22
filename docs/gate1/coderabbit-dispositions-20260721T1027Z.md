# Gate1 CodeRabbit dispositions (20260721T1027Z)

- Reviewed head (pre-fix): a49b61331a0cf5344276f19a8c2803e7bcc8f794
- Functional fix head (CI green run 29822408360): 01ea4e00dbf4e9d4957d233ba67b4e43c80e82bb
- CodeRabbit prior review submitted_at: 2026-07-21T10:10:18Z

## Applied

| Finding | Disposition | Notes |
|---|---|---|
| test_draft latest pin under invalid kind | fixed | uses git-commit kind with value latest; asserts pattern failure |
| capability-manifest evidence attribution | fixed | require actor/timestamp/verdict on evidence items |
| work-object evidence.actor free string | fixed | agent_id or github login patterns |
| adoption demote explicit none | fixed | oneOf verified predecessor (rollback_verified true) OR none baseline (false) |
| adoption pairwise distinct roles | fixed | adoption_receipt_errors plus unit test |
| corpora front-matter relations targets | fixed | validate_links resolves relation targets; negative test |
| source card metadata mismatch | fixed | optional source_cards field-for-field vs provenance; negative test |
| expert verified identity mutable URL | fixed | evidence_uri pinned to immutable commit a49b613 |
| PyYAML CI dependency | fixed | stdlib-only front-matter relation parser |

## Deferred / not fixed

| Finding | Disposition | Notes |
|---|---|---|
| workflow persist-credentials | deferred | OAuth lacks workflow scope; non-claim |
| workflow SAN_DIFF_BASE event SHA | deferred | same workflow scope gate |
| workflow job name cosmetic | skip | trivial |
| exclusive writer leases across objects | deferred heavy | lease registry beyond Gate1 |
| ISSUE_TEMPLATE excluded/gates/rollback | already satisfied | fields already required |

## Non-claims

Not merged; not Gate1 GO; Gideon invite still pending AakashSrinivasan; no Discord dual-write; workflow YAML untouched.
