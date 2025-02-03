"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from django.utils.translation import gettext_lazy as _

from pathlib import Path
from dotenv import load_dotenv
import os
from corsheaders.defaults import default_headers

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f@^!#(oesgfx+=x)y&toxqpzn^fw+u8i50c06+z_te@tgm%1jx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

USE_I18N = True
USE_L10N = True
USE_TZ = True


LANGUAGE_CODE = 'en'

LANGUAGES = [
    ("en", _("English")),
    ('ka', _("Georgian")),
    ('ru', _("Russian"))
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

MODELTRANSLATION_LANGUAGES = ('en', 'ka', 'ru')

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

ASGI_APPLICATION = 'project.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',  # Use 'channels_redis' if using Redis
    },
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.sites',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'dj_rest_auth.registration',
    'main',
    'default',
    'authentication',
    'channels',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'rest_framework',
    'corsheaders',
]



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '850f242d7d5cf2'
EMAIL_HOST_PASSWORD = 'a98cf5743bfa6b'
DEFAULT_FROM_EMAIL = 'sandbox.smtp.mailtrap.io'

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'

REST_USE_JWT = False

REST_AUTH_TOKEN_MODEL = None
TOKEN_MODEL = None

LOGIN_REDIRECT_URL = 'http://localhost:3000'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['openid', 'profile', 'email'],  # Required scopes for Google login
        'AUTH_PARAMS': {'access_type': 'online'},  # Optional: Google's access_type
        'OAUTH_PKCE_ENABLED': True,  # Enable PKCE (Proof Key for Code Exchange) for better security
        'APP': {
            'client_id': '264255295494-vpu5hf44fk9h11765l13p2oppt12evoq.apps.googleusercontent.com',  # Your Google client ID
            'secret': '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',  # Your Google client secret
            'key': '',  # Optional: You can leave this empty or add if needed
        }
    }
}

GOOGLE_CLIENT_ID = '264255295494-vpu5hf44fk9h11765l13p2oppt12evoq.apps.googleusercontent.com'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, "templates")
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True  
CORS_ALLOW_HEADERS = list(default_headers) + [
    'Authorization',
    'Content-Type',  
]

CORS_ALLOW_METHODS = ['*'] 

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'https://caligraphe-api.onrender.com'
]

ALLOWED_HOSTS = [
    '127.0.0.1', 
    'localhost',
    'caligraphe-api.onrender.com'
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'https://caligraphe-api.onrender.com'
]

# Sessions
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = None
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  
SESSION_SAVE_EVERY_REQUEST = True

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # or 'django.db.backends.mysql'
        'NAME': 'defaultdb',
        'USER': 'avnadmin',
        'PASSWORD': 'AVNS_MAwqgjOKyCFVtz8M3O3',
        'HOST': 'mysql-2e91a58d-shabashvilinika-e2db.c.aivencloud.com',
        'PORT': '17842',  # or '3306' for MySQL
        'OPTIONS': {
            'charset': 'utf8mb4',
            'ssl': {
                'ca': r'ca.pem',  # Path to the certificate file
            },
        },
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'authentication.middleware.CustomSessionAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


MEDIA_URL = '/uploads/' 
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760
APPEND_SLASH = False
# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

TIME_ZONE = os.getenv('DJANGO_TIME_ZONE', 'UTC')
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000/en')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000/en')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
