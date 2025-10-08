import os
import tempfile
import pytest
from app import app
from config import Config

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)
    os.environ["DATABASE"] = db_path
    # seed a minimal DB for tests
    from seed_db import seed_db  # not present as function, but we ensure db exists by running seed_db.py
    # run the seed script to create DB
    import subprocess, sys
    subprocess.run([sys.executable, "seed_db.py"], check=True)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
    try:
        os.remove(db_path)
    except OSError:
        pass

def test_index(client):
    rv = client.get("/")
    assert b"VulnBank" in rv.data

def test_register_page(client):
    rv = client.get("/register")
    assert rv.status_code == 200
