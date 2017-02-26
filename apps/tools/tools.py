import sys, logging

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

from django.conf import settings

def GetLogger():
    return logging.getLogger(settings.TOOLS_LOGGER_NAME)

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

