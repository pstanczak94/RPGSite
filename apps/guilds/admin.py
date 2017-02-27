from django.contrib import admin
from apps.guilds.models import Guild, GuildRank
from django.utils.translation import ugettext_lazy as _

from apps.tools.tools import GetPlayersWithLinks

@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'get_members', 'created')
    
    def get_members(self, guild):
        return GetPlayersWithLinks(guild.player_set.all())
    get_members.short_description = _('Members')
    
@admin.register(GuildRank)
class GuildRankAdmin(admin.ModelAdmin):
    list_display = ('guild', 'name', 'level', 'get_members')
    
    list_filter = ('guild', 'name', 'level')
    
    def get_members(self, guild_rank):
        return GetPlayersWithLinks(guild_rank.player_set.all())
    get_members.short_description = _('Who has it')