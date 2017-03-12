import sys, logging, pytz

from django.urls.base import reverse_lazy
from django.utils.formats import date_format
from django.utils.safestring import mark_safe
from django.utils.timezone import localtime

def IsLinux():
    return sys.platform in ('linux', 'linux2')

def IsWindows():
    return sys.platform == 'win32'

def StringEmpty(text):
    return text in (None, '')

def StringCrop(text, max_len):
    if len(text) > max_len:
        return text[:max_len] + '...'
    else:
        return text

from django.utils import timezone

def GetCurrentTimestamp():
    return int(timezone.now().timestamp())

from django.conf import settings

def GetSetting(name, default=None):
    return getattr(settings, name, default)

def GetLogger():
    return logging.getLogger(GetSetting('TOOLS_LOGGER_NAME', 'rpgsite'))

def LogDebug(msg):
    GetLogger().debug(msg)

def LogInfo(msg):
    GetLogger().info(msg)

def LogWarning(msg):
    GetLogger().warning(msg)

def LogError(msg):
    GetLogger().error(msg)

def LogFatal(msg):
    GetLogger().fatal(msg)

def GetLocalDateTime(datetime):
    # localtime(datetime, pytz.timezone('Europe/Warsaw'))
    # activate(pytz.timezone('Europe/Warsaw'))
    return date_format(localtime(datetime), settings.DATETIME_FORMAT)

def CaseInsensitiveKwargs(field_name, **kwargs):
    if field_name in kwargs:
        value = kwargs.pop(field_name)
        kwargs[field_name + '__iexact'] = value
    return kwargs

def GetPlayersWithLinks(iterable, sep=', ', empty_value='-', pattern='admin:players_player_change'):
    html = []
    for player in iterable:
        html.append(
            '<a href="%s">%s</a>' % (
                reverse_lazy(pattern, args=(player.pk,)),
                player.name
            )
        )
    return mark_safe(sep.join(html)) if html else empty_value

from django.contrib import admin

def CustomListFilter(name, title):
    class ListFilterWrapper(admin.FieldListFilter):
        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return (name, ListFilterWrapper)
