"""
Django settings for rpgsite project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Operating system

import sys

IS_WINDOWS = sys.platform == 'win32'
IS_LINUX = sys.platform in ('linux', 'linux2')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^pk_pdf!!av9q-au8=$yx@vpvq^9qzu^$#g4dm9-!+2zm#3@y('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

USE_WHITENOISE = False

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '192.168.1.10',
]

if IS_LINUX:
    SECRET_DIR = '/var/www/rpgsite'
else:
    SECRET_DIR = os.path.join(BASE_DIR, 'secret')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.accounts',
    'apps.players',
    'apps.houses',
    'apps.guilds',
    'apps.server',
    'emoji',
]

MIDDLEWARE = [
    #'tools.middleware.PrettyIndentMiddleware',
    #'tools.middleware.HideIndentMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rpgsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'builtins': [
                'django.templatetags.static',
                'emoji.templatetags.emoji_tags',
                'apps.tools.templatetags.base_tags',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'rpgsite.context_processors.navigation_context_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'rpgsite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(SECRET_DIR, 'database', 'mysql.ini'),
            'init_command':
                'SET default_storage_engine=INNODB; '
                'SET sql_mode=STRICT_TRANS_TABLES; ',
        },
    },
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SECRET_DIR, 'database', 'rpgsite.db'),
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True
USE_TZ = True

USE_L10N = False

DATETIME_FORMAT = 'j F Y, H:i'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_ROOT = os.path.join(SECRET_DIR, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# Media files (uploaded by users)

MEDIA_ROOT = os.path.join(SECRET_DIR, 'media')

MEDIA_URL = '/media/'

# Inputs

INPUT_USERNAME_MIN_LENGTH = 3
INPUT_USERNAME_MAX_LENGTH = 30
INPUT_USERNAME_REGEX = r'^[a-zA-Z0-9]+$'

INPUT_PASSWORD_MIN_LENGTH = 6
INPUT_PASSWORD_MAX_LENGTH = 50

INPUT_EMAIL_MIN_LENGTH = 3
INPUT_EMAIL_MAX_LENGTH = 254

CHARACTER_NAME_MIN_LENGTH = 3
CHARACTER_NAME_MAX_LENGTH = 20
CHARACTER_NAME_REGEX = r'^[a-zA-Z ]+$'

# Accounts

import datetime

EMAIL_VERIFICATION_TIME = datetime.timedelta(days=2)

MAX_PLAYERS_PER_ACCOUNT = 4

# Create root account and player

CREATE_ROOT_ON_INIT = True

# RPGSite settings

STATS_RECORDS_LIMIT = 20

# forgottenserver integration

from django.utils.translation import ugettext_lazy as _

VOCATIONS = (
    ('0', 'none', _('None')),
    ('1', 'sorcerer', _('Sorcerer')),
    ('2', 'druid', _('Druid')),
    ('3', 'paladin', _('Paladin')),
    ('4', 'knight', _('Knight')),
    ('5', 'mastersorcerer', _('Master Sorcerer')),
    ('6', 'elderdruid', _('Elder Druid')),
    ('7', 'royalpaladin', _('Royal Paladin')),
    ('8', 'eliteknight', _('Elite Knight')),
)

# Login and logout

LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Email server configuration

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'username@gmail.com'
EMAIL_HOST_PASSWORD = 'password'

EMAIL_USE_CONFIG_FILE = False
EMAIL_CONFIG_FILE = os.path.join(SECRET_DIR, 'emails.ini')

if EMAIL_USE_CONFIG_FILE:
    # Read config from `secret/emails.ini` file
    try:
        from configparser import ConfigParser
        with open(EMAIL_CONFIG_FILE, 'r') as file:
            config = ConfigParser()
            config.read_string(file.read())
            section = 'default'
            if config.has_option(section, 'host'):
                EMAIL_HOST = str(config.get(section, 'host'))
            if config.has_option(section, 'port'):
                EMAIL_PORT = config.getint(section, 'port')
            if config.has_option(section, 'use_ssl'):
                EMAIL_USE_SSL = config.getboolean(section, 'use_ssl')
            if config.has_option(section, 'user'):
                EMAIL_HOST_USER = str(config.get(section, 'user'))
            if config.has_option(section, 'pass'):
                EMAIL_HOST_PASSWORD = str(config.get(section, 'pass'))
            del config, section
    except:
        print('Email config ini was not loaded correctly!')

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': INPUT_PASSWORD_MIN_LENGTH,
        },
    },
    {
        'NAME': 'rpgsite.validators.MaximumLengthValidator',
        'OPTIONS': {
            'max_length': INPUT_PASSWORD_MAX_LENGTH,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
]

# Logging to `secret/logs/rpgsite.log` file

LOG_FILENAME = os.path.join(SECRET_DIR, 'logs', 'rpgsite.log')
LOG_LEVEL = 'DEBUG'
LOG_ENABLED = True

# Logging configuration

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_log_enabled': {
            '()': 'apps.tools.logging_filters.RequireLogEnabled',
        }
    },
    'formatters': {
        'django.server': {
            'format': '[%(asctime).16s] %(message)s',
        },
        'rpgsite': {
            'format': '[%(asctime).16s][%(levelname)s] %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'rpgsite_file': {
            'level': LOG_LEVEL,
            'filters': ['require_log_enabled'],
            'class': 'logging.FileHandler',
            'filename': LOG_FILENAME,
            'formatter': 'rpgsite',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins', 'rpgsite_file'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server', 'rpgsite_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'rpgsite': {
            'handlers': ['django.server', 'rpgsite_file'],
            'level': 'DEBUG',
        },
    }
}

# django-emoji configuration

EMOJI_IMG_TAG = '<img src="{0}" alt="{1}" title="{2}" class="emoji" />'
EMOJI_ALT_AS_UNICODE = True
EMOJI_REPLACE_HTML_ENTITIES = True

# Other misc settings

TOOLS_LOGGER_NAME = 'rpgsite'
BEAUTIFULSOUP_PARSER = 'lxml'

# WhiteNoise configuration
# (used for serving static files when DEBUG=False)

if USE_WHITENOISE:
    _index_1 = INSTALLED_APPS.index('django.contrib.staticfiles')
    INSTALLED_APPS.insert(_index_1, 'whitenoise.runserver_nostatic')
    _index_2 = MIDDLEWARE.index('django.middleware.security.SecurityMiddleware')
    MIDDLEWARE.insert(_index_2 + 1, 'whitenoise.middleware.WhiteNoiseMiddleware')

