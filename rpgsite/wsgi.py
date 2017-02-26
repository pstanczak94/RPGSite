"""
WSGI config for rpgsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rpgsite.settings")

application = get_wsgi_application()

from apps.accounts.models import Account
from apps.tools import tools

if not Account.objects.username_exists('root'):
    try:
        Account.objects.create_superuser(
            username = 'root',
            email = 'root@rpgsite.pl',
            password = 'rpgsite'
        )
    except:
        tools.LogError('Root user creation failed.')
    else:
        tools.LogInfo('Root user was created.')
