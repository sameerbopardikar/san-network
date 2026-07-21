---
title: Validation and Feedback Loops
type: concept
article_status: canonical
status: developing-doctrine
summary: The checks and corrective cycles that let an agent observe whether its work satisfies the intended contract, repair failures, and rerun until a valid stop condition is reached.
taxonomy_path:
  - Agentic Engineering
  - Reliability
relations:
  - type: part_of
    target: concepts/agentic-layer
    label: Agentic Layer
  - type: validates
    target: concepts/durable-execution
    label: Durable Execution
  - type: feeds
    target: concepts/evaluation-observability
    label: Evaluation and Observability
  - type: constrains
    target: concepts/multi-agent-orchestration
    label: Multi-Agent Orchestration
---

# Validation and Feedback Loops

A feedback loop gives an agent a way to observe the consequences of its work, compare them with an explicit contract, correct failures, and try again. Without feedback, an agent performs open-loop generation: it produces an artifact and relies on confidence or human inspection to determine whether the result works.

Closed loops are one of the highest-leverage differences between conversational assistance and reliable agentic execution.

## Basic loop

A minimal loop is:

`act → observe → compare → diagnose → repair → rerun`

The comparison requires a validator. Validators may include tests, type checks, linters, schema checks, browser assertions, data reconciliations, citation checks, policy checks, independent review, or measured external outcomes.

The loop should define both success and stop conditions. “Keep trying until it works” can create unbounded cost, repeated unsafe actions, or optimization against a weak test.

## Validator design

A validator should be:

- **Relevant:** it tests the intended outcome, not an easy proxy.
- **Authoritative:** the agent cannot simply rewrite the check to approve its own work.
- **Current:** it runs against the exact artifact or state being promoted.
- **Reproducible:** another process can rerun it.
- **Adversarial where needed:** important negative paths are tested, not only the happy path.
- **Bounded:** cost and retry limits are explicit.

A green unit test suite can still miss product intent, security boundaries, or browser behavior. Validation is usually layered rather than singular.

## Testing versus review

Testing asks whether the artifact behaves according to executable checks. Review asks whether it matches intent, architecture, scope, policy, and quality. The same agent may run tests during implementation, but consequential work benefits from an independent reviewer whose judgment is bound to the exact commit or artifact inspected.

A review verdict expires when the reviewed bytes change. Likewise, earlier green tests do not validate later edits.

## Agent-accessible feedback

Checks become most useful when agents can invoke and interpret them directly. A closed-loop prompt should name:

- exact validation commands;
- expected output or acceptance thresholds;
- how to classify failures;
- what may be changed to repair them;
- which failures require escalation;
- when to stop retrying.

The validator is part of the tool environment, not decorative prose in a plan.

## Feedback hierarchy

Different evidence answers different questions:

1. **Static checks:** syntax, types, schemas, formatting, policy.
2. **Unit and integration tests:** local behavioral contracts.
3. **End-to-end tests:** connected system behavior.
4. **Adversarial probes:** security, replay, concurrency, and failure boundaries.
5. **Human review:** intent, quality, taste, and risk judgment.
6. **Production or longitudinal outcomes:** whether the system created the intended real-world result.

Passing an earlier layer does not imply passing a later one. The system should report its actual evidence maturity rather than compressing all checks into “verified.”

## Feedback and learning

A completed loop can update more than the artifact. Repeated failures may reveal a missing context field, weak validator, ambiguous workflow step, or bad doctrine. Those lessons should become durable improvements to the [[concepts/agentic-layer|agentic layer]] when they generalize.

The objective is not merely self-correction within one run. It is compounding reliability across a problem class.

## Failure modes

- **False green:** checks pass but do not cover the real outcome.
- **Self-approval:** the same agent weakens the test or judges its own evidence.
- **Stale proof:** validation applies to an earlier artifact.
- **Infinite repair:** retries continue without a bounded stop rule.
- **Proxy optimization:** the agent improves the metric while harming the actual objective.
- **Downstream continuation after failure:** later stages run despite a required check failing.

## Evidence basis

The practitioner doctrine is developed in [[sources/private-practitioner/agentic-engineer-tactical-agentic-coding-close-the-loops|Close the Loops: More Compute, More Confidence]] and synthesized in [[synthesis/tactical-agentic-coding-operating-system|Tactical Agentic Coding: Operating-System Synthesis]]. Local receipts linked from [[index|Agentic Engineering Operating Corpus]] provide bounded implementation evidence for replay and validation contracts.
