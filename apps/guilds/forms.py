from django import forms
from django.core.validators import RegexValidator
from django.forms.fields import ChoiceField
from django.forms.models import ModelChoiceField
from django.forms.widgets import RadioSelect, Select

from apps.guilds.models import Guild
from apps.tools.forms import CharField, CustomModelForm
from rpgsite.tools import GetSetting

from django.utils.translation import ugettext_lazy as _

GuildNameMinLength = 3
GuildNameMaxLength = 20

GuildNameValidator = RegexValidator(
    regex = r'^[a-zA-Z ]+$',
    message = _('Guild name contains illegal characters.')
)

GuildOwnerMinLevel = 50

GuildNameHelpText = _(
    'Guild name needs to be from {min} to {max} characters length.\n'
    'Only english characters and spaces are allowed.'
).format(
    min = GuildNameMinLength,
    max = GuildNameMaxLength,
)

class CreateForm(CustomModelForm):
    class Meta:
        model = Guild
        fields = ['owner', 'name']

    owner = ModelChoiceField(
        label = _('Guild owner'),
        help_text = _('Guild owner must have at least {min} level.').format(min=GuildOwnerMinLevel),
        queryset = None,
        widget = Select(attrs = {'class':'form-control'}),
    )

    name = CharField(
        label = _('Guild name'),
        help_text = GuildNameHelpText,
        min_length = GuildNameMinLength,
        max_length = GuildNameMaxLength,
        validators = [GuildNameValidator],
    )

    def __init__(self, account, *args, **kwargs):
        super(CreateForm, self).__init__(*args, **kwargs)
        self.fields['owner'].queryset = account.players

    def clean_owner(self):
        owner = self.cleaned_data.get('owner')

        if owner.level < GuildOwnerMinLevel:
            self.add_error('owner', _(
                'Player must have {min} level to create guild.'
            ).format(
                min = GuildOwnerMinLevel
            ))

        return owner