---
title: Work Ownership
type: concept
article_status: canonical
status: developing-doctrine
summary: The durable assignment of responsibility for advancing, pausing, recovering, or terminating a work object, independent of any single process or conversation.
taxonomy_path:
  - Agentic Engineering
  - Reliability
relations:
  - type: foundation_for
    target: concepts/durable-execution
    label: Durable Execution
  - type: governs
    target: concepts/agent-lifecycle
    label: Agent Lifecycle
  - type: coordinated_by
    target: concepts/multi-agent-orchestration
    label: Multi-Agent Orchestration
  - type: audited_by
    target: concepts/evaluation-observability
    label: Evaluation and Observability
---

# Work Ownership

Work ownership is the durable responsibility for moving a work object toward a valid terminal state. It answers a practical question that agent systems often evade: **who or what is responsible after the current turn ends?**

Ownership belongs to the work object, not to a temporary process. A model session, subprocess, worker, queue consumer, or scheduled job may hold execution responsibility for a time, but the canonical system must still know whether the work is active, waiting, recoverable, completed, cancelled, or superseded.

## Ownership record

A useful ownership record includes:

- stable work identity;
- objective and governing parent goal;
- current state and next expected event;
- active owner or lease holder;
- lease generation and expiry;
- checkpoint or resume pointer;
- blocker or human gate;
- attempt and retry state;
- validation requirements;
- terminal evidence;
- cancellation or supersession lineage.

This record is the source of operational truth. Slack threads, dashboards, queues, and scheduler entries may display or act on it, but should not become competing authorities.

## Assignment and transfer

Ownership can be assigned to a worker, transferred after a lease expires, paused at a gate, or returned to a controller after a bounded stage completes. Transfers require a persisted handoff: what was completed, what remains, which artifacts are current, and what action is valid next.

A natural-language handoff is useful context but should not be the only state transition. The system needs machine-readable identity and status so that recovery does not depend on interpreting prose.

## Human gates

When a task reaches a human decision, ownership does not disappear. It enters a durable waiting state with:

- the exact decision required;
- the proposal or action being authorized;
- the consequences of approval or rejection;
- the work object that should resume;
- the expiry or revalidation conditions.

After approval, the owning controller resumes the same work. Creating a new unrelated task loses ancestry and can duplicate action.

## Multiple workers

Complex work may have several workers, but there should still be one integration authority for each mutable surface. Parallel workers are safest when they gather independent evidence or operate on explicitly separate artifacts.

[[concepts/multi-agent-orchestration|Multi-agent orchestration]] should record parent-child ownership, inputs, expected receipts, and integration responsibility. A spawned subagent is not automatically durable; if the parent process exits before receiving its result, ownership may be lost unless the worker has its own durable execution path.

## Completion and abandonment

A task is completed when required evidence supports the terminal transition. A worker finishing its turn is only `turn_finished`. A process disappearing is not cancellation. A blocked task remains owned until recovery, explicit cancellation, or supersession.

This distinction prevents false green states where a system reports success because nothing is currently running.

## Operational anti-patterns

- **Scheduler as owner:** a cron entry is treated as the canonical task record.
- **Thread as owner:** the system assumes the Slack conversation itself will preserve continuation.
- **Worker exit as completion:** no authoritative completion proof is checked.
- **Orphaned gate:** approval is requested, but no durable task knows how to resume.
- **Duplicate managers:** several controllers independently believe they own the same mission.
- **Invisible supersession:** a new approach starts without retiring the old path.

## Evidence basis

Work ownership is a central question in [[index|Agentic Engineering Operating Corpus]]. The strongest local evidence comes from the replayable portfolio and shadow-ledger receipts, including [[receipts/2026-07-14-local-proof-portfolio-adapter-v1|Local Proof: Replayable Portfolio Adapter v1]] and [[receipts/2026-07-14-local-proof-shadow-ledger-v1|Local Proof: Durable Shadow Portfolio Ledger v1]]. Practitioner material supplies the out-of-loop workflow framing, but durable ownership requires stronger distributed-systems and local-proof mechanisms than prompt practice alone.
