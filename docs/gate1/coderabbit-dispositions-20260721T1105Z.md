# Gate1 CodeRabbit dispositions (20260721T1105Z)

- Base head: 0e49cd7664453e2dc3b1360a9bd1a90a12d5a5e4
- Prior CodeRabbit review submitted_at: 2026-07-21T10:10:18Z (mapped commit a49b613→0e49cd7)
- Checks at cycle start: validate=pass, CodeRabbit=pass/Review completed

## Applied this cycle

| Finding | Disposition | Notes |
|---|---|---|
| gitleaks installer OS check | fixed | reject non-Linux before arch/download |
| capability-manifest evidence environment_digest | fixed | required 64-hex digest; unit test |
| Gate1 disposition MD under receipts/ | fixed | moved to docs/gate1/; validate_receipts fail-closed on non-JSON operational artifacts |
| expert identity commit pin | fixed | retargeted to b22292f793fc467e057555e8ff75f02dbaea10cc |

## Deferred / not fixed

| Finding | Disposition | Notes |
|---|---|---|
| workflow persist-credentials | deferred | OAuth lacks workflow scope |
| workflow SAN_DIFF_BASE event SHA | deferred | same |
| workflow job name cosmetic | skip | trivial |
| exclusive writer leases across objects | deferred heavy | beyond Gate1 finish line |
| capability-manifest structured rollback object | deferred heavy | status rollback still free-text for planned manifests |

## Non-claims

Not merged; not Gate1 GO; Gideon invite still pending AakashSrinivasan; no Discord dual-write; workflow YAML untouched.
