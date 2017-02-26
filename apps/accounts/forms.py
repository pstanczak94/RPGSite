from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.tools.forms import AutoFocusFormMixin, CharField

from .models import Account

username_validators = [
    RegexValidator(
        settings.INPUT_USERNAME_REGEX,
        _('Username contains illegal characters.')
    ),
]

password_validators = []

email_validators = [
    EmailValidator(
        _('This is not a valid email.')
    ),
]

def get_username_help_text():
    return _('Username length: from {min} to {max}. '
             'Allowed characters: a-z, A-Z, 0-9.'
             .format(min=settings.INPUT_USERNAME_MIN_LENGTH,
                     max=settings.INPUT_USERNAME_MAX_LENGTH))

def get_password_help_text():
    return _('Password length: from {min} to {max}. '
             'All characters are allowed.<br>'
             'It can\'t be too common or contain only numbers.'
             .format(min=settings.INPUT_PASSWORD_MIN_LENGTH,
                     max=settings.INPUT_PASSWORD_MAX_LENGTH))

class LoginForm(AutoFocusFormMixin, forms.Form):

    next = CharField(
        required = False,
        max_length = 500,
        widget = forms.HiddenInput(),
    )

    username = CharField(
        autofocus = True,
        max_length = 150,
        label = _('Username'),
        placeholder = _('Type your username here'),
        widget = forms.TextInput(),
    )

    password = CharField(
        max_length = 100,
        label = _('Password'),
        placeholder = _('Type your password here'),
        widget = forms.PasswordInput(),
    )
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.account = None

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()

        if not self.is_valid():
            return

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        try:
            account = Account.objects.get_by_natural_key(username)
        except ObjectDoesNotExist:
            self.add_form_error(_('Account with that name does not exist.'), 'username')
            return

        if not account.check_password(password):
            self.add_form_error(_('Password does not match.'), 'password')
            return

        if not account.is_active or account.blocked:
            self.add_form_error(_('This account is blocked or deleted.'))
            return

        if not user:
            self.add_form_error(_('You cannot log into this account.'))
            return

        self.account = account

class RegisterForm(AutoFocusFormMixin, forms.Form):

    username = CharField(
        autofocus = True,
        label = _('Username'),
        placeholder = _('Type your new username here'),
        help_text = get_username_help_text(),
        min_length = settings.INPUT_USERNAME_MIN_LENGTH,
        max_length = settings.INPUT_USERNAME_MAX_LENGTH,
        validators = username_validators,
        widget = forms.TextInput(),
    )

    password = CharField(
        label = _('Password'),
        placeholder = _('Type your new password here'),
        help_text = get_password_help_text(),
        min_length = settings.INPUT_PASSWORD_MIN_LENGTH,
        max_length = settings.INPUT_PASSWORD_MAX_LENGTH,
        validators = password_validators,
        widget = forms.PasswordInput(),
    )

    password_repeat = CharField(
        label = _('Repeat password'),
        placeholder = _('Repeat your password here'),
        help_text = _('This password needs to match above.'),
        min_length = settings.INPUT_PASSWORD_MIN_LENGTH,
        max_length = settings.INPUT_PASSWORD_MAX_LENGTH,
        validators = password_validators,
        widget = forms.PasswordInput(),
    )

    email = CharField(
        label = _('Email address'),
        placeholder = _('Type your email address here'),
        help_text = _('This email will be verified later and used for account recovery.'),
        min_length = settings.INPUT_EMAIL_MIN_LENGTH,
        max_length = settings.INPUT_EMAIL_MAX_LENGTH,
        validators = email_validators,
        widget = forms.EmailInput(),
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.account = None

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        if not self.is_valid():
            return

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')
        email = cleaned_data.get('email')

        if Account.objects.username_exists(username):
            self.add_error('username', _('Username is already in use.'))
            return

        if Account.objects.email_exists(email):
            self.add_error('email', _('This email is bound to another account.'))
            return

        try:
            validate_password(password)
        except ValidationError as e:
            self.add_error('password', e.messages)
            return
            
        if password != password_repeat:
            self.add_error('password', _('You didn\'t repeat new password correctly.'))
            return
    
        account = Account.objects.create_account(username, password=password, email=email)

        if not account:
            self.add_form_error(_('Account creation failed. Please, try again.'))
            return

        self.account = account

class PasswordChangeForm(AutoFocusFormMixin, forms.Form):
    autofocus_post_clean = False

    current_password = CharField(
        autofocus = True,
        label = _('Current password'),
        placeholder = _('Type your current password here'),
        help_text = _('For security reasons you need to type your current password.'),
        max_length = 100,
        widget = forms.PasswordInput(),
    )

    password = CharField(
        label = _('New password'),
        placeholder = _('Type your new password here'),
        help_text = get_password_help_text(),
        min_length = settings.INPUT_PASSWORD_MIN_LENGTH,
        max_length = settings.INPUT_PASSWORD_MAX_LENGTH,
        validators = password_validators,
        widget = forms.PasswordInput(),
    )

    password_repeat = CharField(
        label = _('Repeat new password'),
        placeholder = _('Repeat your new password here'),
        help_text = _('This password needs to match above.'),
        min_length = settings.INPUT_PASSWORD_MIN_LENGTH,
        max_length = settings.INPUT_PASSWORD_MAX_LENGTH,
        validators = password_validators,
        widget = forms.PasswordInput(),
    )

    def __init__(self, account, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.account = account

    def clean(self):
        cleaned_data = super(PasswordChangeForm, self).clean()

        if not self.is_valid():
            return

        current_password = cleaned_data.get('current_password')
        password = cleaned_data.get('password')
        password_repeat = cleaned_data.get('password_repeat')

        if not self.account.check_password(current_password):
            self.add_form_error(_('Your current password is other.'))
            return

        if password != password_repeat:
            self.add_form_error(_('You didn\'t repeat new password correctly.'))
            return

class EmailVerificationForm(AutoFocusFormMixin, forms.Form):
    autofocus_post_clean = False

    username = CharField(
        required = False,
        max_length = 150,
        widget = forms.HiddenInput(),
    )

    activation_key = CharField(
        autofocus = True,
        label = _('Verification key'),
        help_text = _('Verification key can be found in email box after account creation.'),
        placeholder = _('Copy your verification key here'),
        min_length = 64,
        max_length = 64,
        widget = forms.TextInput(),
    )

    def clean(self):
        data = super(EmailVerificationForm, self).clean()

        if not self.is_valid():
            return data

        username = data.get('username')
        key = data.get('activation_key')

        try:
            account = Account.objects.get_by_natural_key(username)
        except Account.DoesNotExist:
            self.add_form_error(_('Account doesn\'t exist, verification failed.'))
            return data

        if account.email_activated:
            self.add_form_error(_('Your email is already activated.'))
            return data

        if not account.email_activation_key or not account.email_key_expires:
            self.add_form_error(_('Your email can\'t be activated.'))
            return data

        if timezone.now() > account.email_key_expires:
            self.add_form_error(_('Email verification time expired.'))
            return data

        if account.email_activation_key != key:
            self.add_form_error(_('Verification key is wrong.'))
            return data

