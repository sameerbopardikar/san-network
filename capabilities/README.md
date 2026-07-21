# Network Capabilities

This plane contains portable skills and packages that agents can independently inspect, test, reject, adopt, roll back, and revoke.

Normative network rules do not live here. They are defined by:

- `kernel/protocols/capability-adoption.md`;
- `kernel/protocols/promotion-and-rollback.md`; and
- `kernel/schemas/capability-manifest.schema.json`.

The first planned capability is `bootstrap-agent-from-kernel`. It remains a draft until its exact pins, deterministic tests, destination verification, and release receipt satisfy the kernel contracts.
