import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o3g)kj_7u1m$g0!-7&b&u+7-jj%9a0b(8cf8r2afnv&a7k4u=d'

# SECURITY WARNING: don't run with debug turned on in production!
#######

# This section is important for CORS_ORIGIN_ALLOW_ALL 
# pip install django-cors-headers
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', '192.168.62.69', '192.168.100.61', '116.68.205.72', 'mis.digital', '192.168.101.188','localhost', '192.168.101.197']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'YamahaBookingApp',
    'django_filters',
    'corsheaders',
    'channels'
]
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "asgiref.inmemory.ChannelLayer",
#         "ROUTING": "YamahaBookingAPI.parent_routing.channel_routing",
#     }
# }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'YamahaBookingAPI.urls'

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

WSGI_APPLICATION = 'YamahaBookingAPI.wsgi.application'
ASGI_APPLICATION = "routing.application"




# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'YamahaBooking': {
       'NAME': 'yamahan',
       'ENGINE': 'sql_server.pyodbc',
       'HOST': '192.168.100.61',
       'USER': 'sa',
       'PASSWORD': 'dataport',
       'OPTIONS': {
           'driver' : 'SQL Server Native Client 11.0',
           'driver_supports_utf8' : 'True',
           'use_legacy_date_fields': 'True',
           'autocommit': True,
       }
    },
    'LocationTracker': {
       'NAME': 'LocationTracker',
       'ENGINE': 'sql_server.pyodbc',
       'HOST': '192.168.100.62',
       'USER': 'sa',
       'PASSWORD': 'dataport',
       'OPTIONS': {
           'driver' : 'SQL Server Native Client 11.0',
           'driver_supports_utf8' : 'True',
           'use_legacy_date_fields': 'True',
           'autocommit': True,
       }
    },
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MIDDLEWARE_CLASSES = (
    'YamahaBookingApp.CorsMiddleware' 
)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
#CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#      'http://192.168.10/yamahaN/register.php',
# )



STATIC_URL = '/static/'


MEDIA_URL = 'PaySlip/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'PaySlip')



STATIC_DIR = os.path.join(BASE_DIR, 'UploadedMedia')
