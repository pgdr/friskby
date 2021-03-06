"""
Django settings for friskby project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import pytz 
import os
import dj_database_url
import sys 

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR , tail = os.path.split( os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+xy7&q+xuwnohtv$0)m7rpv7y&3#qndflc_%c%@3_jbx8h3b!4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if os.getenv("FRISKBY_DEBUG"):
    debug_site = os.getenv("FRISKBY_DEBUG")
    if debug_site.lower() == "false":
        DEBUG = False
    elif debug_site.lower() == "true":
        DEBUG = True
    else:
        raise Exception("When setting the FRISKBY_DEBUG env veriable it must be True | False")

ALLOWED_HOSTS = ["friskby.herokuapp.com"]

if DEBUG:
    ALLOWED_HOSTS.append("*")


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'git_version',
    'api_key',
    'sensor'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'friskby.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['friskby/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'friskby.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

if "test" in sys.argv:
    DATABASES = { 'default' : {
        "ENGINE" : "django.db.backends.sqlite3",
        "NAME" : "friskby.sqlite",
        "TEST" : {
            "NAME" : "friskby-test.sqlite"}}}
else:
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if DATABASE_URL:
        DATABASES = { 'default' : dj_database_url.parse( DATABASE_URL ) }
    else:
        raise Exception("The DATABASE_URL environment variable has not bee set")


if False:
    # This should in my opinion also work
    DATABASE_URL = os.environ.get("DATABASE_URL")
    if DATABASE_URL:
        default_db = dj_database_url.parse( DATABASE_URL )
        default_db["TEST"] = {"ENGINE" : "django.db.backends.sqlite3",
                              "NAME" : "friskby-test.sqlite" }
        DATABASES = { "default" : default_db }
    else:
        raise Exception("The DATABASE_URL environment variable has not bee set")


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'



# The Django project is set up to use timezone information; i.e all
# date and time instances should be 'aware' in Python language, and
# everything stored in the database is in UTZ. The timezone setting
# here is only used as a default fallback when interacting with the
# user.
TIME_ZONE = os.environ.get("TZ")
if TIME_ZONE is None:
    raise Exception("Must set time zone variable TZ")


USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)




CORS_ORIGIN_ALLOW_ALL = True
#CORS_URLS_REGEX = r'^/friskby/api/.*$'

