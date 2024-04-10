
import os
from pathlib import Path
from decouple import config
from datetime import timedelta
from pathlib import Path
import dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = os.path.join(BASE_DIR,'.env')
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)
    
    
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEBUG = os.environ.get("DEBUG") != "False"


ALLOWED_HOSTS = ["127.0.0.1", "localhost",".vercel.app", ".now.sh"]
# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]
#ALLOWED_HOSTS = ['*']
# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop.apps.ShopConfig',
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
    'whitenoise.runserver_nostatic',
    'djoser',
    'react',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
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
]

ROOT_URLCONF = 'myshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
         #
         "DIRS": [BASE_DIR / "templates"],
         #       'DIRS': [],
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


#WSGI_APPLICATION = 'myshop.wsgi.application'
WSGI_APPLICATION = 'myshop.wsgi.app'

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'postgres',  # Replace 'your_database_name' with your database name
#        'USER': 'postgres',       # Replace 'your_username' with your database username
#        'PASSWORD': 'postgres',   # Replace 'your_password' with your database password
#        'HOST': 'localhost',           # Replace 'localhost' with your database host if not running locally
#        'PORT': '5432',                    # Replace '' with your database port if not using the default port
#
#    }
#}

DATABASES = {
    'default': {        
        'ENGINE': os.environ["DB_ENGINE"],
        'NAME': os.environ["DB_NAME"],
        'USER': os.environ["DB_USER"],
        'PASSWORD': os.environ["DB_PASSWORD"],
        'HOST': os.environ["DB_HOST"],
        'PORT': os.environ["DB_PORT"],
    }
}
STATIC_URL = '/static/'
# Directory where collected static files will be stored.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_build', 'static')

#STATIC_URL = '/static/'
#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'frontend', 'dist'),
#    os.path.join(BASE_DIR, 'frontend', 'public'),
#    # Add other directories as needed
#]

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')


ADMIN_URL = config('DJANGO_ADMIN_URL', default='admin')
APPEND_SLASH = True

#REACT_BASE_TEMPLATE = BASE_DIR / 'templates' / 'base.html'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

WHITENOISE_INDEX_FILE = True
WHITENOISE_ROOT = STATIC_ROOT
WHITENOISE_ALLOW_ALL_ORIGINS = True

# Media settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}


CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOW_CREDENTIALS = True
AUTHENTICATION_BACKENDS ={
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
}

SITE_ID = 1
AUTH_USER_MODEL = 'accounts.CustomUser'

#AUTH_USER_MODEL = "accounts.CustomUser"
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'username-reset/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SEND_CONFIRMATION_EMAIL' :True,
    'SERIALIZERS': {},
    'USER_CREATE_PASSWORD_RETYPE' : True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION' :True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION' :True,
    'SEND_CONFIRMATION_EMAIL' :True,
    'SERIALAZERS':{  }
}
# app password: vxfnflimsnbvgfvx
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "sergeyitalykiev@gmail.com"
EMAIL_HOST_PASSWORD = "vxfnflimsnbvgfvx"
EMAIL_USE_TLS = True


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

    'AUTH_HEADER_TYPES': ('Bearer'),
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

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'site_cache'),
    }
}