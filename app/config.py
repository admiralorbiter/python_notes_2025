# app/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-please-change-in-production')
    NOTEBOOKS_DIR = os.environ.get('NOTEBOOKS_DIR', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'notebooks'))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Max upload size of 16 MB
    
    # PyScript configuration
    PYSCRIPT_ENABLED = True
    
    # Security headers
    TEMPLATES_AUTO_RELOAD = True
    SESSION_COOKIE_SECURE = False
    REMEMBER_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    ENV = 'development'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    ENV = 'testing'
    WTF_CSRF_ENABLED = False
    NOTEBOOKS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tests/fixtures/notebooks')

class ProductionConfig(Config):
    """Production configuration."""
    ENV = 'production'
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    
    # Override these in .env for production
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Ensure we have a valid secret key in production
    @classmethod
    def init_app(cls, app):
        if not cls.SECRET_KEY or len(cls.SECRET_KEY) < 16:
            app.logger.error('Invalid SECRET_KEY. Using a secure key is required in production!')
            raise ValueError('SECRET_KEY must be set to a secure random string in production')

# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}