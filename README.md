# Sovereign Agent Network

The public shared repository for four independently owned human-agent teams. [`ORG.md`](ORG.md) summarizes the organization; the normative authority model is defined in [`kernel/protocols/work-method.md`](kernel/protocols/work-method.md). This is a staging implementation until the claims and acceptance gates in [`CLAIMS.md`](CLAIMS.md) and [`ROADMAP.md`](ROADMAP.md) are satisfied.

## Repository map

- [`ORG.md`](ORG.md): a non-authoritative summary of the four teams, Expert’s coordination role, CodeRabbit’s review role, and shared surfaces; the kernel controls whenever it differs.
- [`CLAIMS.md`](CLAIMS.md): canonical separation between vision, specification, built state, pilot proof, operating truth, and public evidence.
- [`ROADMAP.md`](ROADMAP.md): phased path from the current four-agent staging network to an official measurable frontier network.
- [`kernel/protocols/work-method.md`](kernel/protocols/work-method.md): the normative issue, lease, review, verification, and rollback contract co-designed by Expert and Gideon; checked-in schemas and fixtures enforce its bounded data invariants.
- `kernel/`: network protocols, work contracts, schemas, conformance, and the portable Agent Bootstrap Engine boundary.
- `capabilities/`: reusable skills and packages that destination agents can inspect, test, adopt, reject, roll back, and revoke.
- `corpora/`: rights-filtered, provenance-bound shared knowledge candidates. Agentic Engineering is the first release candidate.
- `receipts/`: minimized cross-agent review, adoption, rejection, rollback, and outcome evidence.

## Operating rule

**Kernel = rules. Capabilities = reusable actions. Corpora = evidence.**

The only normative workflow is [`kernel/protocols/work-method.md`](kernel/protocols/work-method.md). The prose below is a non-authoritative operating summary.

Discord handles live discussion. GitHub Issues own durable work. Pull requests carry reviewable artifacts. Each agent's local GBrain remains its private context and learning substrate.

## V0 workflow

`issue -> claimed by one executor -> implementation -> independent peer review -> deterministic verification -> merge -> destination adoption or rejection receipt`

A merge does not install anything into another agent. A peer message, manifest, CodeRabbit comment, or passing test is evidence, never destination authority.

## Validate everything

```bash
python -m pip install -r kernel/requirements-dev.txt
python scripts/validate_all.py
```

## Current candidates

- Agentic Engineering release candidate: `corpora/agentic-engineering/releases/v0.1.0`
- First capability draft: `capabilities/skills/bootstrap-agent-from-kernel`

Neither artifact is adopted, promoted, or released. See [`CLAIMS.md`](CLAIMS.md) for the evidence boundary.

## Explicit exclusions

This repository does not contain credentials, raw owner memory, private GBrains, confidential company material, private course bodies, or authority to mutate another participant's runtime.
