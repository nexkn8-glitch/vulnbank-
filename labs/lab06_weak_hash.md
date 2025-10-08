# Lab 06 — Weak Password Hashing

**Objective:** See insecure password storage and migrate to secure hashes.

**Hints**
- Check `seed_db.py` and `app.py` `hash_pw()` — it uses SHA-1 or similar.
- Research bcrypt or argon2 and per-user salt.

**Learning outcomes**
- Migrate to `bcrypt`/`argon2`, add pepper/salt, and add password policy enforcement.
