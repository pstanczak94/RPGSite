from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from datetime import timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save)
def player_post_save(sender, instance, created, **kwargs):
    if sender == Player and created:
        for i in [0,1,2,3,4,5,6]:
            instance.playerskill_set.create(
                skill_id = i, value = 10
            )

class PlayerManager(models.Manager):
    
    def _check_kwargs_for_name(self, **kwargs):
        name_field = 'name'
        if name_field in kwargs:
            name = kwargs.pop(name_field)
            kwargs[name_field + '__iexact'] = name
        return kwargs
    
    def filter(self, **kwargs):
        kwargs = self._check_kwargs_for_name(**kwargs)
        return super(PlayerManager, self).filter(**kwargs)

    def get(self, **kwargs):
        kwargs = self._check_kwargs_for_name(**kwargs)
        return super(PlayerManager, self).get(**kwargs)
    
class Player(models.Model):
    
    objects = PlayerManager()
    
    SEX_CHOICES = (
        (1, _('Male')),
        (2, _('Female')),
    )
    
    VOCATION_CHOICES = (
        (1, _('Knight')),
        (2, _('Paladin')),
        (3, _('Sorcerer')),
        (4, _('Druid')),
    )
    
    TOWN_CHOICES = (
        (1, _('RPGLand')),
    )
    
    account = models.ForeignKey(
        'accounts.Account', 
        on_delete = models.CASCADE, 
    )
    
    group = models.ForeignKey(
        'players.PlayerGroup', 
        null = True, 
        blank = True, 
        on_delete = models.SET_NULL, 
    )
    
    name = models.CharField(
        max_length = 30, 
        unique = True, 
    )
    
    sex = models.PositiveSmallIntegerField(
        default = SEX_CHOICES[0][0],
        choices = SEX_CHOICES,
    )
    
    vocation = models.PositiveSmallIntegerField(
        default = VOCATION_CHOICES[0][0],
        choices = VOCATION_CHOICES,
    )
    
    town = models.PositiveSmallIntegerField(
        default = TOWN_CHOICES[0][0],
        choices = TOWN_CHOICES,
    )
    
    promotion = models.BooleanField(
        default = False
    )
    
    experience = models.BigIntegerField(
        default = 0
    )
    
    level = models.PositiveIntegerField(
        default = 1
    )
    
    magic_level = models.PositiveSmallIntegerField(
        default = 0
    )
    
    health = models.PositiveIntegerField(
        default = 150
    )
    
    health_max = models.PositiveIntegerField(
        default = 150
    )
    
    mana = models.PositiveIntegerField(
        default = 0
    )
    
    mana_max = models.PositiveIntegerField(
        default = 0
    )
    
    mana_spent = models.PositiveIntegerField(
        default = 0
    )
    
    soul = models.PositiveSmallIntegerField(
        default = 0
    )
    
    direction = models.PositiveSmallIntegerField(
        default = 2
    )
    
    look_body = models.PositiveSmallIntegerField(
        default = 0
    )
    
    look_feet = models.PositiveSmallIntegerField(
        default = 0
    )
    
    look_head = models.PositiveSmallIntegerField(
        default = 0
    )
    
    look_legs = models.PositiveSmallIntegerField(
        default = 0
    )
    
    look_type = models.PositiveSmallIntegerField(
        default = 136
    )
    
    pos_x = models.PositiveIntegerField(
        default = 0
    )
    
    pos_y = models.PositiveIntegerField(
        default = 0
    )
    
    pos_z = models.PositiveSmallIntegerField(
        default = 0
    )
    
    capacity = models.PositiveIntegerField(
        default = 0
    )
    
    last_logout = models.DateTimeField(
        default = None,
        null = True, 
        blank = True
    )
    
    last_ip = models.GenericIPAddressField(
        default = None,
        null = True, 
        blank = True
    )
    
    save_on_logout = models.BooleanField(
        default = True
    )
    
    conditions = models.BinaryField(
        default = b''
    )
    
    stamina = models.DurationField(
        default = timedelta(days=1, hours=12)
    )
    
    skull = models.BooleanField(
        default = False
    )
    
    skull_time = models.DurationField(
        default = None,
        null = True,
        blank = True
    )
    
    loss_experience = models.PositiveIntegerField(
        default = 100
    )
    
    loss_mana = models.PositiveIntegerField(
        default = 100
    )
    
    loss_skills = models.PositiveIntegerField(
        default = 100
    )
    
    loss_items = models.PositiveIntegerField(
        default = 100
    )
    
    balance = models.PositiveIntegerField(
        default = 0
    )
    
    premium_end = models.DateTimeField(
        default = None,
        null = True, 
        blank = True
    )
    
    guild = models.ForeignKey(
        'guilds.Guild', 
        null = True,
        blank = True, 
        on_delete = models.SET_NULL
    )
    
    guild_rank = models.ForeignKey(
        'guilds.GuildRank', 
        null = True,
        blank = True, 
        on_delete = models.SET_NULL
    )
    
    guild_nick = models.CharField(
        default = '',
        max_length = 30, 
        blank = True
    )
    
    in_game = models.BooleanField(
        default = False
    )
    
    created = models.DateTimeField(
        default = timezone.now
    )

    class Meta:
        db_table = 'players'
        verbose_name = _('player')
        verbose_name_plural = _('players')

    def __str__(self):
        return self.name

class PlayerGroup(models.Model):
    
    name = models.CharField(
        max_length = 30, 
        unique = True
    )
    
    access = models.PositiveIntegerField(
        default = 0
    )
    
    flags = models.IntegerField(
        default = 0
    )
    
    max_depot_items = models.PositiveSmallIntegerField(
        default = 1000
    )
    
    max_vip_list = models.PositiveSmallIntegerField(
        default = 50
    )

    class Meta:
        db_table = 'player_groups'
        verbose_name = _('group')
        verbose_name_plural = _('groups')

    def __str__(self):
        return self.name

class PlayerVipList(models.Model):
    
    player = models.ForeignKey(
        'players.Player', 
        on_delete = models.CASCADE,
        db_index = True
    )
    
    vip_player = models.ForeignKey(
        'players.Player', 
        on_delete = models.CASCADE, 
        related_name = 'vip_player',
        db_index = True
    )

    class Meta:
        db_table = 'player_viplist'
        unique_together = ['player', 'vip_player']
        verbose_name = _('vip list')
        verbose_name_plural = _('vip lists')

    def __str__(self):
        return '%s -> %s' % (
            self.player.name, self.vip_player.name
        )

class PlayerSpell(models.Model):
    
    player = models.ForeignKey(
        'players.Player', 
        on_delete = models.CASCADE,
        db_index = True
    )
    
    words = models.CharField(
        max_length = 30
    )

    class Meta:
        db_table = 'player_spells'
        unique_together = ['player', 'words']
        verbose_name = _('spell')
        verbose_name_plural = _('spells')

    def __str__(self):
        return '%s -> %s' % (
            self.player.name, self.words
        )

class PlayerStorage(models.Model):
    
    player = models.ForeignKey(
        'players.Player', 
        on_delete = models.CASCADE,
        db_index = True
    )
    
    key = models.PositiveSmallIntegerField()
    
    value = models.IntegerField()

    class Meta:
        db_table = 'player_storage'
        unique_together = ['player', 'key']
        verbose_name = _('storage')
        verbose_name_plural = _('storages')

    def __str__(self):
        return '%s -> %d: %d' % (
            self.player.name, self.key, self.value
        )

class PlayerSkill(models.Model):
    
    player = models.ForeignKey(
        'players.Player', 
        on_delete = models.CASCADE,
        db_index = True
    )
    
    skill_id = models.PositiveSmallIntegerField()
    
    value = models.PositiveIntegerField(
        default = 0
    )
    
    count = models.PositiveIntegerField(
        default = 0
    )

    class Meta:
        db_table = 'player_skills'
        unique_together = ['player', 'skill_id']
        verbose_name = _('skill')
        verbose_name_plural = _('skills')

    def __str__(self):
        return '%s (skill_id: %d, value: %d, count: %d)' % (
            self.player.name, self.skill_id, self.value, self.count
        )

class PlayerItem(models.Model):
    
    player = models.ForeignKey(
        'players.Player', 
        on_delete = models.CASCADE,
        db_index = True
    )
    
    s_id = models.IntegerField()
    
    p_id = models.IntegerField(
        default = 0
    )
    
    item_type = models.PositiveIntegerField()
    
    count = models.PositiveSmallIntegerField(
        default = 0
    )
    
    attributes = models.BinaryField(
        default = b''
    )

    class Meta:
        db_table = 'player_items'
        unique_together = ['player', 's_id']
        verbose_name = _('item')
        verbose_name_plural = _('items')

    def __str__(self):
        return '%s (s_id: %d, p_id: %d, item_type: %d, count: %d)' % (
            self.player.name, self.s_id, self.p_id, self.item_type, self.count
        )

class PlayerDepotItem(models.Model):
    
    player = models.ForeignKey(
        'players.Player', 
        on_delete = models.CASCADE,
        db_index = True
    )
    
    depot_id = models.PositiveSmallIntegerField(
        default = 0
    )
    
    s_id = models.IntegerField()
    
    p_id = models.IntegerField(default = 0)
    
    item_type = models.IntegerField()
    
    count = models.IntegerField(default = 0)
    
    attributes = models.BinaryField(
        default = b''
    )

    class Meta:
        db_table = 'player_depotitems'
        unique_together = ['player', 's_id']
        verbose_name = _('depot item')
        verbose_name_plural = _('depot items')

    def __str__(self):
        return '%s (s_id: %d, p_id: %d, item_type: %d, count: %d)' % (
            self.player.name, self.s_id, self.p_id, self.item_type, self.count
        )
