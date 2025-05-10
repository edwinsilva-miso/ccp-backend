import os


class Config:
    """Application configuration."""

    # Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')

    # Database config
    DB_USER = os.environ.get('DB_USER', 'postgres')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
    DB_NAME = os.environ.get('DB_NAME', 'rutas')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    # OpenRoute Service config
    OPENROUTE_API_KEY = os.environ.get('OPENROUTE_API_KEY', '')
    OPENROUTE_BASE_URL = os.environ.get('OPENROUTE_BASE_URL', 'https://api.openrouteservice.org')


class TestConfig(Config):
    """Test configuration."""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
