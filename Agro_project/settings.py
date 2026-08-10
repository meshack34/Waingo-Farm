import os
from dotenv import load_dotenv

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-wbpoj_d(4x$qfo)mo=t&vkv^!c5$_yl%8)shp^u4x+sz$0t%ya'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*,","localhost","127.0.0.1","waingofarm.pythonanywhere.com",".ngrok-free.app",]
CSRF_TRUSTED_ORIGINS = [
    "https://waingofarm.com",
    "https://cd1d-41-139-140-211.ngrok-free.app/",
]

# Application definition

INSTALLED_APPS = [
    "Farm",
    "widget_tweaks",
    "crispy_forms",
    "crispy_bootstrap5",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Agro_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'Farm.context_processors.cart_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'Agro_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# =========================================================
# AUTHENTICATION
# =========================================================

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = "/owner/"

LOGOUT_REDIRECT_URL = "/login/"


PAYPAL_CLIENT_ID = "AQRk_BNJ53jb5kdVbkLQBrjFLBCPfzGszSEeME7-9Zpv0EQjvMeuhjs9p25G7-du1XYzrBkaO7wfe5c3"
PAYPAL_CLIENT_SECRET = "EKOf5W7Uli_WV5LHkbn6jNMEwIvqVFvv8cvNnlp4wBGNaaAyFBjAFmrNOdD2u72AsFbd3UqlEi6RYRkB"
PAYPAL_MODE = "sandbox"

# =========================================================
# MPESA DARaja CONFIGURATION
# =========================================================

DARAJA_CONSUMER_KEY = os.getenv("DARAJA_CONSUMER_KEY")

DARAJA_CONSUMER_SECRET = os.getenv("DARAJA_CONSUMER_SECRET")

DARAJA_SHORTCODE = os.getenv("DARAJA_SHORTCODE")

DARAJA_PASSKEY = os.getenv("DARAJA_PASSKEY")

DARAJA_CALLBACK_URL = os.getenv("DARAJA_CALLBACK_URL")