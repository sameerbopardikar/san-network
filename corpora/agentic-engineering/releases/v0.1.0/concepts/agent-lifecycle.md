---
title: Agent Lifecycle
type: concept
article_status: release-synthesis
status: developing-doctrine
summary: The ordered states and events through which an agent run moves, from admission and context assembly through action, validation, completion, failure, or recovery.
taxonomy_path:
  - Agentic Engineering
  - Foundations
relations:
  - type: part_of
    target: concepts/agentic-engineering
    label: Agentic Engineering
  - type: depends_on
    target: concepts/work-ownership
    label: Work Ownership
  - type: implemented_by
    target: concepts/durable-execution
    label: Durable Execution
  - type: observed_by
    target: concepts/evaluation-observability
    label: Evaluation and Observability
---

# Agent Lifecycle

The agent lifecycle is the sequence of states through which a bounded unit of agent work moves. A lifecycle gives structure to what would otherwise be a loose series of model turns and tool calls. It identifies when work is admitted, who owns it, what context applies, whether action is permitted, how results are checked, and what happens when execution stops unexpectedly.

A lifecycle is not the same as a model session. One work object may span multiple sessions, workers, retries, or providers. Conversely, one session may touch several work objects. The lifecycle belongs to the work.

## Canonical stages

A useful general sequence is:

`admitted → oriented → planned → authorized → executing → validating → reviewing → completed`

Alternative terminal or intermediate states include:

`waiting_gate`, `blocked`, `retryable_failure`, `recovering`, `cancelled`, and `superseded`.

The names matter less than the invariants between them. A task should not enter execution before it has an owner and authority. It should not enter completion before the required evidence exists. A temporary process failure should not erase ownership.

## Admission

Admission converts a request, event, or discovered need into a canonical work object. This step should establish identity, objective, scope, priority, origin, and governing policy. Without admission, duplicate triggers can create overlapping work with no shared identity.

Good admission is selective. Not every message or event deserves a durable mission. The system should distinguish conversation, signal, candidate work, and accepted work.

## Orientation and context assembly

The agent receives the minimum context needed for its stage: relevant files, facts, constraints, tools, prior receipts, and current state. [[concepts/context-and-memory|Context and memory]] are assembled for purpose, not dumped wholesale.

Orientation should make source precedence explicit. A stale summary, an external article, and a direct owner instruction should not enter reasoning as equivalent evidence.

## Authorization

Before action, the lifecycle evaluates authority. Reversible internal work may continue automatically. External sends, spend, access changes, destructive operations, production mutations, or governing-goal changes may enter a durable `waiting_gate` state.

The gate must bind a human decision to the exact proposed action or scope. “The user approves changes” in prompt prose is not an enforceable approval mechanism.

## Execution

Execution may be one focused agent stage or a composition of workers. During this phase the system records attempts, tool actions, checkpoints, and material state changes. [[concepts/work-ownership|Work ownership]] and leases prevent silent abandonment or uncontrolled duplication.

## Validation and review

Validation asks whether the artifact works. Review asks whether it matches intent, scope, policy, and quality. These are related but distinct. A test suite may pass while the wrong feature was built; a thoughtful review may approve intent while missing a runtime defect.

The lifecycle should stop on failed required checks rather than letting downstream stages manufacture a false green. See [[concepts/validation-feedback-loops|Validation and Feedback Loops]].

## Completion

Completion is an evidence-backed state transition, not a final assistant sentence or worker exit. The completion event should identify the artifact, validators, receipts, version or byte identity, and any unresolved caveats.

For consequential work, completion should be reconstructable after restart by a different process. If it depends on the memory of the finishing agent, it is not durable completion.

## Failure and recovery

A lifecycle should distinguish transient execution failure from terminal task failure. A dead process, expired lease, provider timeout, or interrupted browser session can trigger recovery while the work remains owned.

Recovery uses checkpoints and idempotency to resume safely. It must also detect cases where retry would duplicate an external action or apply work against stale state. These mechanisms are covered in [[concepts/durable-execution|Durable Execution]].

## Evidence basis

Lifecycle decomposition is synthesized from the focused-agent and closed-loop practices in Tactical Agentic Coding: Operating-System Synthesis (excluded from this public release candidate and not public verification evidence), the corpus’s active durable-work questions in Agentic Engineering Operating Corpus (excluded from this public release candidate and not public verification evidence), and local proof receipts linked there. The current corpus still needs broader production and scientific evidence on long-horizon lifecycle behavior.
