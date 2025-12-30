import os
from datetime import timedelta


class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or os.environ.get('SECRET_KEY') or 'dev-jwt-secret-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRATION_HOURS = int(os.environ.get('JWT_EXPIRATION_HOURS', 24))
    JWT_EXPIRATION_DELTA = timedelta(hours=JWT_EXPIRATION_HOURS)
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
    
    # Pagination
    USERS_PER_PAGE = 10


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.getcwd(), 'instance', 'app.db')


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    def __init__(self):
        super().__init__()
        # Ensure critical keys are set in production
        if not os.environ.get('SECRET_KEY'):
            import warnings
            warnings.warn(
                "⚠️  WARNING: SECRET_KEY environment variable is not set! "
                "Please set it using a secure random value. "
                "Run 'python generate_secret_key.py' to generate one."
            )
        
        if not os.environ.get('JWT_SECRET_KEY'):
            import warnings
            warnings.warn(
                "⚠️  WARNING: JWT_SECRET_KEY environment variable is not set! "
                "Using SECRET_KEY as fallback. For better security, set a separate JWT_SECRET_KEY."
            )


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
