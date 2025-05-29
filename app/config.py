import os

DB_USER = os.getenv('DB_USER', 'hrusr')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'hrpwd')
DB_NAME = os.getenv('DB_NAME', 'hrdb')
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = os.getenv('DB_PORT', '5432')

SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Add a secret key for session management (IMPORTANT: use a strong, random key in production)
SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key_here') #