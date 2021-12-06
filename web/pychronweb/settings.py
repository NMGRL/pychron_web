"""
Django settings for pychronweb project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'Foobar')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG", default=0)))

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(' ')

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap3"
CRISPY_TEMPLATE_PACK = "bootstrap3"
DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap.html"

# Application definition

INSTALLED_APPS = [
    'samples.apps.SamplesConfig',
    'projects.apps.ProjectsConfig',
    'materials.apps.MaterialsConfig',
    'principal_investigators.apps.PrincipalInvestigatorsConfig',
    'analyses.apps.AnalysisConfig',
    'events.apps.EventsConfig',
    'users',

    'crispy_forms',
    'django_tables2',
    'django_filters',
    'bootstrap3',
    'leaflet',
    'dal',
    'dal_select2',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'pychronweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # BASE_DIR / 'samples/templates',
            # BASE_DIR / 'projects/templates',
            # BASE_DIR / 'events/templates',
            BASE_DIR / 'templates'
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

WSGI_APPLICATION = 'pychronweb.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


engine = 'sql_server.pyodbc' if os.environ.get('DATABASE_KIND', 'mysql') == 'mssql' else 'mysql.connector.django'

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # }
    'default': {
        'ENGINE': engine,
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Denver'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
LOGIN_REDIRECT_URL = 'signup'
LOGIN_URL = 'accounts/login'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
PYCHRON_DATA_ORGANIZATION = 'NMGRLData'
ANALYSES_DEBUG = False
LEAFLET_CONFIG = {
    # 'SPATIAL_EXTENT': (5.0, 44.0, 7.5, 46),
    'DEFAULT_CENTER': (35, -106.0),
    'DEFAULT_ZOOM': 8,
    'MIN_ZOOM': 2,
    'MAX_ZOOM': 20,
    'DEFAULT_PRECISION': 6,
    'TILES': []
    #     ('USGS Topo',
    #      'https://basemap.nationalmap.gov/arcgis/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}',
    #      'Tiles courtesy of the <a href="https://usgs.gov/">U.S. Geological Survey</a>'),
    #     ('USGS Imagery',
    #      'https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}',
    #      'Tiles courtesy of the <a href="https://usgs.gov/">U.S. Geological Survey</a>'),
    #     ('OpenStreetMap Mapnik',
    #      'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    #      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'),
    #     ('OpenTopMap',
    #      'https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
    #      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'),
    #     ('Stamen Terrain',
    #      'https://stamen-tiles-{s}.a.ssl.fastly.net/terrain-background/{z}/{x}/{y}{r}.png',
    #      'Map tiles by <a href="http://stamen.com">Stamen Design</a>, '
    #      '<a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a '
    #      'href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'),
    #     ('Google Streets', 'http://mt0.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', '&copy Google'),
    #     ('Google Hybrid', 'http://mt0.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', '&copy Google'),
    #     ('Google Satelite', 'http://mt0.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', '&copy Google'),
    #     ('Google Terrain', 'http://mt0.google.com/vt/lyrs=p&x={x}&y={y}&z={z}', '&copy Google'),
    # ]
}

# from glob import glob

# GDAL_LIBRARY_PATH=glob('/usr/lib/libgdal.so.*')[0]
# GEOS_LIBRARY_PATH=glob('/usr/lib/libgeos_c.so.*')[0]
