# Lab 04 — Insecure Transfer / Business Logic Flaw

**Objective:** Identify the transfer endpoint that trusts the `from_account` parameter.

**Hints**
- The form accepts `from_account` and `to_account`.
- There's no verification that the user owns `from_account`.

**Learning outcomes**
- Enforce business logic checks and server-side validation for transfers.
