"""
Django settings for fantasy project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dj_key = 'django-insecure-dp_3u6)oxtgk5+@6z9l_u2@e#lbupw2fnmcp2dir%2-fe3e9$k'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', dj_key)

DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'stats.apps.StatsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    # 'bootstrap5',
    'channels',
    'channels_redis',
]

# Standard Django middleware with the addition of both
# whitenoise and django_plotly_dash items

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'django_plotly_dash.middleware.BaseMiddleware',
    'django_plotly_dash.middleware.ExternalRedirectionMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fantasy.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'fantasy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


default_db_backhand = "django.db.backends.sqlite3"
default_db_name = os.path.join(BASE_DIR, 'db.sqlite3')

DATABASES = {
    'default': {
        'ENGINE': os.environ.get("DATABASE_ENGINE", default_db_backhand),
        'NAME': os.environ.get('DATABASE_NAME', default_db_name),
        'USER': os.environ.get('DATABASE_USER', ''),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
        'HOST': os.environ.get('DATABASE_HOST', ''),
        'PORT': os.environ.get('DATABASE_PORT', ''),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

pwv = 'django.contrib.auth.password_validation'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': f'{pwv}.UserAttributeSimilarityValidator',
    },
    {
        'NAME': f'{pwv}.MinimumLengthValidator',
    },
    {
        'NAME': f'{pwv}.CommonPasswordValidator',
    },
    {
        'NAME': f'{pwv}.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

CRISPY_TEMPLATE_PACK = 'bootstap4'

ASGI_APPLICATION = 'fantasy.routing.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379),],
        },
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
# For WhiteNoise -> https://whitenoise.readthedocs.io/en/stable/django.html
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "fantasy/static")
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Enabling the use of frames within HTML documents for django_plotly
X_FRAME_OPTIONS = 'SAMEORIGIN'

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

PLOTLY_DASH = {

    # Route used for the message pipe websocket connection
    "ws_route": "dpd/ws/channel",

    # Route used for direct http insertion of pipe messages
    "http_route": "dpd/views",

    # Flag controlling existince of http poke endpoint
    "http_poke_enabled": True,

    # Insert data for the demo when migrating
    "insert_demo_migrations": False,

    # Timeout for caching of initial arguments in seconds
    "cache_timeout_initial_arguments": 60,

    # Name of view wrapping function
    "view_decorator": None,

    # Flag to control location of initial argument storage
    "cache_arguments": True,

    # Flag controlling local serving of assets
    "serve_locally": False,
}

# Staticfiles finders for locating dash app assets and related files
STATICFILES_FINDERS = [

    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
    'django_plotly_dash.finders.DashAppDirectoryFinder',
]

# Plotly components containing static content that should
# be handled by the Django staticfiles infrastructure

PLOTLY_COMPONENTS = [

    # Common components (ie within dash itself) are automatically added

    'dash_core_components',
    'dash_html_components',
    'dash_renderer',

    # django-plotly-dash components
    'dpd_components',
    # static support if serving local assets
    'dpd_static_support',

    # Other components, as needed
    'dash_bootstrap_components',
]
