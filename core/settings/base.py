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
    "program",
    "event",
    ##
    "rest_framework",
    "rest_framework_nested",
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
        {"name": "9. Create/View/Archive Program (by Organizational Super Admin & Organizational Admin)"},
        {"name": "10. Invite/Undo Invite (by Organizational Super Admin & Organizational Admin)"},
        {"name": "11. Accept/Reject/View Invite (by other Organizational Super Admin & other Organizational Admin)"},
        {"name": "12. View/Leave Associated Programs (by other Organizational Super Admin & other Organizational Admin)"},
        {"name": "13. Subscribe/Unsubscribe/View to Program (by User)"},
        {"name": "14. Subscribers in Program (by O. S. Admins, O. Admins, Event Admins & Event Organizers with permission)"},
        {"name": "15. Subscribed Programs of a User (by Staff)"},
        {"name": "16. Assign/Revoke Program Event Admin (by Organizational Admin & Organizational Super Admin)"},
        {"name": "17. View Program Event Admins in a specific Program (by Program Admin & Organizational Admin & Organizational Super Admin)"},
        {"name": "18. Update Program Event Admin (by Organizational Admin & Organizational Super Admin)"},
        {"name": "19. Create/View/Conclude/Archive/Reactivate Event (by Program Event Admin & Organizational Admin & Organizational Super Admin)"},
        {"name": "20. Get Event by Short Code (by Attendee)"},
        {"name": "21. Create Attendance (by Attendee)"},
        {"name": "22. List Attendances (by Attendee)"},
        {"name": "23. Update Display Name (by Attendee)"},
        {"name": "24. Get Event Attendees (by Program Event Admin & Organizational Admin & Organizational Super Admin)"},
        {"name": "25. Invalidate/Revalidate Attendance (by Program Event Admin & Organizational Admin & Organizational Super Admin)"},
        {"name": "26. My Roles"},
        {"name": "27. List Organizations (by any - no authentication required)"},
    ],
    'SWAGGER_UI_SETTINGS': {
        'docExpansion': 'none',  # Collapses all sections by default
    },
}

CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
SIGNATURE_THRESHOLD = float(os.environ.get('SIGNATURE_THRESHOLD', 0.5))