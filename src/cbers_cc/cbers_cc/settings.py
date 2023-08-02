

from datetime import timedelta
from pathlib import Path
import os
import environ
env = environ.Env()
environ.Env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', default=env('SECRET_KEY'))


# SECURITY WARNING: don't run with debug turned on in production!
ENV = os.getenv('ENV', default=env('ENV'))
DEBUG = True if 'DEV' not in ENV and 'PROD' not in ENV else False
# DEBUG = False


ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # my apps
    'authtoken.apps.AuthtokenConfig',
    'common.apps.CommonConfig',
    'cbers_cc_plugin.apps.CbersCcPluginConfig',
        
    # lib apps
    'rest_framework',
    'rest_framework_simplejwt',
    "rest_framework_api_key",
    "django_filters",
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

ROOT_URLCONF = 'cbers_cc.urls'

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

WSGI_APPLICATION = 'cbers_cc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=django,public'
        },
        'NAME': os.getenv('DB_NAME', default=env('DB_NAME')),
        'USER': os.getenv('DB_USER', default=env('DB_USER')),
        'PASSWORD': os.getenv('DB_PASSWORD', default=env('DB_PASSWORD')),
        'HOST': os.getenv('DB_HOST', default=env('DB_HOST')),
        'PORT': os.getenv('DB_PORT', default=env('DB_PORT')),
        'TEST': {
            'NAME': 'cbers_cc_backend_test_database',
        },
    },
}


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',
        # 'rest_framework_api_key.permissions.HasAPIKey',
        'common.permissions.IsAuthenticatedOrHasAPIKey',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',        
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20
}

SIMPLE_JWT = {
    'ROTATE_REFRESH_TOKENS': True,
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=6),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),
}
API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"


# Add to create the folders in Path
# Add to create the folders in Path
if ENV == 'LOCAL':
    LOG_FILE_PATH = './local-logs'
else:
    LOG_FILE_PATH = './logs'
    

p = Path(LOG_FILE_PATH).resolve()
p.mkdir(parents=True, exist_ok=True)

LOG_LEVEL = os.getenv('LOG_LEVEL', default=env('LOG_LEVEL'))

LOGGING = {
    'version': 1,
    # 'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s.%(msecs)03d] p%(process)s {%(pathname)s:%(lineno)d} [%(name)-12s] [%(threadName)-14s] [%(levelname)8s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(asctime)s.%(msecs)03d %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'debug3': {
            'level': 'DEBUG',
            # 'class': 'logging.FileHandler',
            'filename': p / 'AppDebug3.log',
            'formatter': 'verbose',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight', # specifies the interval
            'backupCount': 30, # how many backup file to keep, 30 days
        },
        'errors': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': p / 'AppErrors.log',
            'formatter': 'verbose'
        },
        'file': {
            'level': LOG_LEVEL,
            'filename': p / 'AppGeneral.log',
            'formatter': 'verbose',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight', # specifies the interval
            'backupCount': 14, # how many backup file to keep, 14 days
        },
    },
    'loggers': {
        '': {
            'handlers': ['debug3', 'errors'],
            'level': 'DEBUG',
            # 'propagate': True,
        },
        'django': {
            'handlers': ['file', 'console', 'debug3', 'errors'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}


if DEBUG:
    # make all loggers use the console.
    for logger in LOGGING['loggers']:
        LOGGING['loggers'][logger]['handlers'] = ['console']


### CELERY
CELERY_BROKER_URL = os.getenv('CELERY_BROKER', default=env('CELERY_BROKER'))
CELERY_RESULT_BACKEND = os.getenv('CELERY_BACKEND', default=env('CELERY_BACKEND'))