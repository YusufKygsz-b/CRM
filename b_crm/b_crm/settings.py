from pathlib import Path

# dotenv
import os
from dotenv import load_dotenv
load_dotenv() 

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = True
ALLOWED_HOSTS = []

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'notifications',
]

LOCAL_APPS = [
    'website',
    ]

THIRD_PARTY_APPS = [
    "daphne",
    "unfold", 
    "admin_honeypot",
    "honeypot",
]

INSTALLED_APPS = THIRD_PARTY_APPS +  DJANGO_APPS + LOCAL_APPS 

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'b_crm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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



ASGI_APPLICATION = 'b_crm.asgi.application'

CHANNEL_LAYERS = {
    'default':{
        'BACKEND':'channels.layers.InMemoryChannelLayer'
    }
}


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if DEBUG == False:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", ""),
            "USER": os.getenv("DB_USER", ""),
            "PASSWORD": os.getenv("DB_PASS", ""),
            "HOST": os.getenv("DB_HOST", "None"),
            "PORT": os.getenv("DB_PORT", "None"),
        },
    }


from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _
# Configuration unfold codes
UNFOLD = {
    "SITE_TITLE": 'Kaygusuz-CRM',
    "SITE_HEADER": 'B-CRM',

     "SIDEBAR": {
         "show_search": True,  # Search in applications and models names
     },

    "SCRIPTS": [
        lambda request: static("unfold/js/custom_unfold.js"),
    ],
}

DJANGO_NOTIFICATIONS_CONFIG = {
    'SOFT_DELETE': True,
}

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

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'yusufkygsz.b@gmail.com'
# EMAIL_HOST_PASSWORD = '...'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
