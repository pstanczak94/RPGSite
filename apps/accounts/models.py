import hashlib

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.tools.tools import CaseInsensitiveKwargs, LogError

def default_email_expiration():
    return timezone.now() + settings.EMAIL_VERIFICATION_TIME

class AccountManager(auth_models.UserManager):

    def filter(self, **kwargs):
        kwargs = CaseInsensitiveKwargs(self.model.USERNAME_FIELD, **kwargs)
        return super(AccountManager, self).filter(**kwargs)

    def get(self, **kwargs):
        kwargs = CaseInsensitiveKwargs(self.model.USERNAME_FIELD, **kwargs)
        return super(AccountManager, self).get(**kwargs)

    def username_exists(self, username):
        return self.get_queryset().filter(username__iexact=username).exists()

    def email_exists(self, email):
        return self.get_queryset().filter(email__iexact=email).exists()

    def create_account(self, username, password=None, email=None):
        try:
            account = self.create_user(username, email=email, password=password)
            account.init_email_verification()
        except Exception as e:
            LogError(repr(e))
            return None
        else:
            return account

class Account(auth_models.AbstractUser):
    
    objects = AccountManager()

    full_name = models.CharField(
        _('full name'),
        max_length = 50,
        default = '',
        blank = True,
    )

    # blocked = models.BooleanField(
    #     _('blocked'),
    #     default = False,
    #     help_text = _('Designates whether this user is blocked.'),
    # )
    #
    # warned = models.BooleanField(
    #     _('warned'),
    #     default = False,
    #     help_text = _('Designates whether this user was warned.'),
    # )

    email_activated = models.BooleanField(
        _('email activated'),
        default = False,
        help_text = _('Designates whether this user has verified his email.'),
    )

    email_activation_key = models.CharField(
        max_length = 64,
        default = '',
        blank = True,
    )

    email_key_expires = models.DateTimeField(
        default = None,
        null = True,
        blank = True,
    )

    class Meta:
        db_table = 'accounts'
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def __str__(self):
        return self.username

    @property
    def get_short_name(self):
        if self.first_name:
            return self.first_name
        else:
            return self.username
    
    @property
    def has_full_name(self):
        return self.full_name or self.first_name or self.last_name

    @property
    def get_full_name(self):
        if self.full_name:
            return self.full_name.strip()
        elif self.first_name or self.last_name:
            return super(Account, self).get_full_name()
        else:
            return self.username

    @property
    def get_active_bans(self):
        return self.banned_account.filter(active=True)

    def change_password(self, old_password, new_password):
        if self.has_usable_password() and not self.check_password(old_password):
            raise ValueError('Password does not match.')
        else:
            self.set_password(new_password)
            self.save()

    @property
    def get_players(self):
        return self.player_set.all()
    
    @property
    def can_add_character(self):
        return self.get_players.count() < settings.MAX_PLAYERS_PER_ACCOUNT

    def generate_email_key(self):
        seed = settings.SECRET_KEY + self.username + self.email
        return hashlib.sha256(seed.encode('utf-8')).hexdigest()

    def init_email_verification(self):
        if not self.email:
            raise ValueError('Email address is not set.')
        else:
            self.email_activation_key = self.generate_email_key()
            self.email_key_expires = default_email_expiration()
            self.save()

    def set_email_activated(self):
        self.email_activated = True
        self.email_activation_key = ''
        self.email_key_expires = None
        self.save()

class AccountGroup(auth_models.Group):
    class Meta:
        proxy = True
        verbose_name = _('group')
        verbose_name_plural = _('groups')
