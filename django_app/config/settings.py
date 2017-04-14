"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
import json
import os

DEBUG = os.environ.get('MODE') == 'DEBUG'
STORAGE_S3 = os.environ.get('STORAGE') == 'S3' or DEBUG is False
DB_RDS = os.environ.get('DB') == 'RDS'

print('DEBUG : {}'.format(DEBUG))
print('STORAGE_S3 : {}'.format(STORAGE_S3))
print('DB_RDS : {}'.format(DB_RDS))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
CONF_DIR = os.path.join(ROOT_DIR, '.conf-secret')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

# 1. settings_common.json의 경로를 CONFIG_FILE_COMMON에 할당
CONFIG_FILE_COMMON = os.path.join(CONF_DIR, 'settings_common.json')

# 2. settings_local.json의 경로를 CONFIG_FILE에 할당
CONFIG_FILE = os.path.join(CONF_DIR, 'settings_local.json' if DEBUG else 'settings_deploy.json')
print('CONFIG_FILE : {}'.format(CONFIG_FILE))

# 3. CONFIG_FILE_COMMON경로의 파일을 읽어 json.loads()한 결과를 config_common에 할당
config_common = json.loads(open(CONFIG_FILE_COMMON).read())

# 4. CONFIG_FILE경로의 파일을 읽어 json.loads()한 결과를 config에 할당
config = json.loads(open(CONFIG_FILE).read())

# config_common의 내용을 현재 config에 합침
for key, key_dict in config_common.items():
    if not config.get(key):
        config[key] = {}
    for inner_key, inner_key_dict in key_dict.items():
        config[key][inner_key] = inner_key_dict

# AWS
AWS_ACCESS_KEY_ID = config['aws']['access_key_id']
AWS_SECRET_ACCESS_KEY = config['aws']['secret_access_key']

AWS_S3_HOST = 's3.{}.amazonaws.com'.format(config['aws']['s3_region'])
AWS_S3_SIGNATURE_VERSION = config['aws']['s3_signature_version']
AWS_STORAGE_BUCKET_NAME = config['aws']['s3_storage_bucket_name']
AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)

# static settings
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    STATIC_DIR,
)

if STORAGE_S3:
    # Static files
    STATICFILES_STORAGE = 'config.storages.StaticStorage'
    STATICFILES_LOCATION = 'static'
    STATIC_URL = 'https://{custom_domain}/{staticfiles_location}/'.format(
        custom_domain=AWS_S3_CUSTOM_DOMAIN,
        staticfiles_location=STATICFILES_LOCATION,
    )
    # Media files
    DEFAULT_FILE_STORAGE = 'config.storages.MediaStorage'
    MEDIAFILES_LOCATION = 'media'
    MEDIA_URL = 'https://{custom_domain}/{mediafiles_location}/'.format(
        custom_domain=AWS_S3_CUSTOM_DOMAIN,
        mediafiles_location=MEDIAFILES_LOCATION
    )
else:
    STATIC_ROOT = os.path.join(ROOT_DIR, 'static_root')
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(ROOT_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config['django']['secret_key']

ALLOWED_HOSTS = config['django']['allowed_hosts']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',

    'storages',

    'member',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.permissions.IsAdminUser',
    ),
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'PAGE_SIZE': 10
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATE_DIR,
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

if DEBUG and DB_RDS:
    # DEBUG모드이며 DB_RDS옵션일 경우, 로컬 postgreSQL이 아닌 RDS로 접속해 테스트한다
    config_db = config['db_rds']
else:
    # 그 외의 경우에는 해당 db설정을 따름
    config_db = config['db']
DATABASES = {
    'default': {
        'ENGINE': config_db['engine'],
        'NAME': config_db['name'],
        'USER': config_db['user'],
        'PASSWORD': config_db['password'],
        'HOST': config_db['host'],
        'PORT': config_db['port'],
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'member.User'
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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
