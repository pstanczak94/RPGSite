from django.contrib import admin
from apps.guilds.models import Guild, GuildRank
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.urls.base import reverse_lazy

@admin.register(Guild)
class GuildAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'get_members', 'created')
    
    def get_members(self, guild):
        ret = []
        
        for player in guild.player_set.all():
            ret.append(
                '<a href="' + 
                str(reverse_lazy('admin:players_player_change', args=(player.pk,))) + 
                '">' + player.name + '</a>')
                
        return mark_safe(', '.join(ret)) if ret else self.get_empty_value_display()
    
    get_members.short_description = _('Members')
    
@admin.register(GuildRank)
class GuildRankAdmin(admin.ModelAdmin):
    list_display = ('guild', 'name', 'level', 'get_members')
    
    list_filter = ('guild', 'name', 'level')
    
    def get_members(self, guild_rank):
        ret = []
        
        for player in guild_rank.player_set.all():
            ret.append(
                '<a href="' + 
                str(reverse_lazy('admin:players_player_change', args=(player.pk,))) + 
                '">' + player.name + '</a>')
                
        return mark_safe(', '.join(ret)) if ret else self.get_empty_value_display()
    
    get_members.short_description = _('Who has it')