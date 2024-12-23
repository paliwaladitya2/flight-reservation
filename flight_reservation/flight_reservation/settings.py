from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = "django-insecure-ry+c3sht4apmxpj5#_zjriu-&9-0n7vj4v(di_mq0=u#gw5sx9"
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Installed Applications
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "reservations",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",  # Handles sessions
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Associates users with sessions
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# URL Configuration
ROOT_URLCONF = "flight_reservation.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Template directory
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = "flight_reservation.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Authentication
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]  # Directory for custom static files
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files (if required)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# User Authentication
AUTH_USER_MODEL = "reservations.CustomUser"  # Custom user model
LOGIN_URL = "/login/"  # Redirect URL for login
LOGIN_REDIRECT_URL = "/my-bookings/"  # Redirect after successful login
LOGOUT_REDIRECT_URL = "/login/"  # Redirect after logout

# Session Settings
SESSION_COOKIE_SAMESITE = "Lax"  # Adjusted for template-based frontend
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False  

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    "http://localhost",
    "http://127.0.0.1",
]

# PayPal Configuration
PAYPAL_CLIENT_ID = "Abrw0xkAkLNHz9GVo5GeuAY2jjsfU4yqgU4TqT_LKQbNPgaC-xDZ2iIFy-8GjwQnDJWLtBfTfaUiIHXY"  # Client ID credentials from paypal
PAYPAL_CLIENT_SECRET = "ENlsdipTMsZpF-Pi2y6fqEc32c3X0y1Lpz1ZJ0zNYWmA-KmaLPbgG4FjOVvowWhQ_E_EX1LKqFmh0CL6"  # Client Secret credentials from paypal
PAYPAL_ENVIRONMENT = "sandbox"  # Environment for testing