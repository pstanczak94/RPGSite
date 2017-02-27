from django.contrib import admin

from .models import AccountBan, PlayerBan, \
    IPAddressBan, Record, Storage

@admin.register(AccountBan)
class AccountBanAdmin(admin.ModelAdmin):
    search_fields = ('banned__username',)
    list_display = ('banned', 'active', 'permament', 'admin', 'reason', 'expires', 'added')
    pass

@admin.register(PlayerBan)
class PlayerBanAdmin(admin.ModelAdmin):
    search_fields = ('banned__name',)
    list_display = ('banned', 'active', 'permament', 'admin', 'reason', 'expires', 'added')
    pass

@admin.register(IPAddressBan)
class IPAddressBanAdmin(admin.ModelAdmin):
    search_fields = ('banned',)
    list_display = ('banned', 'active', 'permament', 'admin', 'reason', 'expires', 'added')
    pass
