# StudentManagementSystem/sms_backend/settings.py

import os
from pathlib import Path
import dj_database_url # Import for PostgreSQL database configuration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY WARNING: keep the secret key used in production secret! ---
# For production, load from environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-insecure-default-secret-key-if-not-set-in-env') # Replace with a strong default or ensure it's always set in Render env

# --- SECURITY WARNING: don't run with debug turned on in production! ---
# This line correctly sets DEBUG to False on Render (production), and True locally (development).
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []
# Render sets the "RENDER" environment variable to "true"
if 'RENDER' in os.environ:
    # Add Render's external hostname to ALLOWED_HOSTS for production
    RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if RENDER_EXTERNAL_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
else:
    # For local development
    ALLOWED_HOSTS.extend(['127.0.0.1', 'localhost'])

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'students',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Place after SecurityMiddleware for static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'sms_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR],
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

WSGI_APPLICATION = 'sms_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Use PostgreSQL in production (on Render) if DATABASE_URL is provided
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.config(
        default=DATABASE_URL
    )


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
# This is the directory where `collectstatic` will gather all static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# For local development, if you have static files outside of app/static/ folders
STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, 'static'), # Uncomment if you have a top-level /static/ folder
]

# Set STATICFILES_STORAGE for WhiteNoise in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS Configuration for both local and production environments
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000", # For local development if backend is on 8000
    "http://localhost:8000", # For local development if backend is on localhost:8000
]

if 'RENDER' in os.environ:
    # Dynamically determine the frontend's Render URL based on the backend's hostname.
    backend_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if backend_hostname:
        # Assuming your frontend service name is 'your-backend-name-frontend' if backend is 'your-backend-name'.
        # Adjust the replacement logic if your frontend naming convention is different.
        frontend_hostname = backend_hostname.replace('-backend', '-frontend') # Example: sms-backend -> sms-frontend
        CORS_ALLOWED_ORIGINS.append(f"https://{frontend_hostname}")
        # Also ensure the backend's own URL is allowed for API testing directly (e.g., /api/)
        CORS_ALLOWED_ORIGINS.append(f"https://{backend_hostname}")


# Allow credentials if needed (e.g., for sessions/cookies, though generally not for simple APIs)
CORS_ALLOW_CREDENTIALS = False # Change to True if your frontend needs to send cookies/auth headers
