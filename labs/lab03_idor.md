# Lab 03 — IDOR (Insecure Direct Object Reference)

**Objective:** Find pages that allow accessing resources by predictable IDs without ownership checks.

**Hints**
- Check `account/<id>` and `transactions/<id>` endpoints.
- The server does not check that the logged-in user owns the account.

**Learning outcomes**
- Implement authorization checks to verify resource ownership before access.
