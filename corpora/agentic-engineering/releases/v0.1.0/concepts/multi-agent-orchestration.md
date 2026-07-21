---
title: Multi-Agent Orchestration
type: concept
article_status: release-synthesis
status: developing-doctrine
summary: The decomposition, coordination, and integration of multiple focused agents or workers under explicit context, ownership, authority, and validation contracts.
taxonomy_path:
  - Agentic Engineering
  - Coordination
relations:
  - type: enabled_by
    target: concepts/agentic-layer
    label: Agentic Layer
  - type: depends_on
    target: concepts/work-ownership
    label: Work Ownership
  - type: uses
    target: concepts/context-and-memory
    label: Context and Memory
  - type: constrained_by
    target: concepts/safety-control-security
    label: Safety, Control, and Security
  - type: validated_by
    target: concepts/validation-feedback-loops
    label: Validation and Feedback Loops
---

# Multi-Agent Orchestration

Multi-agent orchestration is the coordination of several agent stages or workers toward one objective. Its value comes from decomposition, specialization, independent perspective, and parallelism. Its risks come from fragmented context, overlapping authority, duplicated work, integration failure, and the illusion that more agents imply more intelligence.

The default should not be “use many agents.” It should be **one agent, one prompt, one purpose**, adding workers only when the work has separable epistemic or execution roles.

## Good reasons to use multiple agents

- Independent research branches can run in parallel.
- Implementation and review benefit from different contexts and incentives.
- Large homogeneous workloads can be sharded with a common contract.
- Specialized tools or domains require focused workers.
- A planner, executor, and validator need different information.
- Adversarial critique is valuable enough to justify an independent pass.

A single coherent agent is often better when the task depends on hidden continuity, requires frequent shared design decisions, or would make several workers mutate the same surface.

## Decomposition by purpose

The cleanest decomposition follows epistemic purpose rather than arbitrary file counts. Common roles include:

`route → plan → execute → validate → review → integrate`

Each role receives only the context it needs. A reviewer should see the governing objective and the artifact, but not necessarily the implementer’s entire reasoning trace. Fresh context can reduce anchoring and confirmation bias.

## Parent-child ownership

Every worker should have:

- a parent work identity;
- one bounded objective;
- explicit inputs and source pointers;
- allowed tools and mutations;
- forbidden actions and human gates;
- required output and evidence;
- stop conditions;
- an integration owner.

A spawned subagent is often process-local. If the parent exits before receiving the result, the work may vanish. Long-running or restart-sensitive workers need their own [[concepts/durable-execution|durable execution]] path rather than a handle stored in prose.

## Single-writer integration

Parallelize intelligence more readily than writes. Several workers can inspect, research, critique, or test independently. Mutations to one codebase, document, ledger, or deployment should usually have one integration authority unless boundaries are mechanically separate.

This prevents two individually reasonable agents from creating an incoherent combined state.

## Communication and context

Agent communication should use typed artifacts and receipts rather than unbounded conversation where possible. Plans, findings, diffs, tests, and source pointers are easier to validate and replay than informal agent chatter.

The orchestrator compiles the next worker’s context from authoritative state. Workers should not query each other’s raw memory as a substitute for proper handoff.

## Review and disagreement

Independent agents are useful when disagreement is preserved rather than averaged away. A critic should identify concrete findings with evidence, severity, and acceptance tests. The integrator decides what to adopt and records dismissals or remaining uncertainty.

For repeated AI review loops, useful findings should become a stable ledger. Otherwise each pass may generate a different set of plausible comments and create endless churn.

## Metrics

Useful orchestration metrics include:

- accepted work per attempt;
- duplicate or overlapping work rate;
- integration failure rate;
- context size per worker;
- review finding precision;
- restart recovery rate;
- human touchpoints;
- cost and wall time per verified outcome.

Agent count is not a success metric.

## Evidence basis

This article is network-authored doctrine. Public corroboration is limited to the pinned Hermes Agent and tau2-bench source card(s) listed by stable source_id in the release manifest for this artifact (hermes-agent, tau2-bench). Excluded private or local material is not public verification evidence.
