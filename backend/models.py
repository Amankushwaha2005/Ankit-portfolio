import sqlite3
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from config import DATABASE_PATH, UPLOAD_FOLDER, ALLOWED_EXTENSIONS


def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            position TEXT NOT NULL,
            experience TEXT,
            message TEXT,
            resume_filename TEXT NOT NULL,
            resume_path TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def save_contact(name, email, subject, message):
    conn = get_db()
    conn.execute(
        'INSERT INTO contacts (name, email, subject, message, created_at) VALUES (?, ?, ?, ?, ?)',
        (name, email, subject, message, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def save_application(name, email, phone, position, experience, message, resume_file):
    if not resume_file or resume_file.filename == '':
        raise ValueError('Resume file is required')

    if not allowed_file(resume_file.filename):
        raise ValueError('Only PDF, DOC, and DOCX files are allowed')

    original_name = secure_filename(resume_file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_name = f"{timestamp}_{original_name}"
    file_path = os.path.join(UPLOAD_FOLDER, safe_name)
    resume_file.save(file_path)

    conn = get_db()
    conn.execute(
        '''INSERT INTO applications
           (name, email, phone, position, experience, message, resume_filename, resume_path, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (name, email, phone, position, experience, message, original_name, safe_name,
         datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

    return safe_name
