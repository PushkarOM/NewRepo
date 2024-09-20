"""
WSGI config for Ayojan project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ayojan.settings')

# Configure Django
import django
django.setup()

# Wrap the WSGI application in a try-except block for better error reporting
application = get_wsgi_application()
app = application
