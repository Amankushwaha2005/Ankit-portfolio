import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads', 'resumes')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

SECRET_KEY = os.environ.get('SECRET_KEY', 'ankit-portfolio-secret-key-2026')
DEBUG = True
HOST = '0.0.0.0'
PORT = 5000

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
