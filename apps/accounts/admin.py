from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from apps.accounts.models import AccountGroup
from .models import Account
from apps.tools.tools import GetPlayersWithLinks

class AccountAdmin(UserAdmin):
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Account status'), {
            'fields': ('is_active', 'email_activated')
        }),
        (_('Personal info'), {
            'fields': ('email', 'access', 'premium_days')
        }),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    readonly_fields = ('date_joined', 'last_login')

    list_display = (
        'username', 'email', 'get_players_view', 'date_joined', 'email_activated'
    )

    list_filter = (
        'is_staff', 'is_active', 'email_activated'
    )

    search_fields = ('username', 'email', 'first_name', 'last_name')

    ordering = ('username',)

    def get_players_view(self, account):
        return GetPlayersWithLinks(account.players.all())
    get_players_view.short_description = _('Players')

admin.site.unregister(Group)
admin.site.register(AccountGroup)
admin.site.register(Account, AccountAdmin)