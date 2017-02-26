import logging

from django.conf import settings

class RequireLogEnabled(logging.Filter):
    def filter(self, record):
        return settings.LOG_ENABLED
