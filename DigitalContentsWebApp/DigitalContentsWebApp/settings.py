"""
Django settings for DigitalContentsWebApp project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*********************'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'channels',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts.apps.AccountsConfig',
    'django_filters',

    'storages',
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

ROOT_URLCONF = 'DigitalContentsWebApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'DigitalContentsWebApp.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# SQLITE DATABASE
# DATABASES = {
#      'default': {
#          'ENGINE': 'django.db.backends.sqlite3',
#          'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#      }
#  }


# LOCAL POSTGRES DATABASE FOR HOSTING STATIC FILES LOCALLY
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '***********************',
        'USER': '***************',
        'PASSWORD': '*****************',
        'HOST': '**************',
        'PORT': '**************'
    }
}

# POSTGRES AWS RDS DATABASE LIVE
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': '************',
#         'USER': '*********',
#         'PASSWORD': '*************',
#         'HOST': '************',
#         'PORT': '*****'
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# configurations for local storage
STATIC_URL = '/static/'

MEDIA_URL = '/images/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')


# SMTP Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '*****************@gmail.com'
EMAIL_HOST_PASSWORD = '**************'

# S3 BUCKET CONFIGURATIONS
# AWS_ACCESS_KEY_ID = '***************'
# AWS_SECRET_ACCESS_KEY = '********************************'
# AWS_STORAGE_BUCKET_NAME = '*****************'

# django storages S3 bucket https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
# AWS_S3_FILE_OVERWRITE = False
# AWS_DEFAULT_ACL = None
# DEFAULT_FILE_STORAGE = 'DigitalContentsWebApp.custom_storage.MediaStorage'  # stores file to specified directory
# # STATICFILES_STORAGE = 'DigitalContentsWebApp.custom_storage.StaticStorage'  # hosts file from specified directory
#
# # DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' # stores file to s3 bucket directly
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'    # hosts file directly from s3 bucket

ASGI_APPLICATION = "DigitalContentsWebApp.routingg.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# STRIPE KEYS
STRIPE_PUBLISHABLE_KEY = '*****************************'
STRIPE_SECRET_KEY = '**************************'
STRIPE_PRICE_ID = '*******************************'
STRIPE_ENDPOINT_SECRET = "******************************"

# PAYPAL_KEYS
