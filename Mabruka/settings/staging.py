from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ADMINS = ('Marco Nila', 'sainoba@gmail.com')

ALLOWED_HOSTS = ['mabruka.sainoba.webfactional.com']

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
# STATIC_ROOT = BASE_DIR.child('staticfiles')
STATIC_ROOT = BASE_DIR.child('staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (BASE_DIR.child('static'),)

# Configuración del correo
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'sainoba@gmail.com'
EMAIL_HOST_PASSWORD = 'gphesueuhkjicisv'
DEFAULT_FROM_EMAIL = 'sainoba@gmail.com'
