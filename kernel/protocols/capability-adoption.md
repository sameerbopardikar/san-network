# Capability Adoption Protocol

- Protocol ID: `san.capability-adoption`
- Version: `0.1.0`
- Authority: kernel normative rule

The lifecycle is:

`discovered -> quarantined -> schema-validated -> provenance-verified -> policy-evaluated -> sandbox-tested -> locally-active -> task-proven -> monitored`

Each destination may reject at any stage. The destination agent remains authoritative over local activation. Network popularity, CodeRabbit review, and source-agent success are evidence, not local authority.

Activation must be atomic, preserve the prior exact pin, and emit a machine-valid adoption receipt. The receipt must identify distinct executor, reviewer, and verifier roles. A failed validation restores the prior pin and records the rejection or rollback result.
