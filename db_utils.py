import sqlite3
from config import Config
from flask import g

def get_db():
    db_path = Config.DATABASE
    db = getattr(g, "_database", None)
    if db is None:
        db = sqlite3.connect(db_path, check_same_thread=False)
        db.row_factory = sqlite3.Row
        g._database = db
    return db

def close_db(e=None):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()
