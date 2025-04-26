from .base import *
from django.utils.timezone import timedelta

DEBUG = False
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set or empty")

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
if not ALLOWED_HOSTS or ALLOWED_HOSTS == ['']:
    raise ValueError("ALLOWED_HOSTS is not set or empty")

ACCESS_TOKEN_LIFETIME = os.environ.get('ACCESS_TOKEN_LIFETIME', '30')

if not ACCESS_TOKEN_LIFETIME.isdigit():
    raise ValueError("ACCESS_TOKEN_LIFETIME is not a valid integer")
ACCESS_TOKEN_LIFETIME = int(ACCESS_TOKEN_LIFETIME)

REFRESH_TOKEN_LIFETIME = os.environ.get("REFRESH_TOKEN_LIFETIME", "180")
if not REFRESH_TOKEN_LIFETIME.isdigit():
    raise ValueError("REFRESH_TOKEN_LIFETIME is not a valid integer")
REFRESH_TOKEN_LIFETIME = int(REFRESH_TOKEN_LIFETIME)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=ACCESS_TOKEN_LIFETIME),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=REFRESH_TOKEN_LIFETIME),
    "ROTATE_REFRESH_TOKENS": False,
}

CORS_ALLOW_ALL = os.environ.get("CORS_ALLOW_ALL", "false")
if CORS_ALLOW_ALL == 'true':
    CORS_ALLOWED_ORIGINS = []
    CORS_TRUSTED_ORIGINS = []
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOW_METHODS = [
        "DELETE",
        "GET",
        "OPTIONS",
        "PATCH",
        "POST",
        "PUT",
    ]

    CORS_ALLOW_HEADERS = [
        "accept",
        "accept-encoding",
        "authorization",
        "content-type",
        "dnt",
        "origin",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
    ]
else:

    CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS').split(',')
    if not CORS_ALLOWED_ORIGINS or CORS_ALLOWED_ORIGINS == [""]:
        raise ValueError("CORS_ALLOWED_ORIGINS is not set or empty")

    CORS_TRUSTED_ORIGINS = os.environ.get('CORS_TRUSTED_ORIGINS').split(',')
    if not CORS_TRUSTED_ORIGINS or CORS_TRUSTED_ORIGINS == [""]:
        raise ValueError("CORS_TRUSTED_ORIGINS is not set or empty")

    CORS_ALLOW_CREDENTIALS = True

    CORS_ALLOW_METHODS = [
        'DELETE',
        'GET',
        'OPTIONS',
        'PATCH',
        'POST',
        'PUT',
    ]

    CORS_ALLOW_HEADERS = [
        'accept',
        'accept-encoding',
        'authorization',
        'content-type',
        'dnt',
        'origin',
        'user-agent',
        'x-csrftoken',
        'x-requested-with',
    ]

DB_NAME = os.environ.get("DB_NAME")
if not DB_NAME:
    raise ValueError("DB_NAME is not set or empty")

DB_USER = os.environ.get("DB_USER")
if not DB_USER:
    raise ValueError("DB_USER is not set or empty")

DB_PASSWORD = os.environ.get("DB_PASSWORD")
if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD is not set or empty")

DB_HOST = os.environ.get("DB_HOST")
if not DB_HOST:
    raise ValueError("DB_HOST is not set or empty")

DB_PORT = os.environ.get("DB_PORT", "5432")
if not DB_PORT.isdigit():
    raise ValueError("DB_PORT is not a valid integer")
DB_PORT = int(DB_PORT)

DB_ENGINE = os.environ.get('DB_ENGINE', 'django.db.backends.postgresql')  # Default to PostgreSQL if not set
valid_engines = [
    'django.db.backends.postgresql',
    'django.db.backends.mysql',
    'django.db.backends.sqlite3',
    'django.db.backends.oracle',
]

if DB_ENGINE not in valid_engines:
    raise ValueError(f"Invalid DB_ENGINE value: {DB_ENGINE}. Valid options are: {', '.join(valid_engines)}")

DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,  
        'USER': DB_USER,        
        'PASSWORD': DB_PASSWORD,       
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}