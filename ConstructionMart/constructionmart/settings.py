import os
from pathlib import Path
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

# Never commit production secrets. Set DJANGO_SECRET_KEY in Vercel Environment Variables.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    if os.environ.get("VERCEL"):
        raise ImproperlyConfigured(
            "Set DJANGO_SECRET_KEY in Vercel Project Settings > Environment Variables."
        )
    SECRET_KEY = "local-development-only-change-before-deployment"

DEBUG = os.environ.get("DEBUG", "False").lower() in {"1", "true", "yes", "on"}

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".vercel.app",
]
extra_hosts = os.environ.get("DJANGO_ALLOWED_HOSTS", "")
ALLOWED_HOSTS.extend(host.strip() for host in extra_hosts.split(",") if host.strip())

CSRF_TRUSTED_ORIGINS = ["https://*.vercel.app"]
extra_origins = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS.extend(origin.strip() for origin in extra_origins.split(",") if origin.strip())

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "store",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "constructionmart.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "constructionmart.wsgi.application"

# SQLite is for local development only. Vercel must use a persistent PostgreSQL database.
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=0,
            conn_health_checks=True,
        )
    }
elif os.environ.get("VERCEL"):
    raise ImproperlyConfigured(
        "Set DATABASE_URL to a persistent PostgreSQL connection string in Vercel. "
        "SQLite is not suitable for production serverless storage."
    )
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-in"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# HTTPS is handled by Vercel in production.
if os.environ.get("VERCEL"):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SESSION_COOKIE_SECURE = not DEBUG
    CSRF_COOKIE_SECURE = not DEBUG
