"""
Django settings for oroose project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if os.environ.get('MAIN_PROCESS') == 'PRODUCTION':
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, "prod.env"))
elif os.environ.get('MAIN_PROCESS') == 'TESTING':
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, "test.env"))
else:
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, "devel.env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "8ab#e7$3avrz62$)=0_+s)pvq7222py&ga%nks^y#e3bd$xwo="

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django_celery_beat",
    "core",
    "home",
    "bengaluru",
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

ROOT_URLCONF = "oroose.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR, "templates"],
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

WSGI_APPLICATION = "oroose.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_NAME'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get("POSTGRES_HOST"),
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = [BASE_DIR, "static"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Config file
# LOAD_CONFIG_PATH = "config.json"
LOAD_CONFIG_PATH = os.environ.get('LOAD_CONFIG_PATH')


# Celery - prefix with CELERY_
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_TASK_TRACK_STARTED = True


# API
LIVE_INDEX_URL = os.environ.get('LIVE_INDEX_URL')
LIVE_INDEX_500_URL = os.environ.get('LIVE_INDEX_500_URL')

# FHZ Configuration
FH_RANK_FROM = os.environ.get('FH_RANK_FROM')
FH_RANK_TILL = os.environ.get('FH_RANK_TILL')
FH_MAX_PRICE = os.environ.get('FH_MAX_PRICE')
FH_MAX_TOTAL_PRICE = os.environ.get('FH_MAX_TOTAL_PRICE')
FH_MAX_PERCENT = os.environ.get('FH_MAX_PERCENT')
FH_MAX_BUY_ORDER = os.environ.get('FH_MAX_BUY_ORDER')

# Logger
LOG_SCHEDULE_LIVE_500 = "Live 500"
LOG_SCHEDULE_ZERO_500 = "Zero 500"

# Timing
FH_STOCK_LIVE_START = "0915"
FH_STOCK_LIVE_END = "1515"
FH_ZERO_START = "0915"
FH_ZERO_END = "1415"
