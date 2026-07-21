# Network Capabilities

This plane contains portable capability definitions. Inspection and local tests are always allowed. Adoption, destination compilation, rollback, and revocation require destination-local authority, sandboxed execution, conformance evidence, and receipts.

Normative network rules do not live here. They are defined by:

- `kernel/protocols/capability-adoption.md`;
- `kernel/protocols/promotion-and-rollback.md`; and
- `kernel/schemas/capability-manifest.schema.json`.

The first planned capability is `bootstrap-agent-from-kernel`. It remains a draft until its exact pins, deterministic tests, destination verification, and release receipt satisfy the kernel contracts.
