"""
Django settings for cartoview project.

Generated by "django-admin startproject" using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys
from distutils.util import strtobool

import dj_database_url
from celery.schedules import crontab
from tzlocal import get_localzone

from cartoview.log_handler import get_logger

logger = get_logger(__name__)
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SETTINGS_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "SECRET_KEY", "c8(50gzg=^s6&m73&801%+@$24+&8duk$^^4ormfkbj!*q86fo")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(os.getenv("DEBUG", "True"))

ALLOWED_HOSTS = eval(os.getenv("ALLOWED_HOSTS", '["*"]'))

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # third-party apps
    "guardian",
    "channels",
    "crispy_forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_framework",
    "rest_framework_swagger",
    "rest_framework.authtoken",
    "django_filters",
    "generic_relations",
    # wagtail apps
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "wagtail.contrib.modeladmin",
    "wagtailmenus",
    "wagtail.contrib.styleguide",
    "wagtail.contrib.settings",
    "modelcluster",
    "taggit",
    'wagtailfontawesome',
    'wagtail_blocks',

    # cartoview apps
    "cartoview",
    "cartoview.base_resource",
    "cartoview.geonode_oauth",  # Our custom provider
    "cartoview.app_manager",
    "cartoview.api",
    "cartoview.connections",
    "cartoview.layers",
    "cartoview.maps",
    "cartoview.cms",
]

# channels settings
ASGI_APPLICATION = os.getenv(
    "ASGI_APPLICATION", "cartoview.routing.application")

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "wagtail.core.middleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = os.getenv("ROOT_URLCONF", "cartoview.urls")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                "wagtailmenus.context_processors.wagtailmenus",
                "cartoview.context_processors.version",
            ]
        },
    }
]

WSGI_APPLICATION = os.getenv("WSGI_APPLICATION", "cartoview.wsgi.application")

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASE_URL = os.getenv('DATABASE_URL', None)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<database_name>',
        'USER': '<user>',
        'PASSWORD': '<pass>',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(
        DATABASE_URL, conn_max_age=0)

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},  # noqa
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},  # noqa
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},  # noqa
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = os.getenv("LANGUAGE_CODE", "en-us")

TIME_ZONE = os.getenv("TIME_ZONE", get_localzone().zone)

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ("en", "English"),
    ("ar", "Arabic"),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

# Localization
USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, os.pardir, "static_root")
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
STATICFILES_DIRS = []
# auth settings
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)
ACCOUNT_EMAIL_VERIFICATION = os.getenv("ACCOUNT_EMAIL_VERIFICATION", "none")
ANONYMOUS_USER_NAME = os.getenv("ANONYMOUS_USER_NAME", "AnonymousUser")
GUARDIAN_RAISE_403 = True
OAUTH_SERVER_BASEURL = os.getenv("OAUTH_SERVER_BASEURL", "<BASE_SERVER_URL>")
LOGIN_REDIRECT_URL = os.getenv("LOGIN_REDIRECT_URL", "/")
ANONYMOUS_GROUP_NAME = os.getenv("ANONYMOUS_GROUP_NAME", "public")

WAGTAIL_SITE_NAME = os.getenv("WAGTAIL_SITE_NAME", "Cartoview")
SITE_ID = 1

# django rest framework settings
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_METADATA_CLASS": "rest_framework.metadata.SimpleMetadata",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
        # "cartoview.api.permissions.BaseObjectPermissions",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FileUploadParser",
        "rest_framework_xml.parsers.XMLParser",
        "rest_framework_yaml.parsers.YAMLParser",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework_xml.renderers.XMLRenderer",
        "rest_framework_yaml.renderers.YAMLRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
        # "rest_framework.filters.DjangoObjectPermissionsFilter",
    )
}
# django Crispy forms settings
CRISPY_TEMPLATE_PACK = "bootstrap4"
# connections app settings
CARTOVIEW_CONNECTION_HANDLERS = {
    "BASIC": "cartoview.connections.auth.simple.BasicAuthSession",
    "DIGEST": "cartoview.connections.auth.simple.DigestAuthSession",
    "TOKEN": "cartoview.connections.auth.token.TokenAuthSession",
    "NoAuth": "cartoview.connections.auth.base.NoAuthClass"
}
CARTOVIEW_SERVER_HANDLERS = {
    "ARCGIS_MSL": "cartoview.connections.servers.arcgis.ArcGISLayer",
    "ARCGIS_FSL": "cartoview.connections.servers.arcgis.ArcGISLayer",
    "OGC-WMS": "cartoview.connections.servers.ogc.OGCServer",
    "OGC-WFS": "cartoview.connections.servers.ogc.OGCServer",
    "GEOJSON": "cartoview.connections.servers.ogr_handler.GeoJSON",
    "KML": "cartoview.connections.servers.ogr_handler.KML",
}
CARTOVIEW_CONNECTIONS = {
    "connection_handlers": CARTOVIEW_CONNECTION_HANDLERS,
    "server_handlers": CARTOVIEW_SERVER_HANDLERS,
    "proxy": {
        "default_headers": {
            "Accept": "*",
            "Accept-Language": "*",
        },
        "timeout": int(os.getenv("PROXY_TIMEOUT", "4")),
    }
}

# cache settings
CACHE_ENABLED = strtobool(os.getenv("CACHE_ENABLED", "False"))
if CACHE_ENABLED:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.db.DatabaseCache",
            "LOCATION": "cartoview_cache",
        }
    }

# apps settings
APPS_DIR = os.path.join(BASE_DIR, os.pardir, "cartoview_apps")
STAND_ALONE = strtobool(os.getenv("STAND_ALONE", "False"))
if STAND_ALONE:

    # NOTE: load cartoview apps
    if APPS_DIR not in sys.path:
        sys.path.append(APPS_DIR)
    from cartoview.app_manager.config import CartoviewApp  # noqa

    CartoviewApp.load(apps_dir=APPS_DIR)
    for app in CartoviewApp.objects.get_active_apps().values():
        try:
            # ensure that the folder is python module
            app_module = __import__(app.name)
            app_dir = os.path.dirname(app_module.__file__)
            app_settings_file = os.path.join(app_dir, "settings.py")
            libs_dir = os.path.join(app_dir, "libs")
            if os.path.exists(app_settings_file):
                app_settings_file = os.path.realpath(app_settings_file)
                exec(open(app_settings_file).read())
            if os.path.exists(libs_dir) and libs_dir not in sys.path:
                sys.path.append(libs_dir)
            if app.name not in INSTALLED_APPS:
                INSTALLED_APPS += (app.name.__str__(),)
        except Exception as e:
            logger.error(str(e))
# file uploads settings
DATA_UPLOAD_MAX_MEMORY_SIZE = int(os.getenv(
    'DATA_UPLOAD_MAX_MEMORY_SIZE˝', "1073741824"))
FILE_UPLOAD_MAX_MEMORY_SIZE = int(os.getenv(
    'FILE_UPLOAD_MAX_MEMORY_SIZE', "1073741824"))  # maximum file upload 1GB

# Celery application definition
ASYNC_ENABLED = strtobool(os.getenv('ASYNC_ENABLED', 'False'))
RABBITMQ_SIGNALS_BROKER_URL = os.getenv(
    'RABBITMQ_SIGNALS_BROKER_URL', 'amqp://localhost:5672')
REDIS_SIGNALS_BROKER_URL = os.getenv(
    'REDIS_SIGNALS_BROKER_URL', 'redis://localhost:6379/0')
LOCAL_SIGNALS_BROKER_URL = 'memory://'
CELERY_BROKER_URL = os.getenv(
    'CELERY_BROKER_URL', REDIS_SIGNALS_BROKER_URL if ASYNC_ENABLED else LOCAL_SIGNALS_BROKER_URL)
if ASYNC_ENABLED:
    CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_RESULT_PERSISTENT = False

# Allow to recover from any unknown crash.
CELERY_ACKS_LATE = True

# Set this to False in order to run async
CELERY_TASK_ALWAYS_EAGER = False if ASYNC_ENABLED else True
CELERY_TASK_IGNORE_RESULT = True
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULE = {
    'validate-resources-task': {
        'task': 'cartoview.connections.tasks.validate_servers',
        'schedule': crontab(minute=59, hour=23),
    },
}
CELERY_TASK_RESULT_EXPIRES = 43200
CELERY_MESSAGE_COMPRESSION = 'gzip'
CELERY_MAX_CACHED_RESULTS = 32768


try:
    from .local_settings import *  # noqa
except ImportError:
    pass
