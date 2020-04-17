"""
Django settings for arbeid project.

Generated by 'django-admin startproject' using Django 2.2.10.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

from delt.scopes import SCOPES as DELTSCOPES

from .modeselektor import ArnheimDefaults

# General Debug or Production Settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#             _____  _   _ _    _ ______ _____ __  __
#       /\   |  __ \| \ | | |  | |  ____|_   _|  \/  |
#      /  \  | |__) |  \| | |__| | |__    | | | \  / |
#     / /\ \ |  _  /| . ` |  __  |  __|   | | | |\/| |
#    / ____ \| | \ \| |\  | |  | | |____ _| |_| |  | |
#   /_/    \_\_|  \_\_| \_|_|  |_|______|_____|_|  |_|
#                  Arnheim Settings


    
defaults = ArnheimDefaults()
ARNHEIM = defaults
# Zarr Related
ZARR_COMPRESSION = defaults.zarr_compression
ZARR_DTYPE = defaults.zarr_dtype

# Matrise Related
MATRISE_APIVERSION = "0.1"
MATRISE_FILEVERSION = "0.1"

#Bord Related
BORD_APIVERSION = "0.1"
BORD_FILEVERSION = "0.1"

# Postgres Settings
POSTGRES_DB = os.environ.get("POSTGRES_DB", None)
POSTGRES_USER = os.environ.get("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")
POSTGRES_HOST =  os.environ.get("POSTGRES_SERVICE_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_SERVICE_PORT_POSTGRESPORT", 5432)

# Dask Setings =
DASK_SCHEDULER_HOST =  os.environ.get("DASK_SCHEDULER_SERVICE_HOST", "localhost")
DASK_SCHEDULER_PORT = os.environ.get("DASK_SCHEDULER_SERVICE_DASKPORT", 5432)

#             ____  _____  ____  ______ _____ _____  ______ _____
#       /\   |  _ \|  __ \|  _ \|  ____|_   _|  __ \|  ____|  __ \
#      /  \  | |_) | |__) | |_) | |__    | | | |  | | |__  | |__) |
#     / /\ \ |  _ <|  _  /|  _ <|  __|   | | | |  | |  __| |  _  /
#    / ____ \| |_) | | \ \| |_) | |____ _| |_| |__| | |____| | \ \
#   /_/    \_\____/|_|  \_\____/|______|_____|_____/|______|_|  \_\
#                           Arbeider Settings

MODULES = os.environ.get("ARNHEIM_MODULES", "").split(",")


#    _____            _               _
#   |  __ \          (_)             | |
#   | |  | | ___ _ __ ___   _____  __| |
#   | |  | |/ _ \ '__| \ \ / / _ \/ _` |
#   | |__| |  __/ |  | |\ V /  __/ (_| |
#   |_____/ \___|_|  |_| \_/ \___|\__,_|
#       Derived Settings for Django

MEDIA_ROOT = str(defaults.media_path)

# S3 Settings

#S3 Settings
S3_PUBLIC_DOMAIN = defaults.s3_public_domain
AWS_ACCESS_KEY_ID = defaults.s3_key
AWS_SECRET_ACCESS_KEY = defaults.s3_secret
AWS_S3_ENDPOINT_URL  = str(defaults.s3_endpointurl)
AWS_STORAGE_BUCKET_NAME = "test"
AWS_S3_URL_PROTOCOL = defaults.s3_protocol
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_USE_SSL = True
AWS_S3_SECURE_URLS = False # Should resort to True if using in Production behind TLS

ZARR_BUCKET = "zarr"
MEDIA_BUCKET = "media"
FILES_BUCKET = "files"
PARQUET_BUCKET = "parquet"

DEFAULT_PARQUET_STORAGE = defaults.parquet_storage
DEFAULT_ZARR_STORAGE = defaults.zarr_storage
DEFAULT_NAME_GENERATOR = defaults.name_generator
ALLOWED_HOSTS = ["*"]

MEDIA_URL = defaults.media_url
# Overwrite Django Settings
DEBUG = defaults.debug
SECRET_KEY = defaults.secret_key
STORAGE_MODE = defaults.storage
DEFAULT_FILE_STORAGE = defaults.storage_default
# Application definition

MODULES = MODULES + [
    'elements',
    'filters'
]


INSTALLED_APPS = [
    'registration',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_provider',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'channels',
    'kanal',
    'fremmed',
    'herre',
    'due',
    'delt',
    'bord',
    'matrise',
    'jobb',
] + MODULES



MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'arbeid.urls'

CORS_ORIGIN_ALLOW_ALL = True


AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',
    # Uncomment following if you want to access the admin
    'django.contrib.auth.backends.ModelBackend'
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'templates',
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

# Channel layer definitions
# http://channels.readthedocs.io/en/latest/topics/channel_layers.html
CHANNEL_LAYERS = {
    "default": {
        # This example app uses the Redis channel layer implementation channels_redis
        "BACKEND": defaults.channel_backend,
        "CONFIG": {
            "hosts": [(defaults.channel_host, defaults.channel_port)],
        },
    },
}

# ASGI_APPLICATION should be set to your outermost router
ASGI_APPLICATION = 'arbeid.routing.application'
WSGI_APPLICATION = 'arbeid.wsgi.application'


ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = True # Automatically log the user in.


NODE_BACKENDS = {
    "kanal": {
        "autodiscover": True,
        "enforce_catalog": False,
        "enforce_register": False,
        "path": "kanal",
        "base": "nodes",
    },
    "fremmed": {
        "autodiscover": True,
        "enforce_catalog": False,
        "enforce_register": False,
        "path": "fremmed",
        "base": "nodes",
    },
    "kafka": {
        "autodiscover": True,
        "enforce_catalog": False,
        "enforce_register": False,
        "path": "kafka",
        "base": "nodes"
    }
}

ROUTER_BACKENDS = {
    "jobb": {
        "autodiscover": True,
        "enforce_catalog": False,
        "enforce_register": False,
        "path": "jobs"
    },
}

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": defaults.sql_engine,
        "NAME": defaults.db_name,
        "USER": defaults.db_user,
        "PASSWORD":defaults.db_password,
        "HOST": defaults.db_host,
        "PORT": int(defaults.db_port),
        **defaults.db_kwargs
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
    # root logger
        '': {
            'level': defaults.loglevel,
            'handlers': ['console'],
        },
        'oauthlib': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {
        'read': 'Reading all of your Data ',
        'read_starred': "Reading your shared Data",
        'write': 'Modifying all of your Data',
        'can_provision': "Provision",
        'can_start_job': "Can start Nodes",
        'profile': 'Access to your Profile (including Email, Name and Address',
        **DELTSCOPES
        }

}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

LOGIN_REDIRECT_URL = "/"
# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = defaults.static_path
STATIC_URL = defaults.static_url
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

FIXTURE_DIRS =  [ "fixtures"]
