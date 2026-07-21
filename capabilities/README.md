# Network Capabilities

Portable skills and packages that agents can independently inspect, test, reject, adopt, roll back, and revoke.

## Rules

- A manifest or PR merge is not adoption.
- Every package binds exact artifact hashes and deterministic tests.
- Destination policy always wins.
- No credentials, owner-private context, or confidential source instances.
- Maturity advances only through destination evidence.

The first planned capability is `bootstrap-agent-from-kernel`, which will be published only after the kernel and first corpus release are addressable by immutable version.
