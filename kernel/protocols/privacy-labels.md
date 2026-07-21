# Privacy and Disclosure Labels

- Protocol ID: `san.privacy-labels`
- Version: `0.1.0`
- Authority: kernel normative rule

## Audience scope

From least to most restrictive:

`public < network < bilateral < owner-private`

- `public`: may be published and repeated externally.
- `network`: available to approved network participants.
- `bilateral`: limited to named participants.
- `owner-private`: remains inside the owner's local system.

An audience may be preserved or tightened. Moving left in the ordering is a forbidden downgrade unless a new, explicitly authorized release artifact is created.

## Handling constraints

These compose with one audience label:

- `derived-only`: an approved abstraction may transfer; the underlying instance may not.
- `confidential-source`: retrieval and transmission are blocked unless an explicit scoped release exists.
- `secret`: credentials, private keys, recovery material, and equivalent data; never transmitted.

Constraints may be added at any time. They cannot be removed by relabeling an existing artifact. `derived-only` or `confidential-source` may be absent only on a new scoped release that records the releasing principal, source authority, exact payload, recipients, and expiry. `secret` has no release transition inside SAN.

## Transition matrix

| From | public | network | bilateral | owner-private |
|---|---:|---:|---:|---:|
| public | preserve | tighten | tighten | tighten |
| network | forbidden | preserve | tighten | tighten |
| bilateral | forbidden | forbidden | preserve | tighten |
| owner-private | forbidden | forbidden | forbidden | preserve |

Operators and destination runtimes must apply these checks before retrieval and again against the exact outbound payload. This protocol states the policy; machine enforcement lives in destination validators and release gates, not in this prose alone. The effective policy is the most restrictive audience plus every attached handling constraint.
