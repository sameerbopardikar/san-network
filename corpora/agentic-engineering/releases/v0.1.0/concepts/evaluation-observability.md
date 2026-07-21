---
title: Evaluation and Observability
type: concept
article_status: release-synthesis
status: developing-doctrine
summary: The measurement and inspection systems that reveal what agents did, whether the work was correct, how reliably the workflow performs, and when autonomy should expand or contract.
taxonomy_path:
  - Agentic Engineering
  - Quality
relations:
  - type: evaluates
    target: concepts/agentic-engineering
    label: Agentic Engineering
  - type: consumes
    target: concepts/validation-feedback-loops
    label: Validation and Feedback Loops
  - type: observes
    target: concepts/agent-lifecycle
    label: Agent Lifecycle
  - type: audits
    target: concepts/durable-execution
    label: Durable Execution
  - type: informs
    target: concepts/safety-control-security
    label: Safety, Control, and Security
---

# Evaluation and Observability

Observability makes agent behavior inspectable. Evaluation determines whether that behavior is useful, correct, reliable, and safe. Together they replace anecdotal confidence with evidence about how an agentic system performs across repeated work and failure conditions.

Logs alone are not observability, and one successful demo is not evaluation. The system must connect activity to canonical work identity, intended outcome, artifacts, checks, costs, and terminal state.

## Observability model

A useful trace answers:

- Which work object caused this activity?
- Which agent, model, tool, and policy acted?
- What authoritative context and artifact versions were used?
- What material transitions occurred?
- Which external side effects happened?
- What checks ran, against which bytes?
- Why did the system retry, stop, escalate, or complete?

The default human surface should show outcomes and exceptions, not every tool call. Detailed spans remain available for diagnosis.

## Three levels of evidence

### Run-level validation

Did this specific artifact satisfy its acceptance contract? Evidence includes tests, browser checks, reconciliations, citations, review, and exact artifact identity.

### Workflow evaluation

How reliably does the problem-class workflow succeed across a representative set? Measures include acceptance rate, false-green rate, retry count, recovery, duplicate work, cost, latency, and human intervention.

### Outcome evaluation

Did the work create the intended real-world result? A code patch can pass tests yet fail to improve the product. A research brief can be accurate yet fail to change a decision. Outcome evidence is often slower and more domain-specific than technical validation.

These levels should not be collapsed into one “success” field.

## Deterministic and model-based evaluators

Deterministic checks are preferred where a clear invariant exists: schema validity, source integrity, citation resolution, replay convergence, artifact hashes, test results, or budget limits.

Model-based evaluation is useful for intent alignment, synthesis quality, relevance, and nuanced review, but it should use explicit rubrics, preserve evidence, and be calibrated against human judgment or known outcomes. An LLM grading another LLM is not automatically independent.

## Adversarial evaluation

Important systems should be tested under conditions that break ordinary happy-path assumptions:

- interrupted execution between state transitions;
- duplicate and overlapping workers;
- stale leases and stale artifacts;
- malformed or adversarial inputs;
- prompt injection and tool manipulation;
- missing evidence or ambiguous authority;
- retries after partial external side effects;
- validators that can be gamed or rewritten.

The purpose is not theatrical red teaming. It is to discover which claimed guarantees survive realistic failure.

## Autonomy ladder

Autonomy should expand by evidence for a problem class. A useful progression is:

`human in loop → supervised out of loop → policy-constrained unattended → monitored high autonomy`

Promotion depends on consecutive verified successes, low false-green rates, correct approval behavior, restart recovery, and bounded cost. New evidence can reduce autonomy as well as increase it.

## Metrics that matter

- attempts per accepted outcome;
- value or scope per successful run;
- consecutive verified-success streak;
- acceptance-test pass rate;
- false-green rate;
- restart and lease-recovery rate;
- duplicate or overlap rate;
- approval-gate correctness;
- cost and wall time per verified outcome;
- human touchpoints;
- real outcome or decision impact.

Raw token count, tool-call count, and agent count are activity measures, not success measures.

## Evidence basis

Evaluation doctrine is synthesized from Tactical Agentic Coding: Operating-System Synthesis (excluded from this public release candidate and not public verification evidence) and the local proof/evaluation questions in Agentic Engineering Operating Corpus (excluded from this public release candidate and not public verification evidence). Prompt-injection benchmark coverage is represented by AgentDojo (excluded from this public release candidate and not public verification evidence). The self-expanding corpus’s own deterministic evaluation requirements provide an applied example of provenance, freshness, contradiction, retrieval, and lineage checks.
