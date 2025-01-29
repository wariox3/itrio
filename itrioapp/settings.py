from pathlib import Path
from datetime import timedelta
from decouple import config
import os
from utilidades.manejador_errores import WebServiceHandler
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-my80p16^62e976wt)x8avn6klib1vfa#x*_z$%ae*+can(o)v1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

SHARED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django_tenants',
    'contenedor',
    'seguridad',
)

TENANT_APPS = (
    'general',
    'contabilidad',
    'cartera',
    'transporte',
    'humano',
    'inventario',
    'ruteo'
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',   
    'django_filters',
    'drf_yasg',
    'django_tenants',
    "corsheaders",
    'contenedor',
    'seguridad',
    'general',
    'contabilidad',
    'cartera',
    'transporte',
    'inventario',
    'humano',
    'ruteo'
]

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'itrioapp.urls'

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

WSGI_APPLICATION = 'itrioapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
        'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_CLAVE'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
    }
}


DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

TENANT_MODEL = "contenedor.Contenedor" # app.Model
TENANT_DOMAIN_MODEL = "contenedor.Dominio"  # app.Model

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

#STATIC_URL = 'static/'
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'EXCEPTION_HANDLER': 'itrioapp.exceptions.custom_exception_handler',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=12),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

AUTH_USER_MODEL = 'seguridad.User'

CORS_ALLOWED_ORIGINS = [
    "https://example.com",
    "https://sub.example.com",
    "http://example.com",
    "http://sub.example.com",
    "http://localhost:8080",
    'http://localhost:4200',
    'http://localhost:8081',
    "http://127.0.0.1:9000",
    "http://127.0.0.1:8000",
    "http://159.203.62.234",
    "http://179.15.105.37",
    "http://159.203.57.104",
    "http://138.197.140.230",
    "http://reddocapi.online",
    "http://reddoc.online",
    "http://reddoc.co",
    "https://reddoc.com.co",
    "https://reddocapi.co",
    "http://190.249.212.131",
    "https://ruteo.co",
    "http://ruteo.online",
]


CORS_ALLOWED_ORIGIN_REGEXES = [
    #r"^https?://(\w+\.)?muup\.online$",
    r"^https?://(\w+\.)?reddoc\.online$",
    r"^https?://(\w+\.)?reddoc\.co$",
    r"^https?://(\w+\.)?reddoc\.com\.co$",
    r"http?://(\w+\.)?localhost:4200"
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with"
]

'''LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
    },
}'''


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'web_service': {
            'level': 'ERROR',
            'class': 'utilidades.manejador_errores.WebServiceHandler',
            'url': 'http://niquel.semantica.com.co/api/error/nuevo',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['web_service'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}