import hashlib

from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, RegexValidator, MaxLengthValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from rpgsite.tools import CaseInsensitiveKwargs, GetCurrentTimestamp, GetSetting

def get_name_help_text():
    return _(
        'Account name needs to be from {min} to {max} characters length.\n'
        'Allowed characters are: a-z, A-Z, 0-9.'
    ).format(
        min=GetSetting('INPUT_USERNAME_MIN_LENGTH'),
        max=GetSetting('INPUT_USERNAME_MAX_LENGTH')
    )

def get_password_help_text():
    return _(
        'Password needs to be from {min} to {max} characters length.\n'
        'It can\'t be too common or contain only numbers.'
    ).format(
        min=GetSetting('INPUT_PASSWORD_MIN_LENGTH'),
        max=GetSetting('INPUT_PASSWORD_MAX_LENGTH')
    )

class AccountManager(models.Manager):

    def filter(self, **kwargs):
        kwargs = CaseInsensitiveKwargs('name', **kwargs)
        return super(AccountManager, self).filter(**kwargs)

    def get(self, **kwargs):
        kwargs = CaseInsensitiveKwargs('name', **kwargs)
        return super(AccountManager, self).get(**kwargs)

    def get_by_natural_key(self, name):
        return self.get(name=name)

    def name_exists(self, name):
        return self.get_queryset().filter(name=name).exists()

    def _create_account(self, user, name, email, password):
        account = self.model(user=user, name=name, email=email)
        account.set_password(password)
        account.save()
        return account

    def create_account(self, name, email, password):
        user = User.objects.create_user(username=name, email=email, password=password)
        return self._create_account(user=user, name=name, email=email, password=password)

    def create_admin(self, name, email, password):
        user = User.objects.create_superuser(username=name, email=email, password=password)
        return self._create_account(user=user, name=name, email=email, password=password)

class Account(models.Model):

    objects = AccountManager()

    user = models.OneToOneField('auth.User', models.CASCADE, related_name='account')

    name = models.CharField(
        _('name'),
        max_length = 32,
        unique = True,
        help_text = get_name_help_text(),
        validators = [
            RegexValidator(
                regex = GetSetting('INPUT_USERNAME_REGEX'),
                message = _('Account name may contain only english letters and digits.')
            ),
            MinLengthValidator(GetSetting('INPUT_USERNAME_MIN_LENGTH')),
            MaxLengthValidator(GetSetting('INPUT_USERNAME_MAX_LENGTH'))
        ],
        error_messages = {
            'unique': _("An account with that name already exists."),
        },
    )

    password = models.CharField(
        _('hashed password'),
        max_length = 40,
        help_text = get_password_help_text(),
    )

    email = models.EmailField(
        _('email address'),
        max_length = 255,
        help_text = _('This email address will be used for account recovery.'),
    )

    creation = models.IntegerField(
        _('creation timestamp'),
        default = GetCurrentTimestamp,
    )

    def get_creation_display(self):
        return str(datetime.fromtimestamp(self.creation))
    get_creation_display.short_description = _('date created')

    access = models.IntegerField(
        _('access level'),
        default = 1,
        choices = (
            (1, _('Normal')),
            (2, _('Tutor')),
            (3, _('Senior Tutor')),
            (4, _('Gamemaster')),
            (5, _('God')),
        ),
        help_text = _('This field describes the access level of an account.'),
        db_column = 'type',
    )

    secret = models.CharField(
        _('secret auth token'),
        blank = True,
        null = True,
        max_length = 16,
        help_text = _('Secret token used by a game server to authenticate accounts.'),
    )

    premdays = models.IntegerField(
        _('premium days'),
        default = 0,
        help_text = _('Number of premium days left.'),
    )

    lastday = models.PositiveIntegerField(
        _('last premium day'),
        default = 0,
        help_text = _('This field is a helper for premium days calculations.'),
    )

    class Meta:
        managed = False
        db_table = 'accounts'

    def __str__(self):
        return self.name

    @staticmethod
    def make_password_sha1(raw_password):
        return hashlib.sha1(raw_password.encode('utf-8')).hexdigest()

    def change_password(self, raw_password):
        self.set_password(raw_password)
        self.save()
        self.user.set_password(raw_password)
        self.user.save()

    def check_password(self, raw_password):
        return self.user.check_password(raw_password)

    def set_password(self, raw_password):
        self.password = Account.make_password_sha1(raw_password)

    def can_add_character(self):
        return self.players.count() < GetSetting('MAX_PLAYERS_PER_ACCOUNT')

    # def get_active_bans(self):
    #     return self.banned_account.filter(active=True)
    #
    # def get_ban_info(self):
    #     for ban in self.get_active_bans():
    #         if ban.permament:
    #             return str(_(
    #                 'This account has been permamently banned.\n'
    #                 'Ban reason: {reason}.'
    #             ).format(
    #                 reason = ban.get_reason_display()
    #             ))
    #         if not ban.has_expired:
    #             return str(_(
    #                 'This account has been banned.\n'
    #                 'Ban reason: {reason}.\n'
    #                 'Ban expires: {expires}.'
    #             ).format(
    #                 reason = ban.get_reason_display(),
    #                 expires = GetLocalDateTime(ban.expires)
    #             ))
    #     return ''
    #
    # def generate_email_activation_key(self):
    #     seed = settings.SECRET_KEY + self.name + self.email
    #     return hashlib.sha256(seed.encode('utf-8')).hexdigest()
    #
    # def initialize_email_activation(self):
    #     if self.email:
    #         EmailActivation.objects.create(
    #             user = self.user,
    #             email_activation_key = self.generate_email_activation_key(),
    #         )
    #
    # def set_email_activated(self):
    #     self.emailactivation_set.activated = True
    #     self.emailactivation_set.save()

class AccountVipList(models.Model):
    account = models.ForeignKey('Account', models.CASCADE)
    player = models.ForeignKey('players.Player', models.CASCADE)
    description = models.CharField(max_length=128, default='')
    icon = models.IntegerField(default=0)
    notify = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'account_viplist'
        unique_together = (('account', 'player'),)

class AccountBanHistory(models.Model):
    account = models.ForeignKey('Account', models.DO_NOTHING)
    reason = models.CharField(max_length=255)
    banned_at = models.BigIntegerField()
    expired_at = models.BigIntegerField()
    banned_by = models.ForeignKey('players.Player', models.DO_NOTHING, db_column='banned_by')

    class Meta:
        managed = False
        db_table = 'account_ban_history'

class AccountBans(models.Model):
    account = models.OneToOneField('Account', models.DO_NOTHING, primary_key=True)
    reason = models.CharField(max_length=255)
    banned_at = models.BigIntegerField()
    expires_at = models.BigIntegerField()
    banned_by = models.ForeignKey('players.Player', models.DO_NOTHING, db_column='banned_by')

    class Meta:
        managed = False
        db_table = 'account_bans'

# def get_email_expiration_date():
#     return timezone.now() + GetSetting('EMAIL_VERIFICATION_TIME')

# class EmailActivation(models.Model):
#
#     account = models.OneToOneField('accounts.Account', models.CASCADE)
#
#     activated = models.BooleanField(
#         _('email activated'),
#         default = False,
#         help_text = _('Designates whether this user has verified his email.'),
#     )
#
#     key = models.CharField(
#         _('email activation token'),
#         max_length = 64,
#     )
#
#     expires = models.DateTimeField(
#         _('expiration date of the email activation token'),
#         default = get_email_expiration_date,
#     )
