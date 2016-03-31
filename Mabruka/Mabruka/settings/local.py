from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#       'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#       'NAME': 'Mabruka',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
#       'USER': 'root',
#       'PASSWORD': 'root',
#       'HOST': 'localhost',                      # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
#       'PORT': '5432',                      # Set to empty string for default.
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = BASE_DIR.child('staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR.child('static'),)

if DEBUG:
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_HOST_USER = 'sainoba@gmail.com'
    EMAIL_HOST_PASSWORD = 'gphesueuhkjicisv'
    DEFAULT_FROM_EMAIL = 'sainoba@gmail.com'

# SwampDragon settings
DRAGON_URL = 'http://localhost:9999/'

REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    'anon': '100/second',
    'user': '100/second',
}