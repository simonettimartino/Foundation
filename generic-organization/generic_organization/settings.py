"""
Django settings for generic-organization project.

Generated by 'django-admin startproject' using Django 2.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import socket
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

VERIFY_WIDGET_URL = os.environ.get('VERIFY_WIDGET_URL', 'localhost')
VERIFY_WIDGET_REQUEST_CONTEXT = os.environ.get('VERIFY_WIDGET_REQUEST_CONTEXT', '')
CELERY_BROKER_URL = os.environ.get('REDIS_BROKER_URL', 'N/A')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_RESULT_BACKEND', 'N/A')

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_HIJACK_ROOT_LOGGER = True

API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"

PGCRYPTO_DEFAULT_CIPHER = 'AES'
PGCRYPTO_DEFAULT_KEY = 'eqyhcZgIUb7VKzlE9hRhcePQYPk3bU4E'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sP9Tb48LkJgQux2eLkDKQhWjAWjDTJK6VX6dAYcQwbRCHftfPX'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*']

TEMPLATE_FOLDER_LIST = ["organization_template", "generic_organization", "generic_organization_service"]
BASE_CODE_FOLDER = "/code"

# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'generic_organization_service',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

for root, dirs, files in os.walk(BASE_CODE_FOLDER, topdown=False, followlinks=False):
    if os.path.exists(os.path.join(root, "org_implementation.org")) and os.path.basename(root) \
            not in TEMPLATE_FOLDER_LIST:
        INSTALLED_APPS.append(os.path.basename(root))


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'generic_organization.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['generic_organization_service/templates'],
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

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

WSGI_APPLICATION = 'generic_organization.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'generic_organization_db'),
        'USER': os.environ.get('DB_USERNAME', 'postgres'),
        'PASSWORD': os.environ.get('DB_PWD', 'postgres'),
        'PORT': os.environ.get('DB_PORT', '5433'),
        # 'HOST': 'indydb',
        'HOST': os.environ.get('DB_ADDRESS', '192.168.120.197'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

LOGGING = {
    'version': 1,
    'filters':{
        'ImageMaskingFilter':{
            '()': 'custom_logger.ImageMaskingFilter',
        }
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] [pid:%(process)d] ====>  %(message)s',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'verbose_json': {
            'format': '{\"time\":\"%(asctime)s\", \"level\": \"%(levelname)s\", \"file\":\"%(pathname)s\",\"line\":\"%(lineno)s\", \"pid\":\"%(process)d\", \"message\": \"%(message)s\"}',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'standard': {
            'format': "[%(asctime)s] %(levelname)s %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'json_base': {
            '()': 'custom_formatter.JSONFormatter'
        }
    },
    'handlers': {
        'null': {
            'level': os.getenv('SEVERITY_LOG_LEVEL', 'INFO'),
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': os.getenv('SEVERITY_LOG_LEVEL', 'INFO'),
            'class': 'logging.StreamHandler',
            'formatter': 'verbose_json',
            'filters': ['ImageMaskingFilter']
        },
        'celery': {
            'level': os.getenv('SEVERITY_LOG_LEVEL', 'INFO'),
            'class': 'logging.StreamHandler',
            'formatter': 'verbose_json',
            'filters': ['ImageMaskingFilter']
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'generic_organization_service': {
            'handlers': ['console'],
            'level': os.getenv('SEVERITY_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'zeep.transports': {
            'level': 'ERROR',
            'propagate': False,
            'handlers': ['console'],
        },
        'celery': {
            'handlers': ['celery'],
            'level': os.getenv('SEVERITY_LOG_LEVEL', 'INFO'),
            'propagate': False
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

DESCRIPTION_APP=os.environ.get('DESCRIPTION_APP', 'N/A')
DESCRIPTION_VERSION=os.environ.get('DESCRIPTION_VERSION', 'N/A')
DESCRIPTION_TYPE=os.environ.get('DESCRIPTION_TYPE', 'N/A')
DESCRIPTION_ORGANIZATION=os.environ.get('DESCRIPTION_ORGANIZATION', 'N/A')