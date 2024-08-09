import os
from pathlib import Path
from decouple import config
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
from shop.loadimages_tos3 import LoadImagesToS3
from distutils.util import strtobool
import os
from celery.schedules import crontab


load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = bool(strtobool(os.getenv('DEBUG', 'True')))
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_DEFAULT_ACL = 'public-read'
AWS_QUERYSTRING_AUTH = False  # needed for ckeditor with S3
AWS_S3_FILE_OVERWRITE = False  # False to avoid overwriting files
#AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_MEDIA_LOCATION = os.getenv('AWS_MEDIA', 'media')  # Default to 'media' if not specified
AWS_LOCATION = 'staticfiles_build/static/'
AWS_TEMPLATES = f'https://{AWS_S3_CUSTOM_DOMAIN}/templates/'
USE_S3 = bool(strtobool(os.getenv('USE_S3', 'True')))
AWS_FRONTEND_DOMAIN = f"https://{AWS_S3_CUSTOM_DOMAIN}"
VERCEL_DOMAIN = os.getenv('VERCEL_DOMAIN')
LOCAL_HOST = os.getenv('LOCAL_HOST')
TELEGRAM_BOT_TOKEN=os.getenv('NOTIFICATIONS_API')
SAYINGS_FILE_PATH = os.path.join(BASE_DIR, 'order', 'sayings.txt')
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=31536000, s-maxage=31536000, must-revalidate'
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    VERCEL_DOMAIN,
    AWS_FRONTEND_DOMAIN,
]
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS=0
INTERNAL_IPS = ["127.0.0.1", "localhost", '::1']
ALLOWED_HOSTS = ['127.0.0.1', '.vercel.app', 'localhost']

# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
    'order',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'knox',
    'cart',
    'accounts',
    'djoser',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'storages',
    'imagekit',
    'drf_yasg',
    'django_filters',
    "phonenumber_field",
    "anymail",
    'myshop',
      # "debug_toolbar",

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',

]
# DIRS = [AWS_TEMPLATES]

ROOT_URLCONF = 'myshop.urls'
WSGI_APPLICATION = 'myshop.wsgi.app'

DIRS = [os.path.join(BASE_DIR, 'templates'),
        #        AWS_TEMPLATES,

        ]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': DIRS,
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

# WSGI_APPLICATION = 'myshop.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DATABASE'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT'),
    }
}

if USE_S3:
    # LoadImagesToS3().copy_local_media_to_s3(os.path.join(BASE_DIR, 'media'))
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    # STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    IMAGEKIT_DEFAULT_CACHEFILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_MEDIA_LOCATION}/'
else:
    # Local static file settings
    MEDIA_URL = 'media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    #    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # Use whitenoise for serving static files
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    STATIC_URL = '/static/'  # URL to serve static files
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')
#    WHITENOISE_ROOT = STATIC_ROOT
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'dist'),  # Directory containing main.js and main.css
    os.path.join(BASE_DIR, 'dist', 'assets'),  # Directory containing other assets (images, etc.)
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Additional Whitenoise settings
WHITENOISE_INDEX_FILE = True
WHITENOISE_ALLOW_ALL_ORIGINS = True
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 6
}

AUTHENTICATION_BACKENDS = {
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
}

SITE_ID = 3
AUTH_USER_MODEL = 'accounts.CustomUser'

# AUTH_USER_MODEL = "accounts.CustomUser"
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username-reset/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'SERIALIZERS': {},
    'USER_CREATE_PASSWORD_RETYPE': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'SEND_CONFIRMATION_EMAIL': True,
    'SERIALAZERS': {}
}


ANYMAIL = {
    "MAILGUN_API_KEY": os.getenv('MAILGUN_API_KEY'),
    "MAILGUN_SENDER_DOMAIN": os.getenv('MAILGUN_SENDER_DOMAIN'),
      
}
EMAIL_TIMEOUT = 60  # 60 seconds


EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_FROM_EMAIL = os.getenv('MAILGUN_SMTP_USERNAME')
SERVER_EMAIL = os.getenv('MAILGUN_SMTP_USERNAME')


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# DEBUG_TOOLBAR_CONFIG = {
#    'SHOW_TOOLBAR_CALLBACK': lambda request: DEBUG,  # Only show toolbar in DEBUG mode
# }
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REDIS_CACHE_LOCATION = os.getenv('REDIS_CACHE_LOCATION', 'redis://localhost:6379/1')
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_CACHE_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {
                'max_connections': 100,  # Increase if needed
                'retry_on_timeout': True,
            },
            'SOCKET_CONNECT_TIMEOUT': 5,  # seconds
            'SOCKET_TIMEOUT': 5,  # seconds
        },
        'KEY_PREFIX': 'imdb',
        'TIMEOUT': 60 * 15,  # Cache timeout in seconds (e.g., 15 minutes)
    }
}

# Celery configuration
CELERY_BROKER_URL = os.getenv('REDIS_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

CELERY_IMPORTS = ('order.tasks',)
CELERY_BEAT_SCHEDULE = {
    'update-order-statuses-every-minute': {
        'task': 'order.tasks.update_order_statuses_task',
        'schedule': crontab(minute='*/1'),  # Run every minute
    },
}


#CELERY_WORKER_CANCEL_LONG_RUNNING_TASKS_ON_CONNECTION_LOSS = True

BROKER_POOL_LIMIT = None  # Adjust based on your needs
CELERY_WORKER_POOL_RESTARTS = True
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_WORKER_CANCEL_LONG_RUNNING_TASKS_ON_CONNECTION_LOSS = True
BROKER_TRANSPORT_OPTIONS = {
    'fanout_prefix': True,
    'fanout_patterns': True,
    'max_connections': 50,  # Increase if needed
    'socket_keepalive': True,
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}