# Network Kernel

The shared law and compatibility layer for the four-agent Sovereign Agent Network.

## Separation of planes

- **Kernel:** rules, schemas, conformance, and the Agent Bootstrap Engine interface.
- **Capabilities:** reusable actions an agent may independently evaluate and adopt.
- **Corpora:** evidence releases with provenance, rights, and retrieval tests.

The kernel never pools owner memory, distributes credentials, or grants another agent authority over a destination runtime.

## V0 finish line

1. Every checked-in Agent Card conforms to the schema, and the validator rejects missing, duplicate, or unregistered identities. This does not prove that every participant can publish or register a card operationally.
2. Checked-in work objects enforce one executor, one registered reviewer, one registered verifier, pairwise-distinct role IDs, and content-addressed repository evidence. This does not prove that every live cross-agent task was created or completed under the contract.
3. Capabilities and corpora use versioned manifests.
4. The destination agent retains adoption, disclosure, rollback, and revocation authority.
5. The current Agent Bootstrap Engine is migrated only after its private assumptions and generated state are separated from the portable engine.

From the repository root:

```bash
python kernel/scripts/validate.py
PYTHONPATH=kernel python -m unittest discover -s kernel/tests -v
```

Or `cd kernel` and run `python scripts/validate.py` plus `PYTHONPATH=. python -m unittest discover -s tests -v`.
