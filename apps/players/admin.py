from django.conf import settings
from django.contrib import admin
from django import forms

from rpgsite.tools import CustomListFilter
from .models import Player
from apps.accounts.models import Account

from django.utils.translation import ugettext_lazy as _

class PlayerForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = '__all__'

class PlayerAddForm(forms.ModelForm):

    def clean(self):
        super(PlayerAddForm, self).clean()

        name = self.cleaned_data.get('account')

        account = Account.objects.get_by_natural_key(name)

        if not account.can_add_character():
            self.add_error('account', _(
                'One account can only contain %(num)d players.'
            ) % {
                'num': settings.MAX_PLAYERS_PER_ACCOUNT,
            })

        return self.cleaned_data

    class Meta:
        model = Player
        fields = (
            'account', 'group_id', 'name', 'sex', 'vocation', 'town_id',
        )

class PlayerAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        self.form = self.change_form if obj else self.add_form
        return super(PlayerAdmin, self).get_form(request, obj, **kwargs)

    add_form = PlayerAddForm
    change_form = PlayerForm

    list_display = (
        'name', 'account', 'level', 'vocation', 'sex', 'get_creation_display',
    )

    list_filter = (
        'sex',
        'vocation',
        'group_id',
        CustomListFilter('guildmembership__guild__name', _('guild name')),
    )

    search_fields = (
        'name', 'lastip', 'account__name', 'account__email',
    )

    ordering = (
        'name',
    )

admin.site.register(Player, PlayerAdmin)

# @admin.register(PlayerGroup)
# class PlayerGroupAdmin(admin.ModelAdmin):
#     list_display = (
#         'name', 'access', 'flags', 'max_depot_items', 'max_vip_list'
#     )
#
#     ordering = ('name',)
#
# @admin.register(PlayerSkill)
# class PlayerSkillAdmin(admin.ModelAdmin):
#     search_fields = ('player__name',)
#     list_display = ('player', 'skill_id', 'value', 'count')
#
# @admin.register(PlayerSpell)
# class PlayerSpellAdmin(admin.ModelAdmin):
#     search_fields = ('player__name',)
#     list_display = ('player', 'words')
#
# @admin.register(PlayerItem)
# class PlayerItemAdmin(admin.ModelAdmin):
#     search_fields = ('player__name',)
#     list_display = ('player', 's_id', 'p_id', 'item_type', 'count')
#
# @admin.register(PlayerDepotItem)
# class PlayerDepotItemAdmin(admin.ModelAdmin):
#     search_fields = ('player__name',)
#     list_display = ('player', 'depot_id', 's_id', 'p_id', 'item_type', 'count')
#
# @admin.register(PlayerStorage)
# class PlayerStorageAdmin(admin.ModelAdmin):
#     search_fields = ('player__name',)
#     list_display = ('player', 'key', 'value')
#     list_filter = ('key',)
#
# @admin.register(PlayerVipList)
# class PlayerVipListAdmin(admin.ModelAdmin):
#     search_fields = ('player__name',)
#     list_display = ('player', 'vip_player')
