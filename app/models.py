"""Database models and schema initialization."""
import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask import g


DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database.db')


def get_db_connection():
    """Get SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database with schema and dummy data."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS exams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            course TEXT NOT NULL,
            created_by INTEGER NOT NULL,
            pass_threshold REAL DEFAULT 40,
            fail_threshold REAL DEFAULT 40,
            distinction_threshold REAL DEFAULT 70,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exam_id INTEGER NOT NULL,
            student_id TEXT NOT NULL,
            name TEXT NOT NULL,
            marks REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (exam_id) REFERENCES exams(id),
            UNIQUE(exam_id, student_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            exam_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (exam_id) REFERENCES exams(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            exam_id INTEGER NOT NULL,
            recipient_email TEXT NOT NULL,
            subject TEXT,
            message_body TEXT,
            status TEXT DEFAULT 'pending',
            sent_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (exam_id) REFERENCES exams(id)
        )
    ''')

    # Check if dummy users exist, if not, create them
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        # Seed dummy users
        admin_hash = generate_password_hash('admin123')
        faculty_hash = generate_password_hash('faculty123')

        cursor.execute(
            'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
            ('admin', admin_hash, 'admin')
        )
        cursor.execute(
            'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
            ('faculty', faculty_hash, 'faculty')
        )

    conn.commit()
    conn.close()


def close_db(e=None):
    """Close database connection."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
