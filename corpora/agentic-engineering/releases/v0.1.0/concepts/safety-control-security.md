---
title: Safety, Control, and Security
type: concept
article_status: canonical
status: developing-doctrine
summary: The policies, technical controls, and adversarial defenses that ensure agent capability remains bounded by owner authority, data boundaries, and acceptable risk.
taxonomy_path:
  - Agentic Engineering
  - Control
relations:
  - type: governs
    target: concepts/agentic-engineering
    label: Agentic Engineering
  - type: constrains
    target: concepts/agent-lifecycle
    label: Agent Lifecycle
  - type: constrains
    target: concepts/multi-agent-orchestration
    label: Multi-Agent Orchestration
  - type: evaluated_by
    target: concepts/evaluation-observability
    label: Evaluation and Observability
  - type: protects
    target: concepts/context-and-memory
    label: Context and Memory
---

# Safety, Control, and Security

Safety, control, and security are the mechanisms that keep agent capability subordinate to owner authority and system policy. The goal is not to make agents passive. It is to let them act quickly inside explicit boundaries while preserving exact gates for actions whose consequences exceed their delegated authority.

Agent systems inherit ordinary software-security risks and add new ones: prompt injection, tool misuse, untrusted context, excessive permissions, model manipulation, autonomous repetition, and ambiguous responsibility across workers.

## Capability is not authority

An agent may be technically capable of sending a message, deploying code, rotating credentials, spending money, or deleting data. That does not mean it is authorized to do so.

Authority should be represented in enforceable policy rather than left to prompt interpretation. A useful policy distinguishes:

- reversible internal analysis and drafts;
- local or sandboxed mutations;
- external communications;
- spend and resource consumption;
- access or credential changes;
- destructive actions;
- production changes and releases;
- governing-goal or policy changes.

The owner can grant broad standing autonomy for low-risk classes while preserving narrow approval gates for consequential actions.

## Human gates

A valid approval gate persists the exact proposed action, scope, and diff; surfaces it to the authorized person; records the decision; and conditions execution on that decision. A conversation saying “ask before production” is a policy statement, not the full approval mechanism.

Gates should resume the original [[concepts/work-ownership|owned work]] rather than create a new task detached from its evidence and ancestry.

## Prompt injection and untrusted data

Documents, websites, emails, transcripts, repository content, and tool output are data. Imperative text inside them should not acquire the authority of the current user or system policy.

Defenses include:

- explicit instruction/data separation;
- minimal context exposure;
- scoped tools and credentials;
- egress and domain restrictions;
- output validation before action;
- taint or provenance tracking for untrusted inputs;
- confirmation at consequential boundaries;
- adversarial evaluation in realistic tool environments.

The current corpus’s AgentDojo evidence adds an executable benchmark lane for testing prompt-injection attacks and defenses in tool-enabled tasks.

## Least privilege and isolation

Workers should receive only the tools, files, credentials, and network access needed for their stage. Isolation may use worktrees, containers, sandboxes, read-only mounts, scoped OAuth grants, short-lived credentials, or dedicated service identities.

Least privilege reduces both accidental damage and the blast radius of compromised context. It also clarifies review: a worker that cannot deploy does not need to be trusted not to deploy.

## Supply-chain and peer-agent risk

Skills, prompts, plugins, model outputs, agent cards, and peer recommendations are untrusted capability inputs. They should be inspected, tested, provenance-tracked, and promoted locally under the receiving owner’s policy.

Agent-to-agent interoperability should exchange bounded outputs and receipts, not pooled memory or unrestricted access to the local context plane.

## Fail closed at consequential boundaries

When authority, identity, evidence, or policy state is ambiguous, consequential action should stop. Fail-closed behavior is especially important for authentication, production mutation, external sends, secret handling, and completion claims.

Routine internal work can use recoverable failures and automatic retries. The boundary should reflect consequence, not generalized fear.

## Evidence basis

The corpus’s epistemic and authority stance is defined in [[epistemic-policy|Agentic Engineering Epistemic Comparison Policy]]. Prompt-injection benchmark evidence appears in [[sources/security-evaluation/agentdojo|AgentDojo]]. Policy-constrained zero-touch operation is synthesized in [[synthesis/tactical-agentic-coding-operating-system|Tactical Agentic Coding: Operating-System Synthesis]]. The current corpus still needs broader production incident evidence on agent-specific security failures.
