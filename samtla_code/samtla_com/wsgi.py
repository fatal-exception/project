"""
WSGI config for samtla_com project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os, sys

sys.path.append('/home/mhroot/public_www/samtla_com')
sys.path.append('/home/mhroot/public_www/samtla_com/samtla_com')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "samtla_com.settings")

application = get_wsgi_application()
