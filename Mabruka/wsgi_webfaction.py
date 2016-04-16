"""
WSGI config for Mabruka project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
import sys
import site

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir(
    '/home/sainoba/.virtualenvs/Mabruka/lib/python3.5/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/sainoba/webapps/mabruka_wsgi/Mabruka')
sys.path.append('/home/sainoba/webapps/mabruka_wsgi/Mabruka/Mabruka')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Mabruka.settings.staging")

activate_env = os.path.expanduser(
    "/home/sainoba/.virtualenvs/Mabruka/bin/activate_this.py")
# execfile(activate_env, dict(__file__=activate_env))
exec(compile(open(activate_env, "rb").read(), activate_env, 'exec'),
     dict(__file__=activate_env))

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
