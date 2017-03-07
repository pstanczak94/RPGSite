from django.db import models
from django.utils.translation import ugettext_lazy as _

from rpgsite.tools import CaseInsensitiveKwargs, GetCurrentTimestamp

class PlayerManager(models.Manager):

    def filter(self, **kwargs):
        kwargs = CaseInsensitiveKwargs('name', **kwargs)
        return super(PlayerManager, self).filter(**kwargs)

    def get(self, **kwargs):
        kwargs = CaseInsensitiveKwargs('name', **kwargs)
        return super(PlayerManager, self).get(**kwargs)

    def get_by_natural_key(self, name):
        return self.get(name__iexact=name)

    def name_exists(self, name):
        return self.get_queryset().filter(name__iexact=name).exists()
    
class Player(models.Model):
    
    objects = PlayerManager()
    
    SEX_CHOICES = (
        (1, _('Male')),
        (0, _('Female')),
    )

    VOCATION_CHOICES = (
        (4, _('Knight')),
        (3, _('Paladin')),
        (1, _('Sorcerer')),
        (2, _('Druid')),
        # (0, _('None')),
        # (5, _('Master Sorcerer')),
        # (6, _('Elder Druid')),
        # (7, _('Royal Paladin')),
        # (8, _('Elite Knight')),
    )

    TOWN_CHOICES = (
        (1, _('Trekolt')),
        (2, _('Rhyves')),
        (3, _('Varak')),
        (4, _('Jorvik')),
        (5, _('Saund')),
    )

    name = models.CharField(
        max_length = 30,
        unique = True,
    )

    group_id = models.SmallIntegerField(
        default = 1,
    )

    account = models.ForeignKey(
        'accounts.Account', 
        on_delete = models.CASCADE,
        related_name = 'players',
    )

    level = models.IntegerField(
        default = 1,
    )
    
    vocation = models.SmallIntegerField(
        default = VOCATION_CHOICES[0][0],
        choices = VOCATION_CHOICES,
        db_index = True,
    )

    health = models.IntegerField(
        default = 150,
    )

    healthmax = models.IntegerField(
        default = 150,
    )

    experience = models.BigIntegerField(
        default = 0,
    )

    lookbody = models.IntegerField(
        default = 0,
    )

    lookfeet = models.IntegerField(
        default = 0,
    )

    lookhead = models.IntegerField(
        default = 0,
    )

    looklegs = models.IntegerField(
        default = 0,
    )

    looktype = models.IntegerField(
        default = 136,
    )

    lookaddons = models.IntegerField(
        default = 0,
    )
    
    maglevel = models.IntegerField(
        default = 0,
    )
    
    mana = models.IntegerField(
        default = 0,
    )
    
    manamax = models.IntegerField(
        default = 0,
    )
    
    manaspent = models.IntegerField(
        default = 0,
    )
    
    soul = models.IntegerField(
        default = 0,
    )

    town_id = models.SmallIntegerField(
        default = TOWN_CHOICES[0][0],
        choices = TOWN_CHOICES,
    )
    
    posx = models.IntegerField(
        default = 0,
    )
    
    posy = models.IntegerField(
        default = 0,
    )
    
    posz = models.IntegerField(
        default = 0,
    )

    conditions = models.BinaryField(
        default = b'',
    )
    
    cap = models.IntegerField(
        default = 150,
    )

    sex = models.PositiveSmallIntegerField(
        default = SEX_CHOICES[0][0],
        choices = SEX_CHOICES,
    )

    lastlogin = models.BigIntegerField(default=0)
    lastlogout = models.BigIntegerField(default=0)
    lastip = models.IntegerField(default=0)
    save_on_logout = models.BooleanField(default=True, db_column='save')
    stamina = models.SmallIntegerField(default=2520)
    skull = models.BooleanField(default=False)
    skulltime = models.IntegerField(default=0)
    balance = models.PositiveIntegerField(default=0)
    blessings = models.IntegerField(default=0)
    onlinetime = models.IntegerField(default=0)
    deletion = models.BigIntegerField(default=0)
    offlinetraining_time = models.SmallIntegerField(default=43200)
    offlinetraining_skill = models.IntegerField(default=-1)
    skill_fist = models.IntegerField(default=10)
    skill_fist_tries = models.BigIntegerField(default=0)
    skill_club = models.IntegerField(default=10)
    skill_club_tries = models.BigIntegerField(default=0)
    skill_sword = models.IntegerField(default=10)
    skill_sword_tries = models.BigIntegerField(default=0)
    skill_axe = models.IntegerField(default=10)
    skill_axe_tries = models.BigIntegerField(default=0)
    skill_dist = models.IntegerField(default=10)
    skill_dist_tries = models.BigIntegerField(default=0)
    skill_shielding = models.IntegerField(default=10)
    skill_shielding_tries = models.BigIntegerField(default=0)
    skill_fishing = models.IntegerField(default=10)
    skill_fishing_tries = models.BigIntegerField(default=0)

    creation = models.IntegerField(
        default = GetCurrentTimestamp
    )

    class Meta:
        managed = False
        db_table = 'players'

    def __str__(self):
        return self.name

    # def check_is_banned(self):
    #     for ban in self.banned_player.filter(active=True):
    #         if ban.permament or not ban.has_expired:
    #             return True
    #     return False
    #
    # def get_active_bans(self):
    #     return self.banned_player.filter(active=True)
    #
    # def get_ban_info(self):
    #     for ban in self.get_active_bans():
    #         if ban.permament:
    #             return str(_(
    #                 'This player has been permamently banned.\n'
    #                 'Ban reason: {reason}.'
    #             ).format(
    #                 reason = ban.get_reason_display()
    #             ))
    #         if not ban.has_expired:
    #             return str(_(
    #                 'This player has been banned.\n'
    #                 'Ban reason: {reason}.\n'
    #                 'Ban expires: {expires}.'
    #             ).format(
    #                 reason = ban.get_reason_display(),
    #                 expires = GetLocalDateTime(ban.expires)
    #             ))
    #     return ''

class PlayerNamelock(models.Model):
    player = models.OneToOneField('players.Player', models.CASCADE, primary_key=True, related_name='namelocked_player')
    reason = models.CharField(max_length=255)
    namelocked_at = models.BigIntegerField()
    namelocked_by = models.ForeignKey('players.Player', models.SET_NULL, null=True, db_column='namelocked_by')

    class Meta:
        managed = False
        db_table = 'player_namelocks'

class PlayerDeath(models.Model):
    player = models.ForeignKey('players.Player', models.CASCADE)
    time = models.BigIntegerField()
    level = models.IntegerField()
    killed_by = models.CharField(max_length=255)
    is_player = models.IntegerField()
    mostdamage_by = models.CharField(max_length=100)
    mostdamage_is_player = models.IntegerField()
    unjustified = models.IntegerField()
    mostdamage_unjustified = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'player_deaths'

class PlayerDepotItem(models.Model):
    player = models.ForeignKey('players.Player', models.CASCADE)
    sid = models.IntegerField()
    pid = models.IntegerField()
    itemtype = models.SmallIntegerField()
    count = models.SmallIntegerField()
    attributes = models.TextField()

    class Meta:
        managed = False
        db_table = 'player_depotitems'
        unique_together = (('player', 'sid'),)

class PlayerInboxItem(models.Model):
    player = models.ForeignKey('players.Player', models.CASCADE)
    sid = models.IntegerField()
    pid = models.IntegerField()
    itemtype = models.SmallIntegerField()
    count = models.SmallIntegerField()
    attributes = models.TextField()

    class Meta:
        managed = False
        db_table = 'player_inboxitems'
        unique_together = (('player', 'sid'),)

class PlayerItem(models.Model):
    player = models.ForeignKey('players.Player', models.CASCADE)
    pid = models.IntegerField()
    sid = models.IntegerField()
    itemtype = models.SmallIntegerField()
    count = models.SmallIntegerField()
    attributes = models.TextField()

    class Meta:
        managed = False
        db_table = 'player_items'

class PlayerSpell(models.Model):
    player = models.ForeignKey('players.Player', models.DO_NOTHING)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'player_spells'

class PlayerStorage(models.Model):
    player = models.ForeignKey('players.Player', models.DO_NOTHING)
    key = models.IntegerField()
    value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'player_storage'
        unique_together = (('player', 'key'),)