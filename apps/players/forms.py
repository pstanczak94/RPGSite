import re

from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import title as format_title
from apps.players.models import Player
from django.forms.widgets import RadioSelect, TextInput
from apps.tools.forms import CharField, BootstrapTextInput
from django.core.validators import RegexValidator

from rpgsite.tools import GetSetting

def character_name_fixer(name):
    name = name.strip()
    name = re.sub('\s+', ' ', name)
    name = format_title(name)
    return name

class CreateForm(forms.ModelForm):
    
    class Meta:
        model = Player
        fields = ['name', 'sex', 'vocation', 'town_id']
        widgets = {
            'sex': RadioSelect(),
            'vocation': RadioSelect(),
            'town_id': RadioSelect(),
        }
        
    name = CharField(
        autofocus = True,
        min_length = GetSetting('CHARACTER_NAME_MIN_LENGTH'),
        max_length = GetSetting('CHARACTER_NAME_MAX_LENGTH'),
        validators = [
            RegexValidator(
                GetSetting('CHARACTER_NAME_REGEX'),
                _('Character name contains illegal characters.'),
                'invalid-name'
            )
        ],
    )
        
    def clean(self):
        data = super(CreateForm, self).clean()
        
        if not self.is_valid():
            return data
        
        name = data.get('name')

        if not self.account.can_add_character():
            self.add_error(None, _('You can\'t create more characters.'))
            return data

        fixed_name = character_name_fixer(name)
        
        if name != fixed_name:
            self.add_error('name', _(
                'Character name was corrected.\n'
                'You can continue if that is okey.'
            ))
            self.corrected_name = fixed_name
            return data

        if Player.objects.name_exists(fixed_name):
            self.add_error('name', _('That name is already being used.'))
            return data
        
        return data

class StatsForm(forms.Form):

    vocation = forms.ChoiceField(
        label = _('Vocation'),
        choices = (
            ('all', _('All')),
            ('knight', _('Knight')),
            ('paladin', _('Paladin')),
            ('sorcerer', _('Sorcerer')),
            ('druid', _('Druid')),
        ),
        widget = forms.Select(),
    )

    sortby = forms.ChoiceField(
        label = _('Sort by'),
        choices = (
            ('level', _('Level')),
            ('name', _('Name')),
        ),
        widget = forms.Select(),
    )

    order = forms.ChoiceField(
        label = _('Order'),
        choices = (
            ('desc', _('Descending')),
            ('asc', _('Ascending')),
        ),
        widget = forms.Select(),
    )

    def clean(self):
        super(StatsForm, self).clean()
        return self.cleaned_data