import re

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import title as format_title
from apps.players.models import Player
from django.forms.widgets import RadioSelect, TextInput
from apps.tools.forms import CharField
from django.core.validators import RegexValidator

class BootstrapTextInput(TextInput):
    def __init__(self, attrs=None):
        super(BootstrapTextInput, self).__init__(attrs)
        if 'class' in self.attrs:
            self.attrs['class'] += ' form-control'
        else:
            self.attrs['class'] = 'form-control'

def character_name_fixer(name):
    name = name.strip()
    name = re.sub('\s+', ' ', name)
    name = format_title(name)
    return name

class CreateForm(forms.ModelForm):
    
    class Meta:
        model = Player
        fields = ['name', 'sex', 'vocation', 'town']
        widgets = {
            'sex': RadioSelect(),
            'vocation': RadioSelect(),
            'town': RadioSelect(),
        }
        
    name = CharField(
        autofocus = True,
        min_length = settings.CHARACTER_NAME_MIN_LENGTH,
        max_length = settings.CHARACTER_NAME_MAX_LENGTH,
        validators = [
            RegexValidator(
                settings.CHARACTER_NAME_REGEX,
                _('Character name contains illegal characters.'),
                'invalid-name'
            )
        ],
        widget = BootstrapTextInput(),
    )
        
    def clean(self):
        data = super(CreateForm, self).clean()
        
        if not self.is_valid():
            return data
        
        name = data.get('name')

        fixed_name = character_name_fixer(name)
        
        if name != fixed_name:
            self.add_error('name', _(
                'Character name was corrected.\n'
                'You can continue if that is okey.'
            ))
            self.corrected_name = fixed_name
            return data
        
        if not self.account.can_add_character:
            self.add_error(None, _('You can\'t create more characters.'))
            return data
        
        if Player.objects.filter(name=fixed_name).exists():
            self.add_error('name', _('That name is already beign used.'))
            return data
        
        return data










