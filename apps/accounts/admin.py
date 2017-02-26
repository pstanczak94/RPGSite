from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import Account
from django.utils.safestring import mark_safe
from django.urls.base import reverse_lazy
from django.contrib.auth import models as auth_models
from apps.accounts.models import Group

@admin.register(Account)
class AccountAdmin(UserAdmin):
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Account status'), {
            'fields': ('is_active', 'blocked', 'email_activated', 'warned')
        }),
        (_('Personal info'), {
            'fields': ('email', 'full_name')
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
        'username', 'email', 'get_players_view', 'date_joined', 'email_activated', 'blocked'
    )

    list_filter = (
        'is_staff', 'is_active', 'email_activated', 'blocked', 'warned'
    )

    search_fields = ('username', 'email', 'first_name', 'last_name')

    ordering = ('username',)

    def get_players_view(self, account):
        ret = []
        
        for player in account.get_players:
            ret.append(
                '<a href="' + 
                str(reverse_lazy('admin:players_player_change', args=(player.pk,))) + 
                '">' + player.name + '</a>')
            
        return mark_safe(', '.join(ret)) if ret else self.get_empty_value_display()
    
    get_players_view.short_description = _('Players')

admin.site.unregister(auth_models.Group)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass

