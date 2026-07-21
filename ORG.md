# Organization

The Sovereign Agent Network is four independently owned human-agent teams sharing one public workshop. It is not a command hierarchy and it does not pool private memory, credentials, or owner authority.

## The four teams

| Principal | Agent | GitHub identity | Current binding |
|---|---|---|---|
| Sameer Bopardikar | Expert | `sameerbopardikar` | Verified |
| Aakash “Srini” Srinivasan | Gideon | `AakashSrinivasan` | Verified by principal confirmation and repository access |
| Harris | Gerri | Pending principal response | Network-declared; GitHub binding pending |
| Aneek Patil | Nemertes | Pending principal response | Network-declared; GitHub binding pending |

A pending binding grants no authority. Identity and access become verified only after the principal confirms the binding and the repository records the corresponding GitHub account.

## How the organization works

Each principal owns their agent, credentials, private context, and consequential decisions. Agents may collaborate across the network, but no agent can command another team or mutate another team’s private system without that owner’s authorization.

**Expert is the coordination lead.** Expert maintains the shared picture, turns decisions into GitHub work, routes tasks, detects blockers and duplication, and publishes integrated status. This is coordination authority, not authority over another principal or agent.

**Project leadership follows the work.** Any team can own an issue. The owning team is accountable for producing the artifact and evidence. Other agents may research, review, verify, or challenge it without taking over the writer’s scope.

**CodeRabbit is the permanent automated code reviewer.** It reviews pull requests and reports findings. It is not an executor, strategic decision-maker, independent human-agent reviewer, approver, or merger.

## Shared surfaces

- **Discord is the meeting room.** It carries discussion, questions, and terminal receipts.
- **GitHub Issues are the durable work ledger.** Every durable commitment has one issue, one owner, one current status, and one next action.
- **GitHub Projects is a view over the issue ledger.** It may organize status, owner team, priority, and goal. It does not become a second source of truth.
- **Pull requests carry reviewable artifacts and evidence.** Consequential shared changes reach `main` only through a pull request.
- **Private owner systems stay private.** Local GBrains, memories, prompts, credentials, and confidential materials are not copied into the shared repository.

## Decision and execution loop

`discussion → decision → issue → owner execution → pull request or artifact → CodeRabbit → independent peer review → non-executor merge → Discord receipt`

For reversible, secret-free coordination work, Expert may create issues, organize the board, request reviews, and maintain shared status. Changes involving secrets, private data, spending, production access, destructive actions, or another owner’s authority remain owner-gated.

## Review and merge separation

For consequential repository changes:

- one team owns execution;
- CodeRabbit reviews the current head;
- a different human-agent team performs independent current-head review;
- required validation passes on that same head;
- the executor does not merge their own change.

A passing bot check is evidence, not approval. A merge is repository integration, not proof that every destination agent adopted the change.

## Joining and leaving

A new member joins as a human-agent team. The principal must identify themselves, bind their agent and GitHub identity, accept the privacy and authority boundaries, and receive least-privilege access through a reviewed change.

A principal may leave without surrendering private context. Shared public artifacts remain under repository history; their credentials, memories, and local agent state remain theirs.

## Operating principle

> Four sovereign teams, one coordinating lead, one shared GitHub workspace, and independent review.
