import hashlib

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.core.validators import MinLengthValidator, RegexValidator, MaxLengthValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.tools.tools import CaseInsensitiveKwargs, GetLocalDateTime

def get_username_help_text():
    return _(
        'Username needs to be from {min} to {max} characters length.\n'
        'Allowed characters are: a-z, A-Z, 0-9.'
    ).format(
        min=settings.INPUT_USERNAME_MIN_LENGTH,
        max=settings.INPUT_USERNAME_MAX_LENGTH
    )

def get_password_help_text():
    return _(
        'Password needs to be from {min} to {max} characters length.\n'
        'It can\'t be too common or contain only numbers.'
    ).format(
        min=settings.INPUT_PASSWORD_MIN_LENGTH,
        max=settings.INPUT_PASSWORD_MAX_LENGTH
    )

def get_email_expiration_date():
    return timezone.now() + settings.EMAIL_VERIFICATION_TIME

class AccountManager(auth_models.UserManager):

    def filter(self, **kwargs):
        kwargs = CaseInsensitiveKwargs(self.model.USERNAME_FIELD, **kwargs)
        return super(AccountManager, self).filter(**kwargs)

    def get(self, **kwargs):
        kwargs = CaseInsensitiveKwargs(self.model.USERNAME_FIELD, **kwargs)
        return super(AccountManager, self).get(**kwargs)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD + '__iexact': username})

    def username_exists(self, username):
        return self.get_queryset().filter(username__iexact=username).exists()

    def email_exists(self, email):
        return self.get_queryset().filter(email__iexact=email).exists()

    def _create_user(self, username, email, password, **extra_fields):
        account = super(AccountManager, self)._create_user(username, email, password, **extra_fields)
        account.initialize_email_activation()
        return account

class Account(auth_models.AbstractUser):

    class Meta:
        db_table = 'accounts'
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    objects = AccountManager()

    id = models.AutoField(
        primary_key = True
    )

    username = models.CharField(
        _('username'),
        max_length = 32,
        unique = True,
        help_text = get_username_help_text(),
        validators = [
            RegexValidator(
                regex = settings.INPUT_USERNAME_REGEX,
                message = _('Username may contain only english letters and digits.')
            ),
            MinLengthValidator(settings.INPUT_USERNAME_MIN_LENGTH),
            MaxLengthValidator(settings.INPUT_USERNAME_MAX_LENGTH)
        ],
        error_messages = {
            'unique': _("An account with that username already exists."),
        },
    )

    password = models.CharField(
        _('password'),
        max_length = 128,
        help_text = get_password_help_text()
    )

    email = models.EmailField(
        _('email address'),
        blank = True,
        help_text = _('This email address will be used for account recovery.')
    )

    access = models.PositiveSmallIntegerField(
        _('access level'),
        default = 1,
        choices = (
            (1, _('Normal')),
            (2, _('Tutor')),
            (3, _('Senior Tutor')),
            (4, _('Gamemaster')),
            (5, _('God')),
        ),
        help_text = _('This field describes the access level of an account.')
    )

    secret = models.CharField(
        _('secret auth token'),
        default = '',
        max_length = 16,
        help_text = _('Secret token used by a game server to authenticate accounts.')
    )

    premium_days = models.IntegerField(
        _('premium days'),
        default = 0,
        help_text = _('Number of premium days left.')
    )

    last_day = models.PositiveIntegerField(
        _('last premium day'),
        default = 0,
        help_text = _('This field is a helper for premium days calculations.')
    )

    email_activated = models.BooleanField(
        _('email activated'),
        default = False,
        help_text = _('Designates whether this user has verified his email.'),
    )

    email_activation_key = models.CharField(
        _('email activation token'),
        max_length = 64,
        default = '',
        blank = True,
    )

    email_key_expires = models.DateTimeField(
        _('expiration date of the email activation token'),
        default = None,
        null = True,
        blank = True,
    )

    def __str__(self):
        return self.username

    def get_active_bans(self):
        return self.banned_account.filter(active=True)

    def get_ban_info(self):
        for ban in self.get_active_bans():
            if ban.permament:
                return str(_(
                    'This account has been permamently banned.\n'
                    'Ban reason: {reason}.'
                ).format(
                    reason = ban.get_reason_display()
                ))
            if not ban.has_expired:
                return str(_(
                    'This account has been banned.\n'
                    'Ban reason: {reason}.\n'
                    'Ban expires: {expires}.'
                ).format(
                    reason = ban.get_reason_display(),
                    expires = GetLocalDateTime(ban.expires)
                ))
        return ''

    def change_password(self, old_password, new_password):
        if self.has_usable_password() and not self.check_password(old_password):
            raise ValueError('Password does not match.')
        else:
            self.set_password(new_password)
            self.save()

    def can_add_character(self):
        return self.players.count() < settings.MAX_PLAYERS_PER_ACCOUNT

    def generate_email_activation_key(self):
        seed = settings.SECRET_KEY + self.username + self.email
        return hashlib.sha256(seed.encode('utf-8')).hexdigest()

    def initialize_email_activation(self):
        if self.email:
            self.email_activation_key = self.generate_email_activation_key()
            self.email_key_expires = get_email_expiration_date()
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
