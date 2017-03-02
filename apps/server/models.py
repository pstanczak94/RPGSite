from django.db import models
from django.utils.translation import ugettext as _

from django.utils import timezone
from datetime import timedelta

def default_ban_length():
    return timezone.now() + timedelta(days=7)

class AbstractBan(models.Model):
    
    REASON_CHOICES = (
        (1, _('Cheating')),
        (2, _('Racist')),
        (3, _('Swearing')),
        (4, _('Account sharing')),
        (5, _('Other')),
    )
    
    admin = models.ForeignKey(
        'accounts.Account', 
        null = True, 
        blank = True, 
        on_delete = models.SET_NULL
    )
    
    active = models.BooleanField(
        default = True,
        db_index = True
    )
    
    permament = models.BooleanField(
        default = False
    )
    
    expires = models.DateTimeField(
        default = default_ban_length,
        null = True,
        blank = True
    )
    
    reason = models.PositiveSmallIntegerField(
        default = 1,
        choices = REASON_CHOICES
    )
    
    comment = models.CharField(
        max_length = 255, 
        blank = True
    )
    
    added = models.DateTimeField(
        default = timezone.now,
        editable = False
    )

    class Meta:
        abstract = True

    @property
    def has_expired(self):
        if self.permament:
            return False
        if self.expires and self.expires > timezone.now():
            return False
        return True

class AccountBan(AbstractBan):
    
    banned = models.ForeignKey(
        'accounts.Account',
        on_delete = models.CASCADE,
        related_name = 'banned_account'
    )
    
    class Meta:
        db_table = 'account_bans'
        
class PlayerBan(AbstractBan):
    
    banned = models.ForeignKey(
        'players.Player',
        on_delete = models.CASCADE,
        related_name = 'banned_player'
    )
    
    class Meta:
        db_table = 'player_bans'
        
class IPAddressBan(AbstractBan):
    
    banned = models.GenericIPAddressField()
    
    class Meta:
        db_table = 'ip_bans'
        verbose_name_plural = 'IP address bans'
        verbose_name = 'IP address ban'

class Storage(models.Model):
    
    key = models.PositiveSmallIntegerField(
        primary_key = True
    )
    
    value = models.IntegerField(
        default = 0
    )

    class Meta:
        db_table = 'storage'

class Record(models.Model):
    
    type = models.PositiveSmallIntegerField(
        primary_key = True
    )
    
    record = models.PositiveIntegerField(
        default = 0
    )

    class Meta:
        db_table = 'records'
