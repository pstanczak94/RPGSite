from django import template
from django.forms.widgets import TextInput, EmailInput, PasswordInput

register = template.Library()

from apps.tools import tools

from django.utils.safestring import mark_safe
from django.template.defaultfilters import date as format_date
from django.templatetags.static import StaticNode

@register.filter(expects_localtime=True, is_safe=False)
def datetime(value, arg=None):
    if tools.StringEmpty(arg):
        arg = 'DATETIME_FORMAT'
    return format_date(value, arg=arg)

@register.filter(is_safe=True)
def bootstrap_label(value, arg=None):
    return value.label_tag(attrs={'class': 'control-label'})

BOOTSTRAP_FORM_CONTROLS = (TextInput, EmailInput, PasswordInput)

@register.filter(is_safe=True)
def bootstrap_input(value, arg=None):
    if isinstance(value.field.widget, BOOTSTRAP_FORM_CONTROLS):
        return value.as_widget(attrs={'class': 'form-control'})
    else:
        return value.as_widget()

@register.simple_tag()
def emoji(arg=None):
    from emoji import Emoji
    if arg in Emoji.keys():
        return mark_safe(Emoji.replace(':' + arg + ':'))
    else:
        return ''

def smart_split_with_version(arg, pattern, sep='?'):
    s = arg.split(sep=sep, maxsplit=1)
    return mark_safe(
        pattern.format(
            StaticNode.handle_simple(s[0]),
            sep if len(s) > 1 else '',
            s[1] if len(s) > 1 else ''
        )
    )

@register.simple_tag()
def link_static_css(arg=None):
    return smart_split_with_version(arg, '<link rel="stylesheet" href="{0}{1}{2}">')

@register.simple_tag()
def link_static_js(arg=None):
    return smart_split_with_version(arg, '<script type="text/javascript" src="{0}{1}{2}"></script>')
