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

from rpgsite.tools import GetSetting

if GetSetting('CREATE_ROOT_ON_INIT', True):
    from apps.accounts.models import Account
    from rpgsite.tools import LogError, LogInfo
    if not Account.objects.name_exists('root'):
        try:
            account = Account.objects.create_admin(
                name = 'root',
                password = 'rpgsite',
                email = 'root@rpgsite.pl',
            )
            account.players.create(
                name = 'God Caday',
                group_id = '3', # God
                lookbody = 101,
                lookfeet = 94,
                lookhead = 82,
                looklegs = 96,
                looktype = 574,
                lookaddons = 3,
            )
        except Exception as e:
            LogError('Root user creation error: ' + str(e))
        else:
            LogInfo('Root user was created.')
