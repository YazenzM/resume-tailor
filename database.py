import sqlite3
from datetime import datetime

DB_NAME = "tracker.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT DEFAULT 'Draft',
            applied_date TEXT,
            resume_path TEXT,
            job_description TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_application(company, role, resume_path, job_desc):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO applications (company, role, status, applied_date, resume_path, job_description)
        VALUES (?, ?, 'Draft', ?, ?, ?)
    """, (company, role, datetime.today().strftime('%Y-%m-%d'), resume_path, job_desc))
    conn.commit()
    conn.close()

def get_applications():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, company, role, status, applied_date, resume_path FROM applications ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_status(app_id, new_status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE applications SET status = ? WHERE id = ?", (new_status, app_id))
    conn.commit()
    conn.close()