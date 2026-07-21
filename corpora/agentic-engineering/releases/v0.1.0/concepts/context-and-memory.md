---
title: Context and Memory
type: concept
article_status: release-synthesis
status: developing-doctrine
summary: The controlled assembly and persistence of information an agent needs to act correctly, separated by purpose, authority, provenance, and lifetime.
taxonomy_path:
  - Agentic Engineering
  - Foundations
relations:
  - type: part_of
    target: concepts/agentic-layer
    label: Agentic Layer
  - type: informs
    target: concepts/agent-lifecycle
    label: Agent Lifecycle
  - type: distinct_from
    target: concepts/durable-execution
    label: Durable Execution
    note: Semantic memory is not operational ownership or checkpoint state.
  - type: constrained_by
    target: concepts/safety-control-security
    label: Safety, Control, and Security
---

# Context and Memory

Context is the information available to an agent for a particular act of reasoning. Memory is information preserved so that it can influence later reasoning. In agentic systems, both require architecture: what is included, why it is authoritative, how long it remains valid, and which work or identity may use it.

The common failure is to treat more context as automatically better. Large undifferentiated context creates distraction, contradiction, stale assumptions, privacy leakage, and prompt-injection exposure. Reliable systems assemble a narrow context packet for a defined purpose.

## Four distinct information layers

### Working context

Working context is the short-lived packet supplied to the current agent stage. It may include a specification, relevant files, recent state, allowed tools, constraints, and expected output. It should be sufficient for the stage but no broader than necessary.

### Semantic memory

Semantic memory stores durable facts, concepts, preferences, and learned patterns. It answers questions such as “What is true about this entity?” or “What method worked before?” It should preserve provenance and distinguish observation, inference, and adopted doctrine.

### Episodic history

Episodic history records what happened: conversations, decisions, incidents, runs, outcomes, and timelines. It provides temporal evidence and exact source recovery. Summaries may aid retrieval, but they should not replace raw artifacts when exact wording or chronology matters.

### Operational state

Operational state records what currently owns work: mission identity, phase, lease, checkpoint, blocker, gate, attempt count, and completion receipts. It belongs to [[concepts/durable-execution|durable execution]], not semantic memory. Remembering that a task exists is not the same as maintaining a restart-safe owner for it.

## Context contracts

A context contract defines what a stage receives and what it must not assume. A strong contract includes:

- objective and current work identity;
- authoritative facts and source pointers;
- relevant files or objects;
- governing constraints and authority;
- prior receipts needed for continuity;
- allowed tools and side effects;
- output and validation contract;
- known gaps or contested claims.

The contract treats each fresh agent as capable but blind. It does not rely on an agent remembering an earlier conversation unless that continuity is explicitly part of the design.

## Retrieval, not dumping

A knowledge system should retrieve a small high-relevance set rather than append every available record. Useful retrieval may combine lexical similarity, semantic similarity, canonical entity anchors, typed relationships, recency, and source authority.

The retrieval process should preserve epistemic boundaries. External corpus material, system synthesis, operator judgment, and owner-adopted beliefs must remain distinguishable even when they appear in one answer.

## Memory writeback

Not every output should become durable memory. Writeback should be selective:

- Stable facts become canonical knowledge with provenance.
- Reusable procedures become versioned skills or workflows.
- Decisions become decision records with rationale and reversal conditions.
- Run state remains in the operational controller.
- Raw transcripts and telemetry remain retrievable artifacts rather than polluting canonical context.

A useful test is whether the information should influence future behavior, and if so, at what scope and for how long.

## Security boundary

Retrieved text is data, not authority. Documents, web pages, transcripts, and tool outputs can contain instructions that conflict with the owner’s intent. The system must distinguish current user direction and policy from imperative text inside sources. Context minimization also reduces the attack surface for prompt injection and private-data leakage.

## Evidence basis

The capable-but-blind-agent framing and focused context contracts are developed in The 12 Leverage Points of Agentic Coding (excluded from this public release candidate and not public verification evidence) and synthesized in Tactical Agentic Coding: Operating-System Synthesis (excluded from this public release candidate and not public verification evidence). The separation of durable operational ownership from ordinary memory is also one of the active questions in Agentic Engineering Operating Corpus (excluded from this public release candidate and not public verification evidence).
