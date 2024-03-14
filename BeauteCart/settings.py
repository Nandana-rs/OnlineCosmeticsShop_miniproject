"""
Django settings for BeauteCart project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
#razorpay payment
# from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z4*i6le@d@7cj2b22+xcc@9e4o61az0!0=14l_6)81&lcqefcm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    #'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'BeauteCartApp',
    ##heregooglestarts
    'oauth2_provider',
    'social_django',
    'allauth',
    'allauth.account',
    #heregoogleends
    'crispy_forms',
    
   

    
    

    #razorpay payment
    # 'razorpay',
    
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #heregooglestarts
    'allauth.account.middleware.AccountMiddleware',
    #heregoogleends
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'BeauteCart.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                #heregooglestarts
                'social_django.context_processors.backends',
                #heregoogleends
                
            ],
        },
    },
]

WSGI_APPLICATION = 'BeauteCart.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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

# Add LOGIN_REDIRECT_URL here
#LOGIN_REDIRECT_URL = 'home'


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
#LOGIN_URL = 'login'  # Assuming 'login' is the name of the URL pattern for your custom login view.

#STATIC_URL = 'static/'
#STATICFILES_DIRS = [
#os.path.join(BASE_DIR,'static')
#]
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#razorpay
RAZOR_KEY_ID = 'rzp_test_CJegkMCy3Kn5Rr'
RAZOR_KEY_SECRET = 'iWFW3jm1HLhZaPLWsZNGpOEW'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL ='/'
LOGOUT_REDIRECT_URL= '/'

# settings.py
AUTH_USER_MODEL = 'BeauteCartApp.CustomUser'

#JAZZMIN_SETTINGS={"show_ui_builder" : True }

#heregooglestarts
OAUTH2_PROVIDER = {
    'APPLICATION_MODEL': 'oauth2_provider.Application',
    'DEFAULT_SCOPES': ['read', 'write'],
}

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '413589767899-a75snc5clgrvvegu20eq70p2lsfc0ut1.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'

AUTHENTICATION_BACKENDS = (
    
   'social_core.backends.google.GoogleOAuth2',
    'allauth.account.auth_backends.AuthenticationBackend',
    
)

SOCIAL_AUTH_URL_NAMESPACE = 'social'
#heregoogleends

#forget password
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'nandanars2024b@mca.ajce.in'  
EMAIL_HOST_PASSWORD = '9946095781nrs'  

#implementing role based acces for product adding by admin & seller
# settings.py

AUTH_PERMISSIONS = {
    'Seller': {
        'add_product': 'Can add product',
    },
    'Administrator': {
        'add_product': 'Can add product',
    },
}

DIALOGFLOW_PROJECT_ID = 'beautebot-pomb'
DIALOGFLOW_LANGUAGE_CODE = 'en'  # Update with your language code
DIALOGFLOW_CREDENTIALS_PATH = 'C:\\Users\\91730\\Downloads\\beautebot-pomb-e99bf2952742.json'










