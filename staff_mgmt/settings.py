from pathlib import Path
import os
from datetime import timedelta
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==========================
# 🔐 Security Keys
# ==========================
SECRET_KEY = config(
    "DJANGO_SECRET_KEY",
    default="unsafe-secret-key-change-in-production"
)


# ==========================
# 📧 Email Settings
# ==========================
EMAIL_BACKEND = config(
    "DJANGO_EMAIL_BACKEND",
)
EMAIL_HOST = config("DJANGO_EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("DJANGO_EMAIL_PORT", cast=int, default=587)
EMAIL_USE_TLS = config("DJANGO_EMAIL_USE_TLS", cast=bool, default=True)
EMAIL_HOST_USER = config("DJANGO_EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("DJANGO_EMAIL_HOST_PASSWORD", default="")
DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL",
    default=f"StaffHub <{EMAIL_HOST_USER}>"
)

# ==========================
# 🍪 Session Settings
# ==========================
SESSION_ENGINE = config(
    "SESSION_ENGINE",
    default="django.contrib.sessions.backends.db"
)
SESSION_COOKIE_NAME = "sessionid"
SESSION_COOKIE_AGE = config("SESSION_COOKIE_AGE", cast=int, default=3600)  # 1hr in seconds
SESSION_SAVE_EVERY_REQUEST = config("SESSION_SAVE_EVERY_REQUEST", cast=bool, default=True)
SESSION_EXPIRE_AT_BROWSER_CLOSE = config("SESSION_EXPIRE_AT_BROWSER_CLOSE", cast=bool, default=True)

# ==========================
# ⏳ Token Expiry Times
# ==========================
OTP_EXPIRY_MINUTES = config("OTP_EXPIRY_MINUTES", cast=int, default=10)
PASSWORD_RESET_TOKEN_EXPIRY_HOURS = config("PASSWORD_RESET_TOKEN_EXPIRY_HOURS", cast=int, default=1)

# Helper variables for use in views/services
OTP_EXPIRY_DELTA = timedelta(minutes=OTP_EXPIRY_MINUTES)
PASSWORD_RESET_TOKEN_EXPIRY_DELTA = timedelta(hours=PASSWORD_RESET_TOKEN_EXPIRY_HOURS)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = "accounts.User"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    
    # Project Apps
    "accounts",
    "attendance",
    "leave",
    "staff",
    "adminpanel",
    "core",
    
    "django_extensions",
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

ROOT_URLCONF = 'staff_mgmt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'staff_mgmt.wsgi.application'

from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}


# Authentication settings
LOGIN_URL = '/accounts/login/'  # login URL
LOGIN_REDIRECT_URL = '/'    # Where to redirect after successful login
LOGOUT_REDIRECT_URL = '/'   # Where to redirect after logout

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

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
