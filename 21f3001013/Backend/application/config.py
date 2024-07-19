import os
import secrets
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = secrets.token_hex(16)
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "testdb1.sqlite3")
    UPLOADED_IMAGES_DEST = os.path.join(os.getcwd(), 'uploads')
    DEBUG = True
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    REDIS_URL = "redis://localhost:6379"
      
    MAIL_SERVER='localhost'
    MAIL_PORT=1025,  # MailHog SMTP port
    MAIL_USE_TLS=False
    MAIL_USE_SSL=False
    MAIL_USERNAME=None
    MAIL_PASSWORD=None
    DEFAULT_MAIL_SENDER='lalitmach22@example.com'

    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 9
    
      

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "testdb1.sqlite3")
    DEBUG = True
    SECRET_KEY = secrets.token_hex(16)
    UPLOADED_IMAGES_DEST = os.path.join(os.getcwd(), 'uploads')
    WTF_CSRF_ENABLED = False
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    REDIS_URL = "redis://localhost:6379"
    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 9    


class StageConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "testdb1.sqlite3")
    DEBUG = True
    SECRET_KEY = secrets.token_hex(16)
    UPLOADED_IMAGES_DEST = os.path.join(os.getcwd(), 'uploads')
    WTF_CSRF_ENABLED = False
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    REDIS_URL = "redis://localhost:6379"
    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379
    CACHE_REDIS_DB = 9    
