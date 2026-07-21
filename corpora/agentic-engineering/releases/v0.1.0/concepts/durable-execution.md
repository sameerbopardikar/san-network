---
title: Durable Execution
type: concept
article_status: release-synthesis
status: developing-doctrine
summary: The mechanisms that keep work identified, owned, recoverable, and safe across model turns, process exits, retries, crashes, and overlapping workers.
taxonomy_path:
  - Agentic Engineering
  - Reliability
relations:
  - type: part_of
    target: concepts/agentic-engineering
    label: Agentic Engineering
  - type: depends_on
    target: concepts/work-ownership
    label: Work Ownership
  - type: implements
    target: concepts/agent-lifecycle
    label: Agent Lifecycle
  - type: validated_by
    target: concepts/validation-feedback-loops
    label: Validation and Feedback Loops
  - type: observed_by
    target: concepts/evaluation-observability
    label: Evaluation and Observability
---

# Durable Execution

Durable execution is the ability of a system to keep work correct and owned across the failure of any individual agent turn, process, session, or worker. It converts ephemeral model activity into a recoverable operational process.

The key idea is simple: the work must outlive the worker. A task is not durable merely because a cron job can rerun a prompt or because a transcript records that the agent intended to continue. The system needs canonical identity, persisted state, safe transitions, and evidence-backed completion.

## Core mechanisms

### Stable identity

Every durable work object needs a canonical identifier shared by triggers, workers, events, checkpoints, receipts, and user-facing projections. Stable identity allows the system to recognize retries and duplicates as the same work rather than unrelated runs.

### Append-only events or equivalent authoritative state

Important transitions should be persisted before dependent action proceeds. Event logs are useful because they reconstruct how state changed, but a carefully guarded transactional state record can also work. The invariant is that restart does not require a previous process’s memory.

### Leases and heartbeats

A lease grants one worker temporary authority to act on a work object. Heartbeats show that the lease holder is alive. When the lease expires, a recovery controller can reclaim the work.

Leases do not by themselves prevent stale workers from writing. Consequential mutations require fencing or generation checks so that an old worker cannot commit after a new owner has taken over.

### Checkpoints

A checkpoint records enough state to resume without repeating unsafe work. Good checkpoints distinguish completed internal computation from external side effects. They preserve source versions, artifact identities, and the next valid transition.

### Idempotency and deduplication

Idempotency ensures that repeating the same command converges on the same result. Deduplication detects equivalent submissions before they create overlapping execution. External actions often require idempotency keys or read-before-write reconciliation because “retry the whole agent” is not safe.

### Retries and dead letters

Retries should be bounded, classified, and observable. Transient failures may retry automatically; persistent or policy failures should enter a durable blocked or dead-letter state with an owner and recovery path. Endless retry loops are not resilience.

### Evidence-backed completion

Completion requires proof tied to the current artifact or state. A worker exit, a final message, or a green check from earlier bytes is insufficient. The completion transition should name the validators, receipts, and exact version that passed.

## Ownership before scheduling

Scheduling wakes work; it does not own work. A cron row can say when to run, but it does not explain the current mission, attempts, blockers, or terminal evidence. [[concepts/work-ownership|Work ownership]] must live in a canonical controller or work record. Schedulers, queues, Slack updates, and dashboards are projections or executors around that authority.

## Failure model

Durable systems assume failure at boundaries:

- the process exits after an external action but before recording success;
- two workers receive the same task;
- a lease expires while the old worker is still running;
- state is written but the projection is not refreshed;
- a validator checks stale artifacts;
- a human gate is approved after the original worker disappears;
- a retry runs against changed inputs.

Tests should interrupt execution between transitions, not only restart after the happy path has completed.

## What durability is not

Durability is not:

- a long-running shell process;
- a background agent that usually finishes;
- a scheduler reporting `last_status: ok`;
- a chat history containing the plan;
- a dashboard row that says “active”;
- retrying until something returns success.

Those can support a durable system, but none is the source of operational truth.

## Evidence basis

The durability model here is network-authored doctrine. Public corroboration is limited to the pinned CloudEvents, OpenTelemetry, and Hermes Agent source cards. Excluded local implementations are disclosed as absent and do not support public verification claims.
