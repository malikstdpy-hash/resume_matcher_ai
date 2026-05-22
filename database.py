import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "resume_matcher.db")

def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume_id INTEGER,
            job_id INTEGER,
            score INTEGER,
            feedback TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (resume_id) REFERENCES resumes(id),
            FOREIGN KEY (job_id) REFERENCES jobs(id)
        )
    """)

    conn.commit()
    conn.close()

def save_resume(name, content):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO resumes (name, content) VALUES (?, ?)", (name, content))
    conn.commit()
    resume_id = cursor.lastrowid
    conn.close()
    return resume_id

def save_job(title, description):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs (title, description) VALUES (?, ?)", (title, description))
    conn.commit()
    job_id = cursor.lastrowid
    conn.close()
    return job_id

def save_match(resume_id, job_id, score, feedback):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO matches (resume_id, job_id, score, feedback)
        VALUES (?, ?, ?, ?)
    """, (resume_id, job_id, score, feedback))
    conn.commit()
    conn.close()

def get_all_matches():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT m.id, r.name, j.title, m.score, m.feedback, m.created_at
            FROM matches m
            JOIN resumes r ON m.resume_id = r.id
            JOIN jobs j ON m.job_id = j.id
            ORDER BY m.created_at DESC
        """)
        results = cursor.fetchall()
    except Exception as e:
        results = []
        print(f"DB Error: {e}")
    finally:
        conn.close()
    return results