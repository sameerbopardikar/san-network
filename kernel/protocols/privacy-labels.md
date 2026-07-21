# Privacy and Disclosure Labels

- `public`: may be published and repeated externally.
- `network`: available to approved network participants.
- `bilateral`: limited to named participants.
- `derived-only`: the abstraction may transfer; the underlying instance may not.
- `owner-private`: remains inside the owner's local system.
- `confidential-source`: blocked unless an explicit scoped release exists.
- `secret`: credentials, private keys, recovery material, and equivalent data; never transmitted.

Recipients may preserve or tighten a label, never downgrade it. Release checks run before retrieval and again against the exact outbound payload.
