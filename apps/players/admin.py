from django.contrib import admin
from django.utils.translation import ugettext as _

from .models import Player, PlayerGroup, PlayerSkill, \
    PlayerDepotItem, PlayerItem, PlayerSpell, \
    PlayerStorage, PlayerVipList

from django import forms
from apps.accounts.models import Account
from django.conf import settings

class PlayerForm(forms.ModelForm):

    class Meta:
        model = Player
        fields = '__all__'

class PlayerAddForm(forms.ModelForm):

    def clean(self):
        data = super(PlayerAddForm, self).clean()

        if self.is_valid():
            account = Account.objects.get_by_natural_key(data['account'])
            if not account.can_add_character:
                self.add_error('account', _(
                    'One account can only contain %(num)d players.'
                ) % {
                    'num': settings.MAX_PLAYERS_PER_ACCOUNT,
                })

        return data

    class Meta:
        model = Player
        fields = ['account', 'group', 'name', 'sex', 'vocation', 'town']

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, **kwargs):
        self.form = self.change_form if obj else self.add_form
        return super(PlayerAdmin, self).get_form(request, obj, **kwargs)

    add_form = PlayerAddForm
    change_form = PlayerForm
    
    list_display = (
        'name', 'account', 'level', 'vocation', 'sex', 'created'
    )

    list_filter = (
        'sex', 'vocation', 'guild', 'group'
    )

    search_fields = ('name', 'last_ip', 'account__username', 'account__email')

    ordering = ('name',)

@admin.register(PlayerGroup)
class PlayerGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'access', 'flags', 'max_depot_items', 'max_vip_list'
    )

    ordering = ('name',)

@admin.register(PlayerSkill)
class PlayerSkillAdmin(admin.ModelAdmin):
    search_fields = ('player__name',)
    list_display = ('player', 'skill_id', 'value', 'count')
    pass

@admin.register(PlayerSpell)
class PlayerSpellAdmin(admin.ModelAdmin):
    search_fields = ('player__name',)
    list_display = ('player', 'words')
    pass

@admin.register(PlayerItem)
class PlayerItemAdmin(admin.ModelAdmin):
    search_fields = ('player__name',)
    list_display = ('player', 's_id', 'p_id', 'item_type', 'count')
    pass

@admin.register(PlayerDepotItem)
class PlayerDepotItemAdmin(admin.ModelAdmin):
    search_fields = ('player__name',)
    list_display = ('player', 'depot_id', 's_id', 'p_id', 'item_type', 'count')
    pass

@admin.register(PlayerStorage)
class PlayerStorageAdmin(admin.ModelAdmin):
    search_fields = ('player__name',)
    list_display = ('player', 'key', 'value')
    list_filter = ('key',)
    pass

@admin.register(PlayerVipList)
class PlayerVipListAdmin(admin.ModelAdmin):
    search_fields = ('player__name',)
    list_display = ('player', 'vip_player')
    pass

