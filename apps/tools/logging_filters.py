import logging

from django.conf import settings

from rpgsite.tools import GetSetting

class RequireLogEnabled(logging.Filter):
    def filter(self, record):
        return GetSetting('LOG_ENABLED', True)
