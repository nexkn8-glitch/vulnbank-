# Legal & Safety Policy — VulnBank

**IMPORTANT — READ BEFORE USING**

1. **Purpose & Authorization**
   - VulnBank is provided strictly for **legal, educational, and isolated lab use** (training, CTFs, classroom exercises).
   - You must **only** run this application on systems and networks you own or control (e.g., local VM, offline lab network).
   - Do **not** deploy to a public-facing production environment. Do **not** target other networks or services.

2. **Environment**
   - Use an isolated VM, container, or sandbox with no unintended internet exposure (recommended: local VM with NAT disabled or private network).
   - Remove or secure this app before exposing to any external network.

3. **Prohibited Actions**
   - Do not use this repository to attack or attempt to break into systems you do not own or without explicit written permission.
   - Do not distribute exploit payloads, attack scripts, or step-by-step exploit instructions derived from this repo.

4. **Data & Privacy**
   - This repository uses synthetic fictional data only. Do not insert real PII or production data into this lab.
   - To reset data, run `python seed_db.py` and clear `static/uploads/`.

5. **Insecure Components**
   - The app intentionally contains insecure code to teach vulnerabilities. Never copy insecure practices into production code.

6. **Reset & Cleanup**
   - To reset the environment:
     - Delete `vulnbank.db`
     - Remove files under `static/uploads/`
     - Run `python seed_db.py`

7. **Liability**
   - The authors provide this code *as-is* for education. Use at your own risk. You are responsible for complying with local laws and institutional policies.

If you are unsure whether your intended use is permitted, stop and consult your instructor, manager, or legal advisor.
