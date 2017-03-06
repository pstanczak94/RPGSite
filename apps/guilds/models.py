from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver

# @receiver(pre_delete)
# def guild_pre_delete(sender, instance, **kwargs):
#     if sender == Guild:
#
#         for player in instance.player_set.all():
#             player.guild_nick = ''
#
# default_guild_ranks = (
#     {'name': 'the Leader', 'level': 3},
#     {'name': 'a Vice-Leader', 'level': 2},
#     {'name': 'a Member', 'level': 1},
# )
#
# @receiver(post_save)
# def guild_post_save(sender, instance, created, **kwargs):
#     if sender == Guild and created:
#
#         for guildrank in default_guild_ranks:
#             instance.guildrank_set.create(**guildrank)
#
#         if instance.owner:
#             instance.owner.guild = instance
#             instance.owner.guild_rank = instance.guildrank_set.get(name='Leader')
#             instance.owner.save()

class Guild(models.Model):

    name = models.CharField(max_length=30, unique=True)

    owner = models.OneToOneField(
        'players.Player', 
        null = True, 
        blank = True, 
        on_delete = models.SET_NULL,
        related_name = 'guild_owner',
        db_column = 'ownerid',
    )

    creationdata = models.DateTimeField(
        default = timezone.now,
    )

    motd = models.CharField(max_length=100, default='')

    class Meta:
        managed = False
        db_table = 'guilds'

    def __str__(self):
        return self.name

    @property
    def get_owner_name(self):
        return self.owner.name if self.owner else 'nobody'

class GuildRank(models.Model):
    guild = models.ForeignKey('guilds.Guild', models.CASCADE)
    name = models.CharField(max_length=30)
    level = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'guild_ranks'
        unique_together = (('guild', 'name'),)

    def __str__(self):
        return self.name

class GuildInvite(models.Model):
    player = models.ForeignKey('players.Player', models.CASCADE)
    guild = models.ForeignKey('guilds.Guild', models.CASCADE)

    class Meta:
        managed = False
        db_table = 'guild_invites'
        unique_together = (('player', 'guild'),)

class GuildMembership(models.Model):
    player = models.OneToOneField('players.Player', models.CASCADE, primary_key=True)
    guild = models.ForeignKey('guilds.Guild', models.CASCADE)
    rank = models.ForeignKey('guilds.GuildRank', models.CASCADE)
    nick = models.CharField(max_length=15, default='')

    class Meta:
        managed = False
        db_table = 'guild_membership'

class GuildWar(models.Model):
    guild1 = models.IntegerField(default=0)
    guild2 = models.IntegerField(default=0)
    name1 = models.CharField(max_length=255)
    name2 = models.CharField(max_length=255)
    status = models.IntegerField(default=0)
    started = models.BigIntegerField(default=0)
    ended = models.BigIntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'guild_wars'

class GuildwarKill(models.Model):
    killer = models.CharField(max_length=50)
    target = models.CharField(max_length=50)
    killerguild = models.IntegerField()
    targetguild = models.IntegerField()
    warid = models.ForeignKey('guilds.GuildWar', models.CASCADE, db_column='warid')
    time = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'guildwar_kills'