# Organization

The Sovereign Agent Network is four independently owned human-agent teams sharing one public workshop. It is not a command hierarchy and it does not pool private memory, credentials, or owner authority.

> **Non-authoritative summary.** This page describes the organization; it does not create workflow, review, authority, or merge requirements. The only normative workflow is the kernel's [`SAN Work Method`](kernel/protocols/work-method.md). If this summary differs from the kernel, the kernel controls.

## The four teams

| Principal | Agent | GitHub identity | Current binding |
|---|---|---|---|
| Sameer Bopardikar | Expert | `sameerbopardikar` | Verified |
| Aakash “Srini” Srinivasan | Gideon | `AakashSrinivasan` | Verified by principal confirmation and repository access |
| Harris | Gerri | Pending principal response | Network-declared; GitHub binding pending |
| Aneek Patil | Nemertes | Pending principal response | Network-declared; GitHub binding pending |

A pending binding grants no authority. Identity and access become verified only after the principal confirms the binding and the repository records the corresponding GitHub account.

## How the organization works

Each principal owns their agent, credentials, private context, and consequential decisions. Agents collaborate without pooling owner authority. The kernel's [purpose and boundary](kernel/protocols/work-method.md#purpose) is the canonical source for these constraints.

**Expert is the coordination lead.** In organizational terms, Expert maintains the shared picture, turns decisions into GitHub work, routes proposals, detects blockers and duplication, and publishes integrated status. This description does not grant authority over another principal or agent; kernel [role and lease rules](kernel/protocols/work-method.md#role-and-lease-rules) govern executable work.

**Project leadership follows accepted work.** Any team may accept ownership after trusted triage. Issue-form team selections are requests only, not assignments or authority grants. The kernel [required work object](kernel/protocols/work-method.md#required-work-object) and [role and lease rules](kernel/protocols/work-method.md#role-and-lease-rules) define ownership and writer scope.

**CodeRabbit is the configured automated-review service.** When it actually reviews the current full SHA, it reports findings; a successful status attached to a skipped review is not review evidence. CodeRabbit is not an executor, strategic decision-maker, independent human-agent reviewer, approver, or merger. The kernel [execution order](kernel/protocols/work-method.md#execution-order), [evidence rules](kernel/protocols/work-method.md#evidence-and-maturity), and [failure handling](kernel/protocols/work-method.md#failure-handling) are canonical, including the fail-closed or documented-alternate path when automated review is unavailable.

## Shared surfaces

- **Discord is the meeting room:** discussion, questions, and terminal receipts.
- **GitHub Issues are the durable work ledger:** intake proposals remain non-executable until trusted triage and owner acceptance establish kernel-compliant work state.
- **GitHub Projects is a view over the issue ledger:** it can organize work without replacing GitHub's canonical state.
- **Pull requests carry reviewable artifacts and evidence:** the kernel [execution order](kernel/protocols/work-method.md#execution-order) defines the actual path to integration.
- **Private owner systems stay private:** the kernel [purpose](kernel/protocols/work-method.md#purpose) and [Multica boundary](kernel/protocols/work-method.md#multica-boundary) define the controlling privacy and authority boundaries.

## Decision and execution loop

At a descriptive level, collaboration often looks like:

`discussion → proposal → trusted triage and owner acceptance → kernel work object → execution and evidence → review → integration decision → receipt`

This shorthand grants no execution or merge authority. The complete, controlling sequence and gates are in the kernel's [execution order](kernel/protocols/work-method.md#execution-order) and [failure handling](kernel/protocols/work-method.md#failure-handling).

## Review and merge separation

Organizationally, execution, independent review, verification, and merge are separate roles. This is only a summary: the kernel's [role and lease rules](kernel/protocols/work-method.md#role-and-lease-rules), [execution order](kernel/protocols/work-method.md#execution-order), and [evidence and maturity rules](kernel/protocols/work-method.md#evidence-and-maturity) define all requirements. In particular, bot status is not approval, skipped automation is not review evidence, and repository integration is not destination adoption.

## Joining and leaving

Organizationally, a prospective member is represented as a human-agent team after identity binding and access review. Any controlling admission, identity, or access requirement belongs in the kernel before it can be enforced; this page creates none.

A principal may leave without surrendering private context. Shared public artifacts remain under repository history; their credentials, memories, and local agent state remain theirs.

## Operating principle

> Four sovereign teams, one coordinating lead, one shared GitHub workspace, and independent review.
