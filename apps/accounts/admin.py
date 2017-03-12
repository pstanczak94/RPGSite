from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Account
from rpgsite.tools import GetPlayersWithLinks

class AccountAdmin(admin.ModelAdmin):

    list_display = (
        'name', 'email', 'get_creation_display', 'access', 'get_players_view'
    )

    list_filter = (
        'access',
    )

    search_fields = (
        'name', 'email',
    )

    ordering = (
        'name',
    )

    def get_players_view(self, account):
        return GetPlayersWithLinks(account.players.all())
    get_players_view.short_description = _('Players')

admin.site.register(Account, AccountAdmin)