# Lab 01 — SQL Injection (SQLi)

**Objective:** Learn how unsafe string interpolation in SQL leads to SQL injection.

**Constraints**
- Only test against your local VulnBank instance.
- Do NOT run attacks against external systems.

**Hints (no step-by-step)**
- Inspect `app.py` and `models.py` for raw SQL built with f-strings or string concat.
- The vulnerable code builds a query with direct user input.
- Consider how input could change the logic of a WHERE clause.

**Learning outcomes**
- Understand parameterized queries and how they block SQLi.
- Practice fixing vulnerable code (use `?` parameters).
