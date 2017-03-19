from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from rpgsite.tools import GetPlayersWithLinks
from apps.guilds.models import Guild, GuildRank, GuildMembership, GuildInvite

from apps.players.models import Player

# Guild

class GuildAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'get_members', 'get_created_display')

    def get_members(self, guild):
        return GetPlayersWithLinks(
            Player.objects.filter(guildmembership__guild=guild)
        )

    get_members.short_description = _('Members')

admin.site.register(Guild, GuildAdmin)

# GuildRank

class GuildRankAdmin(admin.ModelAdmin):
    list_display = ('guild', 'name', 'level', 'get_members')

    list_filter = ('guild', 'name', 'level')

    def get_members(self, guild_rank):
        return GetPlayersWithLinks(
            Player.objects.filter(guildmembership__rank=guild_rank)
        )

    get_members.short_description = _('Who has it')

admin.site.register(GuildRank, GuildRankAdmin)

# GuildMembership

class GuildMembershipAdmin(admin.ModelAdmin):
    list_display = ('player', 'guild', 'rank', 'nick')

admin.site.register(GuildMembership, GuildMembershipAdmin)

# GuildInvite

class GuildInviteAdmin(admin.ModelAdmin):
    list_display = ('player', 'guild')

admin.site.register(GuildInvite, GuildInviteAdmin)
