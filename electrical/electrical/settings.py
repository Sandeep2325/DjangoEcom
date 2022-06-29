"""
Django settings for electrical project.

Generated by 'django-admin startproject' using Django 3.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
import datetime
from pathlib import Path
#from django.utils.encoding import python_2_unicode_compatible, smart_text
#from django.config import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2x+5j9-5@8^tvzl-l--2%k_m!1ne!okdey#_rp8&v!@f=n0gf)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost','127.0.0.1','162.240.55.20','localhost:3000','499f-116-74-253-32.in.ngrok.io']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'admin_actions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'embed_video',
    'app1',
    'chartjs',
    'corsheaders',
    'rest_framework',
    # 'drf_yasg',
    'django_filters',
    # 'rest_framework.authtoken',
    'rest_auth',
    'allauth',
    # 'allauth.account',
    'rest_auth.registration',
    'ckeditor',
    'django_summernote',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.github',
    # 'allauth.socialaccount.providers.twitter',

]
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

CORS_ORIGIN_WHITELIST = [
    'http://127.0.0.1:8000','http://162.240.55.20','http://localhost:3000',"https://499f-116-74-253-32.in.ngrok.io"
]
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000','http://162.240.55.20','http://localhost:3000',"https://499f-116-74-253-32.in.ngrok.io"]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True


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
    "x-requested-with",
]
ROOT_URLCONF = 'electrical.urls'
AUTH_USER_MODEL = 'app1.User'
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000000
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [

                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',

            ],
        },
    },
]
""" AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
) """
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'users.serializers.CustomRegisterSerializer',
}
# CUSTOM_PASSWORD_RESET_CONFIRM = 'desired URL'
# LOGIN_URL = 'https://localhost:8000/dj-rest-auth/login'
AUTHENTICATION_BACKEND = [

    'django.contrib.auth.backends.ModelBackend',

    'allauth.account.auth_backends.AuthenticationBackend',

    # 'django_facebook.auth_backends.FacebookBackend',

    # 'social_core.backends.facebook.FacebookOAuth2',

]
# ACCOUNT_AUTHENTICATION_METHOD = "email"
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = False
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

WSGI_APPLICATION = 'electrical.wsgi.application'
ADMIN_ORDERING = [
    ('app1', [
        'User',
        'Category',
        'Attributes',
        'Product',
        'sales',
        'order',
        'Address',
        'Rating',
        'Coupon',
        'Banner',
        'Blog',
        'FAQ',
        'customer_message',
        'MailText',
        'image',
    ]),
]


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'electrical02',
        'USER': 'root',
        'PASSWORD': 'mySqlServer@#$432',#mySqlServer@#$432
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}
""" DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'electrical6',
       'USER': 'postgres',
       'PASSWORD': 'sandeep',
       'HOST': 'localhost',
       'PORT': '5432',
   }
}  """
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

REST_FRAMEWORK = {
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    # ],
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'dj_rest_auth.jwt_auth.JWTCookieAuthentication',),
    # 'DEFAULT_PERMISSION_CLASSES':
    #     ('rest_framework.permissions.IsAuthenticated',),

    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework_jwt.authentication.JSONWebTokenAuthentication',

    # ),
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework.authentication.BasicAuthentication',
    # ],
    'DEFAULT_PAGINATION_CLASS': 
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'my-app-auth'
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'users.serializers.CustomUserDetailsSerializer',
}
# JSONWebToken Settings
JWT_AUTH = {
    'JWT_ENCODE_HANDLER':
    'rest_framework_jwt.utils.jwt_encode_handler',
    'JWT_DECODE_HANDLER':
    'rest_framework_jwt.utils.jwt_decode_handler',
    'JWT_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_payload_handler',
    'JWT_PAYLOAD_GET_USER_ID_HANDLER':
    'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',
    'JWT_RESPONSE_PAYLOAD_HANDLER':
    'rest_framework_jwt.utils.jwt_response_payload_handler',
    'JWT_VERIFY': True,
    'JWT_VERIFY_EXPIRATION': True,
    # Time for expiration of token
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=10000),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

COMPRESS_PRECOMPILERS = (('text/x-scss', 'django_libsass.SassCompiler'),)
# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
# other finders..'compressor.finders.CompressorFinder',)
STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder',
                       'django.contrib.staticfiles.finders.AppDirectoriesFinder',)
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

MEDIA_URL = '/image/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'image')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
# EMAIL_USE_SSL=FALSE
EMAIL_PORT = 587
EMAIL_HOST_USER = "gowdasandeep8105@gmail.com"
# EMAIL_HOST_PASSWORD = 'Sandeep@1234'
EMAIL_HOST_PASSWORD = 'atkzlpfgzcvpdhai'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
# AUTH_PROFILE_MODULE = 'django_facebook.FacebookProfile'
# SITE_ID = 1
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#BOOTSTRAP_ADMIN_SIDEBAR_MENU = False
JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Prakash Electricals",

    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Prakash Electricals",

    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Prakash Electricals",
    
    }
