"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-dk)$1t3s*rq$v8j!7n5q$202#4!)#$wayk@15&o1w)4)@*_3k+"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost 127.0.0.1").split()


# CORS Origin Whitelist
CORS_ORIGIN_WHITELIST = os.environ.get(
    "DJANGO_CORS_ORIGIN_WHITELIST",
    "http://localhost http://127.0.0.1 http://localhost:3000 http://localhost:8000",
).split()

CSRF_TRUSTED_ORIGINS = ["localhost:3000", "127.0.0.1:3000"]


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_cas_ng",
    "django_extensions",
    "graphene_django",
    "authentication",
    "club_manager",
    "event_manager",
    "user_manager",
    "finance_manager",
    "misc",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # TODO: uncomment this and fix CSRF
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_cas_ng.middleware.CASMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
    "django_cas_ng.backends.CASBackend",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "backend.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DJANGO_DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.environ.get("DJANGO_DB_NAME", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.environ.get("DJANGO_DB_USER", "user"),
        "PASSWORD": os.environ.get("DJANGO_DB_PASSWORD", "password"),
        "HOST": os.environ.get("DJANGO_DB_HOST", "localhost"),
        "PORT": os.environ.get("DJANGO_DB_PORT", "5432"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Graphene Settings
GRAPHENE = {
    "SCHEMA": "backend.schema.schema",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
}


# CAS Configuration
CAS_SERVER_URL = "https://login.iiit.ac.in/cas/"
CAS_IGNORE_REFERER = True
CAS_CHECK_NEXT = False
CAS_REDIRECT_URL = "/accounts/jwt"
CAS_CLIENT_URL = os.environ.get("DJANGO_CAS_CLIENT_URL", "http://localhost:3000")
CAS_FORCE_CHANGE_USERNAME_CASE = "lower"


# Snapshot Testing
TEST_RUNNER = "snapshottest.django.TestRunner"


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "django_static")
STATIC_URL = "/django_static/"


# Media (Images, etc)
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
