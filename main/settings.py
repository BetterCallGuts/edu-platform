from pathlib import Path
import os
from django.contrib.messages import constants as messages



# SECURTY AND DEBUG
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-(hr%r^=#=%+ij*uk6y_-w4pf4njzbxb0z9g)r47gyq8xvf-+q='
DEBUG = True
ALLOWED_HOSTS = [

    "www.talebazhari.com",
    "talebazhari.com",
      '72.60.89.229',
      "127.0.0.1",
      "localhost",
      ]

# LANGUAGES AND TIME ZONES 
LANGUAGE_CODE = 'en-us'
LANGUAGES = [
    ('en', 'English'),
    ('ar', 'Arabic'),
    # ('fr', 'French'),
    # ('es', 'Spanish'),
]
TIME_ZONE = 'Africa/Cairo'
USE_I18N = True
USE_L10N = True
# USE_TZ = True
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]


# STATIC AND MEDIA FILES
STATIC_URL = 'static/' 
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_dir_1'),#/   \\
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'




# GOLABAL VARS
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SITE_HEADER        = 'MySite'
SITE_TITLE         = 'MySite'
SITE_INDEX_TITLE   = 'MySite'
AUTH_USER_MODEL    = 'users.User'
LOGOUT_REDIRECT_URL= '/'
LOGIN_REDIRECT_URL = '/'
X_FRAME_OPTIONS    = 'SAMEORIGIN'

INSTALLED_APPS = [
    # Third Party admin


    'jazzmin',
    # Enternal
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    # Third Party
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',

    # Local
    "users",
    "course",
    "custom_admin",
    "website",
    
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # for i18n
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

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
                'django.template.context_processors.i18n', # for i18n

                # custom
                "website.context_processors.global_variable"

            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}
DATA_UPLOAD_MAX_MEMORY_SIZE = 524288000   # 500 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 524288000

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },


]
MESSAGE_TAGS = {
    messages.DEBUG: 'secondary',     
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',       
}
