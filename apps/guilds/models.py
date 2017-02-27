from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver

@receiver(pre_delete)
def guild_pre_delete(sender, instance, **kwargs):
    if sender == Guild:
        
        for player in instance.player_set.all():
            player.guild_nick = ''

default_guild_ranks = (
    {'name': 'Leader', 'level': 3},
    {'name': 'Vice-Leader', 'level': 2},
    {'name': 'Member', 'level': 1},
)

@receiver(post_save)
def guild_post_save(sender, instance, created, **kwargs):
    if sender == Guild and created:
        
        for guildrank in default_guild_ranks:
            instance.guildrank_set.create(**guildrank)

        if instance.owner:
            instance.owner.guild = instance
            instance.owner.guild_rank = instance.guildrank_set.get(name='Leader')
            instance.owner.save()

class Guild(models.Model):
    
    name = models.CharField(
        max_length = 30, 
        unique = True
    )
    
    owner = models.OneToOneField(
        'players.Player', 
        null = True, 
        blank = True, 
        on_delete = models.SET_NULL,
        related_name = 'guild_owner'
    )
    
    created = models.DateTimeField(
        default = timezone.now
    )

    class Meta:
        db_table = 'guilds'

    def __str__(self):
        return self.name

    @property
    def get_owner_name(self):
        return self.owner.name if self.owner else 'nobody'

class GuildRank(models.Model):
    
    guild = models.ForeignKey(
        'guilds.Guild', 
        on_delete = models.CASCADE
    )
    
    name = models.CharField(
        max_length = 30
    )
    
    level = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'guild_ranks'
        unique_together = ['guild', 'name']

    def __str__(self):
        return self.name
