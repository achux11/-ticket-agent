import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "tickets.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            severity TEXT DEFAULT 'Medium',
            category TEXT,
            status TEXT DEFAULT 'open',
            github_url TEXT,
            github_number INTEGER,
            code_snippet TEXT,
            suggested_fix TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()

def save_ticket(title, description, severity, category, code_snippet, suggested_fix, github_url="", github_number=None):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO tickets (title, description, severity, category, code_snippet, suggested_fix, github_url, github_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, description, severity, category, code_snippet, suggested_fix, github_url, github_number))
    conn.commit()
    ticket_id = c.lastrowid
    conn.close()
    return ticket_id

def get_all_tickets():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM tickets ORDER BY created_at DESC")
    rows = [dict(r) for r in c.fetchall()]
    conn.close()
    return rows

def update_ticket_status(ticket_id, status):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE tickets SET status=? WHERE id=?", (status, ticket_id))
    conn.commit()
    conn.close()

def get_stats():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM tickets")
    total = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tickets WHERE status='open'")
    open_tickets = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tickets WHERE severity='Critical'")
    critical = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM tickets WHERE status='resolved'")
    resolved = c.fetchone()[0]
    conn.close()
    return {"total": total, "open": open_tickets, "critical": critical, "resolved": resolved}
