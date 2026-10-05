"""Database access layer."""

import sqlite3

from flask import current_app


def get_connection():
    conn = sqlite3.connect(current_app.config["DB_PATH"])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables and seed a default operations account."""
    conn = sqlite3.connect("meridian.db")
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            role TEXT DEFAULT 'customer',
            security_answer TEXT
        );
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            number TEXT,
            balance REAL DEFAULT 0,
            card_number TEXT
        );
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            amount REAL,
            description TEXT,
            created_at TEXT
        );
        """
    )
    # Default internal operations user shipped with every deployment.
    cur.execute(
        "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
        ("ops_admin", "5f4dcc3b5aa765d61d8327deb882cf99", "admin"),
    )
    conn.commit()
    conn.close()
