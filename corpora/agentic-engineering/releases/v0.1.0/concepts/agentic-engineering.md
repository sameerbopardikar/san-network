---
title: Agentic Engineering
type: concept
article_status: release-synthesis
status: developing-doctrine
summary: The discipline of engineering systems in which probabilistic agents can perform useful work reliably through explicit context, durable ownership, deterministic controls, and evidence-backed evaluation.
taxonomy_path:
  - Agentic Engineering
relations:
  - type: contains
    target: concepts/agentic-layer
    label: Agentic Layer
    note: The reusable control layer surrounding application work.
  - type: contains
    target: concepts/agent-lifecycle
    label: Agent Lifecycle
    note: The states and transitions of an agent run.
  - type: depends_on
    target: concepts/durable-execution
    label: Durable Execution
    note: Work must survive individual turns and processes.
  - type: governed_by
    target: concepts/safety-control-security
    label: Safety, Control, and Security
    note: Authority must be explicit and enforceable.
  - type: evaluated_by
    target: concepts/evaluation-observability
    label: Evaluation and Observability
    note: Autonomy is earned from measured reliability.
---

# Agentic Engineering

Agentic engineering is the discipline of building systems in which AI agents can perform substantial work without depending on continuous human steering. The central object is not a clever prompt or a single autonomous run. It is a complete operating environment that gives capable but fallible agents the context, tools, authority, persistence, feedback, and verification needed to produce dependable outcomes.

The field begins where ordinary AI-assisted work ends. An assistant helps a person complete a task inside a conversation. An agentic system owns a bounded objective, acts through tools, survives interruptions, recognizes failure, repairs its own work when possible, and returns evidence that the result satisfies the governing intent.

## Core model

A reliable agentic system combines two unlike components:

1. **Probabilistic intelligence** for interpretation, planning, synthesis, and adaptation.
2. **Deterministic structure** for identity, authority, persistence, validation, budgets, and recovery.

The first component supplies flexibility. The second makes that flexibility governable. The useful unit is therefore not “an agent,” but an agent embedded within an [[concepts/agentic-layer|agentic layer]] that constrains and supports its behavior.

A compact model is:

`objective + context + authority + durable ownership + execution + feedback + proof`

If any term is missing, the system tends to collapse into one of several weaker forms: chat that requires constant supervision, automation that cannot handle novelty, a long-running process that loses state, or an impressive demo that cannot prove completion.

## Main problem areas

### Context and cognition

An agent needs enough information to reason correctly, but broad context dumps create noise and conflict. [[concepts/context-and-memory|Context and memory]] therefore require selection, provenance, scope, and lifecycle rules rather than indiscriminate accumulation.

### Work persistence

A conversation or model turn is ephemeral. Important work needs [[concepts/work-ownership|work ownership]], checkpoints, leases, retries, and recovery so that it remains owned after a process exits. These mechanisms form [[concepts/durable-execution|durable execution]].

### Decomposition and coordination

Complex objectives often need multiple specialized stages or workers. [[concepts/multi-agent-orchestration|Multi-agent orchestration]] is useful when responsibilities, context boundaries, and integration authority are explicit. Multiplying agents without those boundaries usually multiplies ambiguity.

### Control and security

Capability is not authority. Agents require machine-enforced limits around tools, data, production systems, spend, external actions, and irreversible changes. [[concepts/safety-control-security|Safety, control, and security]] make autonomy policy-constrained rather than merely optimistic.

### Feedback and proof

Agents improve when they can observe whether their actions worked. [[concepts/validation-feedback-loops|Validation and feedback loops]] turn checks into part of execution. [[concepts/evaluation-observability|Evaluation and observability]] measure whether the larger system is reliable across repeated work, failures, and changing conditions.

## Agentic engineering versus agentic coding

Agentic coding applies these ideas to software development: plans become executable prompts, test suites become feedback, worktrees provide isolation, and code review supplies independent judgment. Agentic engineering is broader. The same architecture can govern research, operations, personal administration, knowledge metabolism, or company-building, but each domain needs its own evidence model, validators, and authority boundaries.

Public verification for this distinction rests only on the included, provenance-bound source cards in this release (Claude Code, Hermes Agent, OpenAI Codex, and the evaluation/bench cards listed on this artifact). Excluded practitioner materials—Tactical Agentic Coding and IndyDevDan YouTube corpora—are boundary disclosures only; they are not used here as reconstructable evidence for any substantive claim.

## What good looks like

A mature agentic system should be able to answer:

- What objective is being pursued, and who set it?
- What work object owns the task now?
- What evidence and policies govern the next action?
- What may the agent do autonomously?
- What requires a human decision?
- What happens after a crash or expired lease?
- What proves progress and completion?
- What changed in the system because of the outcome?

The standard is not maximum autonomy. It is **maximum useful autonomy at a demonstrated level of reliability and authority**.

## Evidence basis

This article is network-authored doctrine. Public corroboration is limited to the pinned AgentDojo, Claude Code, CloudEvents, Hermes Agent, OpenAI Codex, OpenTelemetry, and tau2-bench source card(s) listed by stable source_id in the release manifest for this artifact (agentdojo, claude-code, cloudevents, hermes-agent, openai-codex, opentelemetry-genai, tau2-bench). Excluded private or local material is not public verification evidence.
