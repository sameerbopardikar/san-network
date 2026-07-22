# Gate1 CodeRabbit disposition — full review on f78e0bd2307088b1b7d4891209a6f79f5fb71873

Reviewed head: `f78e0bd2307088b1b7d4891209a6f79f5fb71873` (full 40-char SHA)
Review timestamp: 2026-07-22T02:37:17Z
Review comment URL: https://github.com/sameerbopardikar/san-network/pull/1 (review id 4750499249)
Not auto-paused — confirmed fresh full review against exact current head, no "Reviews paused" banner present.

## Actionable findings (9)

1. `.github/PULL_REQUEST_TEMPLATE.md` — Evidence maturity field is free text; constrain to canonical vocabulary shared with work-object schema.
2. `.github/workflows/validate.yml` — CI diff-check step should derive `SAN_DIFF_BASE` from event context (PR base sha / push before) rather than hardcoding a fixed comparison.
3. `capabilities/scripts/validate_manifests.py` — evidence iteration should reject non-list `evidence` / non-object items explicitly instead of raising on `.get()`.
4. `corpora/scripts/verify_release.py` — `load_provenance`'s `source_id` is used to build a filesystem path (`sources/{source_id}.md`) without charset/format validation; sanitize before path construction.
5. `docs/gate1/coderabbit-dispositions-20260721T1105Z.md` — prior disposition record uses abbreviated commit SHAs (`a49b613`, `0e49cd7`); Gate1 evidence should always bind full 40-char SHAs.
6. `docs/gate1/coderabbit-dispositions-20260721T1359Z.md` — contains live-network assertions (Expert gateway handoff diagnosis, DISCORD_ALLOWED_CHANNELS widening) with no immutable receipt binding; remove or bind to an exact receipt.
7. `kernel/scripts/evidence.py` — sha256 pattern consistency finding (analysis chain; needs read of exact current regex usage).
8. `scripts/validate_all.py` — unavailable-gitleaks soft-fail path only enforced via `SAN_REQUIRE_GITLEAKS=1`; CI should set that variable so this branch cannot silently pass a secret gate in an environment that forgets to set it.
9. `capabilities/tests/test_draft.py` (duplicate comment, carried from earlier head) — released-manifest raw-owner-memory test fixture should isolate the constraint under test rather than relying on an already-invalid draft fixture.

## Disposition

**Deferred — controller freeze in effect.** Per `controller-gate1-freeze-20260721T143613Z` (delegation-greediness / verified-autonomy stop-loss), monorepo remediation churn is paused while `AakashSrinivasan`'s exact-head human review is the outstanding finish-line blocker for PR#1. `AakashSrinivasan` remains a requested reviewer on `f78e0bd` and has not yet re-reviewed this exact head (his last review, CHANGES_REQUESTED, was on ancestor `13537e4`).

These 9 CodeRabbit findings are real, substantive, and unaddressed on current bytes — none are stale/paused-review artifacts. They are recorded here as evidence for the next remediation cycle (whenever the freeze is lifted, either by Sameer, by Gideon's re-review landing, or by an explicit controller decision that consolidating CR fixes before the human re-review is worth one more push). No code changes were made this cycle to honor the freeze and avoid another remediation round before the irreducible human-review gate resolves.

## Verification performed this cycle (read-only)
- Confirmed via GitHub API that this review (id 4750499249) is not an auto-pause artifact — inspected the CodeRabbit comment body directly, no "Reviews paused" banner, `"Full review finished"` action performed.
- Confirmed `reviewDecision: CHANGES_REQUESTED` on PR#1 is inherited from Aakash's stale review on ancestor `13537e4` (GitHub does not clear reviewDecision on push); Aakash has not yet reviewed `f78e0bd`.
- Confirmed PR#5 (`5c5f6a5`) and PR#2/sovereign-agent-network (`9d13ea7`) unchanged — still correctly gated on human re-review, no new findings.
- Confirmed all 3 active SAN worktrees clean, no uncommitted/orphaned mutations.
- Confirmed Discord observer: `new_message_count: 0`, `latest_id` unchanged (`1529288829733703801`) — no protocol activity this cycle.
