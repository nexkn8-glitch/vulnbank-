"""
Seed the SQLite database with fictional users, accounts, and transactions.
No real PII.
"""
import sqlite3
import os
import hashlib
from config import Config

DB = Config.DATABASE

def weak_hash(password: str) -> str:
    # VULN: Weak hashing (SHA-1). FIX: use bcrypt/argon2 with salt.
    return hashlib.sha1(password.encode()).hexdigest()

if os.path.exists(DB):
    os.remove(DB)

conn = sqlite3.connect(DB)
c = conn.cursor()

c.executescript("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    is_admin INTEGER DEFAULT 0
);

CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INTEGER,
    name TEXT,
    balance REAL,
    FOREIGN KEY(owner_id) REFERENCES users(id)
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    amount REAL,
    memo TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(account_id) REFERENCES accounts(id)
);
""")

# Seed users (fictional)
users = [
    ("alice", weak_hash("password123")),  # VULN: weak password hash
    ("bob", weak_hash("hunter2")),
    ("admin", weak_hash("adminpass"))  # admin account for lab
]

c.executemany("INSERT INTO users (username, password) VALUES (?, ?)", users)

# Get user ids
c.execute("SELECT id, username FROM users")
rows = c.fetchall()
uids = {r[1]: r[0] for r in rows}

# Seed accounts
accounts = [
    (uids["alice"], "Checking - 1001", 1500.00),
    (uids["alice"], "Savings - 2001", 5000.00),
    (uids["bob"], "Checking - 3001", 300.00),
    (uids["admin"], "Admin Ledger", 10000.00)
]
c.executemany("INSERT INTO accounts (owner_id, name, balance) VALUES (?, ?, ?)", accounts)

# Get account ids
c.execute("SELECT id, owner_id FROM accounts")
accs = c.fetchall()
acc_map = { (r[1], idx): r[0] for idx, r in enumerate(accs) }

# Seed transactions (memo may later be exploited for stored XSS)
transactions = [
    (1, -50.0, "Coffee"),
    (1, 200.0, "Paycheck"),
    (2, -100.0, "Rent"),
    (3, -25.0, "Books")
]
c.executemany("INSERT INTO transactions (account_id, amount, memo) VALUES (?, ?, ?)", transactions)

conn.commit()
conn.close()
print("Seeded database at", DB)
