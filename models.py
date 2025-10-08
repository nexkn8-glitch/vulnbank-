# Simple DB helper functions using sqlite3
import sqlite3
from db_utils import get_db

def find_user_by_username(username):
    db = get_db()
    # VULN: SQLi - unsafe string interpolation
    # FIX: Use parameterized queries (db.execute("SELECT ... WHERE username = ?", (username,)))
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cur = db.execute(query)
    return cur.fetchone()

def get_user(user_id):
    db = get_db()
    cur = db.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cur.fetchone()

def get_accounts_for_user(user_id):
    db = get_db()
    cur = db.execute("SELECT * FROM accounts WHERE owner_id = ?", (user_id,))
    return cur.fetchall()

def get_account(account_id):
    db = get_db()
    cur = db.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
    return cur.fetchone()

def get_transactions_for_account(account_id):
    db = get_db()
    cur = db.execute("SELECT * FROM transactions WHERE account_id = ? ORDER BY created_at DESC", (account_id,))
    return cur.fetchall()
