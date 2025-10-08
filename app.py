from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory, g
import os
import sqlite3
import hashlib
import pickle  # used for insecure deserialization demo
from config import Config
from db_utils import get_db, close_db
from models import find_user_by_username, get_user, get_accounts_for_user, get_account, get_transactions_for_account

app = Flask(__name__)
app.config.from_object(Config)

# Note: intentionally not setting many security headers to make labs easier
# VULN: Missing security headers
# FIX: Set proper headers (CSP, X-Frame-Options, HSTS) in production.
@app.after_request
def add_headers(response):
    # Intentionally minimal headers; students will add CSP, X-Frame-Options, etc.
    return response

@app.teardown_appcontext
def teardown_db(exception):
    close_db(exception)

def hash_pw(password: str) -> str:
    # VULN: Weak hashing (sha1) for demonstration. FIX: use bcrypt/argon2 and a per-user salt.
    return hashlib.sha1(password.encode()).hexdigest()

@app.route("/")
def index():
    user = None
    if session.get("user_id"):
        user = get_user(session["user_id"])
    return render_template("index.html", user=user)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db = get_db()
        hashed = hash_pw(password)
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
            db.commit()
            flash("Registered! Please log in.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists.")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # VULN: SQLi - unsafe query via string interpolation
        # FIX: Use parameterized queries or ORM to avoid SQL injection
        db = get_db()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{hash_pw(password)}'"
        # VULN: Brute force - no rate limiting or account lockout
        # FIX: Add rate limiting, account lockouts, and monitoring
        cur = db.execute(query)
        user = cur.fetchone()
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["is_admin"] = bool(user["is_admin"])
            flash("Logged in.")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    user_id = session["user_id"]
    accounts = get_accounts_for_user(user_id)
    return render_template("dashboard.html", accounts=accounts)

@app.route("/account/<int:account_id>")
def account_page(account_id):
    # VULN: IDOR - no owner check, any user can view any account if they know the ID
    # FIX: Verify that account.owner_id == session['user_id'] before returning
    account = get_account(account_id)
    if not account:
        flash("Account not found.")
        return redirect(url_for("dashboard"))
    transactions = get_transactions_for_account(account_id)
    return render_template("accounts.html", account=account, transactions=transactions)

@app.route("/transfer", methods=["GET", "POST"])
def transfer():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    db = get_db()
    if request.method == "POST":
        to_account = request.form.get("to_account")
        from_account = request.form.get("from_account")
        amount = float(request.form.get("amount", "0"))
        memo = request.form.get("memo", "")
        # VULN: Insecure transfer (IDOR/business logic) - trusts from_account parameter and doesn't verify ownership
        # FIX: Ensure session user owns from_account and validate amounts/limits and use transactions/locking
        # VULN: CSRF - no CSRF token on this state-changing POST
        # FIX: Add CSRF protection (e.g., WTForms CSRF, flask-wtf)
        # perform naive transfer
        cur = db.execute("SELECT balance FROM accounts WHERE id = ?", (to_account,))
        to_row = cur.fetchone()
        cur = db.execute("SELECT balance FROM accounts WHERE id = ?", (from_account,))
        from_row = cur.fetchone()
        if not to_row or not from_row:
            flash("Invalid accounts.")
            return redirect(url_for("transfer"))
        new_from = from_row["balance"] - amount
        new_to = to_row["balance"] + amount
        db.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_from, from_account))
        db.execute("UPDATE accounts SET balance = ? WHERE id = ?", (new_to, to_account))
        db.execute("INSERT INTO transactions (account_id, amount, memo) VALUES (?, ?, ?)", (to_account, amount, memo))
        db.execute("INSERT INTO transactions (account_id, amount, memo) VALUES (?, ?, ?)", (from_account, -amount, memo))
        db.commit()
        flash("Transfer complete.")
        return redirect(url_for("dashboard"))
    # show user's accounts for selection
    accounts = get_accounts_for_user(session["user_id"])
    return render_template("transfer.html", accounts=accounts)

@app.route("/transactions/<int:account_id>", methods=["GET", "POST"])
def transactions_page(account_id):
    if not session.get("user_id"):
        return redirect(url_for("login"))
    # IDOR: no ownership check
    if request.method == "POST":
        db = get_db()
        amount = float(request.form.get("amount", "0"))
        memo = request.form.get("memo", "")
        # VULN: Stored XSS - memo is saved and later rendered without escaping
        # FIX: Escape output when rendering or sanitize input before saving
        db.execute("INSERT INTO transactions (account_id, amount, memo) VALUES (?, ?, ?)", (account_id, amount, memo))
        db.commit()
        flash("Transaction added.")
        return redirect(url_for("transactions_page", account_id=account_id))
    transactions = get_transactions_for_account(account_id)
    account = get_account(account_id)
    return render_template("transactions.html", transactions=transactions, account=account)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    user = get_user(session["user_id"])
    if request.method == "POST":
        # simple profile update (no file validation)
        flash("Profile updated.")
    return render_template("profile.html", user=user)

@app.route("/upload", methods=["GET", "POST"])
def upload_statement():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    if request.method == "POST":
        f = request.files.get("statement")
        if f:
            # VULN: Insecure file upload - saving without validation and to static uploads
            # FIX: Validate file type, sanitize filename, store outside static, scan for malware
            upload_dir = os.path.join(app.root_path, "static", "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            path = os.path.join(upload_dir, f.filename)
            f.save(path)
            flash("Uploaded.")
            return redirect(url_for("upload_statement"))
    return render_template("upload_statement.html")

@app.route("/goto")
def goto():
    next_url = request.args.get("next", "/")
    # VULN: Open redirect - allows redirecting to arbitrary URLs
    # FIX: Validate `next` to be local or in an allowlist
    return redirect(next_url)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    # Basic admin login check (insecure)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        db = get_db()
        cur = db.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash_pw(password)))
        user = cur.fetchone()
        if user and user["is_admin"]:
            session["user_id"] = user["id"]
            session["is_admin"] = True
            flash("Admin logged in.")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid admin credentials.")
    return render_template("admin.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("is_admin"):
        flash("Admin required.")
        return redirect(url_for("admin"))
    # Admin debugging endpoint: insecure deserialization demonstration
    return render_template("admin.html", admin=True)

@app.route("/admin/deserialize", methods=["POST"])
def admin_deserialize():
    # VULN: Insecure deserialization using pickle. Only for lab and admin pages.
    # FIX: Avoid pickle for untrusted data. Use safe formats like JSON and validate inputs.
    if not session.get("is_admin"):
        flash("Forbidden.")
        return redirect(url_for("admin"))
    data = request.files.get("data")
    if data:
        raw = data.read()
        try:
            obj = pickle.loads(raw)  # VULN: insecure
            flash(f"Deserialized object type: {type(obj)}")
        except Exception as e:
            flash(f"Deserialization error: {e}")
    return redirect(url_for("admin_dashboard"))

# Serve uploaded files (for convenience in lab)
@app.route("/uploads/<path:filename>")
def uploads(filename):
    return send_from_directory(os.path.join(app.root_path, "static", "uploads"), filename)

if __name__ == "__main__":
    app.run(debug=True)
