# CodeRabbit dispositions 20260721T1359Z

Reviewed head before edits: `1a0d3d59265ccfae86520cfa6bfaeebc091b36e1`
Latest CR review integrated: 2026-07-21T13:35:27Z (1 actionable + 1 duplicate on head 1a0d3d5).
CodeRabbit commit status at open: SUCCESS (treated as review input, not Gate1 GO).

## Fixed this cycle

| Finding | Disposition | Notes |
|---|---|---|
| On-disk `sources/*.md` not bound to provenance | fixed | parse card bullets; field-for-field match; negative URL-drift test |
| `_parse_iso_utc` accepted naive timestamps | fixed | require explicit offset/Z; negative regression |

## Explicit skips / deferred

| Finding | Disposition | Reason |
|---|---|---|
| `.github/workflows/*` Gitleaks/persist-credentials/DIFF_BASE | deferred | OAuth lacks `workflow` scope |
| Historical disposition MD blank-line nits | skip | historical docs |
| Heavy claim-register / schema expansion beyond latest actionable set | deferred | stop-rule: avoid endless CR architecture churn |
| Independent Gideon exact-head review | next | AakashSrinivasan is collaborator; request review on new head |

## Non-claims

Not merged. Not Gate1 GO. No Discord dual-write from controller. Expert live gateway already answered Srini handoff diagnosis (stale channel allowlist) — controller remained protocol-silent. `DISCORD_ALLOWED_CHANNELS` repair widens admission and stays Sameer-gated.
