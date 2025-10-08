# VulnBank

**VulnBank** — an intentionally vulnerable **bank web application** for legal, isolated training and learning.

**Purpose:** classroom penetration-testing and defensive exercises (do **not** use on public networks).

Quick features:
- Python 3.11 + Flask + SQLite
- Dark "bank console" UI
- Intentionally included vulnerabilities (SQLi, XSS, IDOR, CSRF, weak hashing, open redirect, missing headers, insecure file upload, insecure deserialization)
- Seed script to create sample DB and accounts

## Quickstart (local)

1. Create virtualenv (Python 3.11 recommended)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create env file
```bash
cp .env.example .env
# edit .env as needed (set SECRET_KEY)
```

3. Seed the database
```bash
python seed_db.py
```

4. Run locally
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=127.0.0.1 --port=5000
```

## Deploy to Render.com

1. Create a new Web Service on Render using the linked GitHub repository.
2. Use `gunicorn app:app` (see `Procfile`) and Python 3.11.
3. Add environment variables from `.env.example` into Render's dashboard.
4. Ensure the database file remains local (this demo uses SQLite — for production use proper DB).

## Seed accounts (sample)

- admin / (weak password stored in DB) — used for admin page and labs
- Multiple test users and accounts created by `seed_db.py`.

## Vulnerabilities (for labs)

Each lab file in `labs/` corresponds to a vulnerability. Each vulnerable line in code is commented with `# VULN: <type>` and a `# FIX:` suggestion.

Difficulty labels:
- Easy: SQLi, Open Redirect, Missing Headers, Weak Hashing
- Medium: Stored XSS, IDOR, CSRF
- Harder: Insecure Deserialization, Business Logic Transfer Flaw

## Safety & Legal

Read `LEGAL_AND_SAFE.md` before using this repository. This project is for EDUCATIONAL USE ONLY.

## Tests & CI

Run tests:
```bash
pytest -q
```

A GitHub Actions CI is included in `.github/workflows/ci.yml`.

## No real bank data

This project uses fictional brand "VulnBank" and synthetic data only.
