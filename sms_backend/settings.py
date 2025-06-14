# StudentManagementSystem/sms_backend/settings.py

import os
from pathlib import Path
import dj_database_url # Import for PostgreSQL database configuration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY WARNING: keep the secret key used in production secret! ---
# For production, load from environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', '8z!$g8vhqh=cos8d5x*q&wi50e!5e+g6^0i^(@)tyq13_t-gh$') # Replace with a strong default or ensure it's always set in Render env

# --- SECURITY WARNING: don't run with debug turned on in production! ---
# This line correctly sets DEBUG to False on Render, and True locally.
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []
# Render sets the "RENDER" environment variable to "true"
if 'RENDER' in os.environ:
    # Add Render's external hostname. This is crucial for DEBUG = False.
    ALLOWED_HOSTS += [os.environ.get('RENDER_EXTERNAL_HOSTNAME')]
else:
    # For local development
    ALLOWED_HOSTS += ['127.0.0.1', 'localhost']

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
    # 'whitenoise.middleware.WhiteNoiseMiddleware', <-- REMOVED from INSTALLED_APPS
    # 'whitenoise.runserver_nostatic', # Only necessary for local static serving with runserver
    # For WhiteNoise to work, ensure 'whitenoise' is implicitly installed (from requirements.txt)
    # and its middleware is correctly placed. No explicit app config needed for whitenoise itself.
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise must be listed directly after SecurityMiddleware for proper static file serving
    'whitenoise.middleware.WhiteNoiseMiddleware', # This is where it belongs
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
        'DIRS': [BASE_DIR], # This allows Django to find index.html in the project root
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

# Use PostgreSQL in production (on Render)
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
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
    # Assuming your frontend service name is 'your-backend-name-frontend' if backend is 'your-backend-name'.
    backend_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if backend_hostname:
        # Example: if backend is 'sms-backend.onrender.com', frontend might be 'sms-frontend.onrender.com'
        # Adjust the replacement logic if your frontend naming convention is different.
        frontend_hostname = backend_hostname.replace('-backend', '-frontend')
        CORS_ALLOWED_ORIGINS.append(f"https://{frontend_hostname}")
        # Also ensure the backend's own URL is allowed for API testing directly (e.g., /api/)
        CORS_ALLOWED_ORIGINS.append(f"https://{backend_hostname}")


# Allow credentials if needed (e.g., for sessions/cookies, though generally not for simple APIs)
CORS_ALLOW_CREDENTIALS = False # Change to True if your frontend needs to send cookies/auth headers
