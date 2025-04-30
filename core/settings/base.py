from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv('../.env')

BASE_DIR = Path(__file__).resolve().parent.parent.parent
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    ##
    "account",
    "organization",
    ##
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "drf_spectacular",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
AUTH_USER_MODEL = "account.User"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "digital_attendance/static/"

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}
SPECTACULAR_SETTINGS = {
    'TITLE': 'Digital Attendance',
    'SERVE_INCLUDE_SCHEMA': False,  # You can enable this to serve the schema file as well
    'TAGS': [
        {"name": "1. Register and login"},
        {"name": "2. Assign/Revoke Staff (by Staff)"},
        {"name": "3. Assign/Revoke Organizational Super Admin (by Staff)"},
        {"name": "4. Create/View Organization (by Organizational Super Admin)"},
        {"name": "5. Archive Organization (by Staff)"},
        {"name": "6. Assign/Revoke Organizational Admin (by Organizational Super Admin & Organizational Admin)"},
        {"name": "7. View Organizational Admins in a specific Organization (by Organizational Super Admin & Organizational Admin)"},
        {"name": "8. Update Organizational Admin (by Organizational Super Admin)"},
    ],
    'SWAGGER_UI_SETTINGS': {
        'docExpansion': 'none',  # Collapses all sections by default
    },
}

CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')