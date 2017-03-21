from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver
from django.utils.translation import ugettext_lazy as _

from rpgsite.tools import GetCurrentTimestamp, CaseInsensitiveKwargs

@receiver(post_save)
def guild_post_save(sender, instance, created, **kwargs):
    if sender == Guild and created:
        GuildMembership.objects.create(
            player = instance.owner,
            guild = instance,
            rank = instance.ranks.get(level = 3),
            nick = _('The creator'),
        )

class GuildManager(models.Manager):
    def filter(self, **kwargs):
        kwargs = CaseInsensitiveKwargs('name', **kwargs)
        return super(GuildManager, self).filter(**kwargs)

    def get(self, **kwargs):
        kwargs = CaseInsensitiveKwargs('name', **kwargs)
        return super(GuildManager, self).get(**kwargs)

    def get_by_natural_key(self, name):
        return self.get(name=name)

    def name_exists(self, name):
        return self.get_queryset().filter(name=name).exists()

class Guild(models.Model):
    objects = GuildManager()

    name = models.CharField(
        max_length = 255,
        unique = True,
    )

    owner = models.OneToOneField(
        'players.Player',
        on_delete = models.DO_NOTHING,
        related_name = 'ownedguild',
        db_column = 'ownerid',
    )

    created = models.IntegerField(
        default = GetCurrentTimestamp,
        db_column = 'creationdata',
        editable = False,
    )

    def get_created_display(self):
        return datetime.fromtimestamp(self.created)

    get_created_display.short_description = _('date created')

    motd = models.CharField(
        max_length = 255,
        blank = True,
    )

    class Meta:
        managed = False
        db_table = 'guilds'

    def __str__(self):
        return self.name

class GuildRank(models.Model):
    guild = models.ForeignKey(
        'guilds.Guild',
        models.DO_NOTHING,
        related_name = 'ranks',
    )

    name = models.CharField(
        max_length = 255,
    )

    level = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'guild_ranks'

    def __str__(self):
        return self.name

class GuildMembership(models.Model):
    player = models.OneToOneField(
        'players.Player',
        models.DO_NOTHING,
        primary_key = True,
    )

    guild = models.ForeignKey(
        'guilds.Guild',
        models.DO_NOTHING,
    )

    rank = models.ForeignKey(
        'guilds.GuildRank',
        models.DO_NOTHING,
    )

    nick = models.CharField(
        max_length = 15,
        blank = True,
    )

    class Meta:
        managed = False
        db_table = 'guild_membership'

class GuildInvite(models.Model):
    player = models.ForeignKey(
        'players.Player',
        models.DO_NOTHING,
    )

    guild = models.ForeignKey(
        'guilds.Guild',
        models.DO_NOTHING,
    )

    class Meta:
        managed = False
        db_table = 'guild_invites'
        unique_together = (('player', 'guild'),)

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