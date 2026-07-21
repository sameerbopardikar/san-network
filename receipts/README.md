# Receipts Plane

`receipts/` contains minimized machine-readable proof of adoption, rejection, promotion, demotion, and rollback events.

It does not contain doctrine, private memories, raw confidential traces, credentials, or reusable capabilities. Normative requirements live in `kernel/protocols/` and `kernel/schemas/`.

Every operational receipt outside `fixtures/` must:

- validate against `kernel/schemas/adoption-receipt.schema.json`;
- name an immutable subject pin and benchmark version;
- identify pairwise-distinct executor, reviewer, and verifier agents;
- include evidence pointers rather than raw private evidence;
- record prior, candidate, resulting, and rollback pins explicitly; and
- pass `python receipts/scripts/validate_receipts.py`.

`fixtures/valid/` and `fixtures/invalid/` are conformance examples only. They are not claims of real network adoption or promotion.
