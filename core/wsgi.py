"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
load_dotenv()
from django.core.wsgi import get_wsgi_application

debug =  os.environ.get("DEBUG", "true")
if debug == "true":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.local")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.production")

application = get_wsgi_application()
