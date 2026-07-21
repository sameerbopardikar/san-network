# Network Kernel

The shared law and compatibility layer for the four-agent Sovereign Agent Network.

## Separation of planes

- **Kernel:** rules, schemas, conformance, and the Agent Bootstrap Engine interface.
- **Capabilities:** reusable actions an agent may independently evaluate and adopt.
- **Corpora:** evidence releases with provenance, rights, and retrieval tests.

The kernel never pools owner memory, distributes credentials, or grants another agent authority over a destination runtime.

## V0 finish line

1. Every participant can publish a valid Agent Card.
2. Every cross-agent task has one work contract, one executor, one independent reviewer, one independent verifier, and explicit acceptance evidence. Executor, reviewer, and verifier must be pairwise distinct.
3. Capabilities and corpora use versioned manifests.
4. The destination agent retains adoption, disclosure, rollback, and revocation authority.
5. The current Agent Bootstrap Engine is migrated only after its private assumptions and generated state are separated from the portable engine.

Run `python scripts/validate.py` and `python -m unittest discover -s tests -v`.
