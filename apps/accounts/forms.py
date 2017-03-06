from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.forms.widgets import PasswordInput, TextInput, EmailInput
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from apps.accounts.models import get_password_help_text
from apps.tools.forms import AutoFocusFormMixin, CharField, CustomModelForm, EmailField

from .models import Account

class LoginForm(AutoFocusFormMixin, forms.Form):

    next = CharField(
        required = False,
        max_length = 255,
        widget = forms.HiddenInput(),
    )

    username = CharField(
        autofocus = True,
        min_length = settings.INPUT_USERNAME_MIN_LENGTH,
        max_length = settings.INPUT_USERNAME_MAX_LENGTH,
        label = _('Username'),
        placeholder = _('Type your username here'),
        widget = forms.TextInput(),
    )

    password = CharField(
        min_length = settings.INPUT_PASSWORD_MIN_LENGTH,
        max_length = settings.INPUT_PASSWORD_MAX_LENGTH,
        label = _('Password'),
        placeholder = _('Type your password here'),
        widget = forms.PasswordInput(),
    )
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.account = None

    def clean(self):
        data = super(LoginForm, self).clean()

        if not self.is_valid():
            return data

        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        try:
            account = Account.objects.get_by_natural_key(username)
        except Account.DoesNotExist:
            self.add_form_error(_('Account with that name does not exist.'), 'username')
            return data

        if not account.check_password(password):
            self.add_form_error(_('Password does not match.'), 'password')
            return data

        if not account.is_active:
            self.add_form_error(_('This account is blocked or deleted.'))
            return data

        ban_info = account.get_ban_info()

        if ban_info:
            self.add_form_error(ban_info)
            return data

        if not user:
            self.add_form_error(_('Account authentication failed.'))
            return data

        self.account = account
        return data

class RegisterForm(CustomModelForm):
    autofocus_post_clean = True

    class Meta:
        model = Account
        fields = ['username', 'password', 'password_repeat', 'email']

    username = CharField(
        autofocus = True,
        label = _('Username'),
        placeholder = _('Type your username here'),
        help_text = Account._meta.get_field('username').help_text,
        min_length = settings.INPUT_USERNAME_MIN_LENGTH,
        max_length = settings.INPUT_USERNAME_MAX_LENGTH,
        widget = TextInput(),
    )

    password = CharField(
        label = _('Password'),
        placeholder = _('Type your password here'),
        help_text = Account._meta.get_field('password').help_text,
        min_length = settings.INPUT_PASSWORD_MIN_LENGTH,
        max_length = settings.INPUT_PASSWORD_MAX_LENGTH,
        widget = PasswordInput(),
    )

    password_repeat = CharField(
        label = _('Repeat password'),
        placeholder = _('Repeat your password here'),
        help_text = _('This password needs to match above.'),
        min_length = settings.INPUT_PASSWORD_MIN_LENGTH,
        max_length = settings.INPUT_PASSWORD_MAX_LENGTH,
        widget = PasswordInput(),
    )

    email = EmailField(
        label = _('Email address'),
        placeholder = _('Type your email address here'),
        help_text = Account._meta.get_field('email').help_text,
        widget = EmailInput(),
    )

    def save(self, commit=True):
        self.instance = Account.objects.create_user(
            username = self.cleaned_data.get('username'),
            password = self.cleaned_data.get('password'),
            email = self.cleaned_data.get('email')
        )
        return self.instance

    def clean(self):
        super(RegisterForm, self).clean()

        password = self.cleaned_data.get('password')
        password_repeat = self.cleaned_data.get('password_repeat')

        try:
            validate_password(password)
        except ValidationError as e:
            self.add_error('password', e.messages)

        if password != password_repeat:
            self.add_error('password_repeat', _('You didn\'t repeat your password correctly.'))

        return self.cleaned_data

class PasswordChangeForm(CustomModelForm):
    autofocus_post_clean = False

    class Meta:
        model = Account
        fields = ['current_password', 'new_password', 'new_password_repeat']

    current_password = CharField(
        autofocus = True,
        label = _('Current password'),
        placeholder = _('Type your current password here'),
        help_text = _('For security reasons you need to type your current password.'),
        min_length = settings.INPUT_PASSWORD_MIN_LENGTH,
        max_length = settings.INPUT_PASSWORD_MAX_LENGTH,
        widget = forms.PasswordInput(),
    )

    new_password = CharField(
        label = _('New password'),
        placeholder = _('Type your new password here'),
        help_text = get_password_help_text(),
        min_length = settings.INPUT_PASSWORD_MIN_LENGTH,
        max_length = settings.INPUT_PASSWORD_MAX_LENGTH,
        widget = forms.PasswordInput(),
    )

    new_password_repeat = CharField(
        label = _('Repeat new password'),
        placeholder = _('Repeat your new password here'),
        help_text = _('This password needs to match above.'),
        min_length = settings.INPUT_PASSWORD_MIN_LENGTH,
        max_length = settings.INPUT_PASSWORD_MAX_LENGTH,
        widget = forms.PasswordInput(),
    )

    def save(self, commit=True):
        self.instance.change_password(
            self.cleaned_data.get('current_password'),
            self.cleaned_data.get('new_password')
        )
        return self.instance

    def clean(self):
        super(PasswordChangeForm, self).clean()

        current_password = self.cleaned_data.get('current_password')
        new_password = self.cleaned_data.get('new_password')
        new_password_repeat = self.cleaned_data.get('new_password_repeat')

        if not self.instance.check_password(current_password):
            self.add_error('current_password', _('Your current password is other.'))

        try:
            validate_password(new_password)
        except ValidationError as e:
            self.add_error('new_password', e.messages)

        if new_password != new_password_repeat:
            self.add_error('new_password_repeat', _('You didn\'t repeat new password correctly.'))

        return self.cleaned_data

class EmailVerificationForm(CustomModelForm):
    autofocus_post_clean = False

    class Meta:
        model = Account
        fields = ['username', 'activation_key']

    username = CharField(
        required = False,
        min_length = settings.INPUT_USERNAME_MIN_LENGTH,
        max_length = settings.INPUT_USERNAME_MAX_LENGTH,
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

    def save(self, commit=True):
        self.instance.set_email_activated()
        return self.instance

    def clean(self):
        super(EmailVerificationForm, self).clean()

        username = self.cleaned_data.get('username')
        activation_key = self.cleaned_data.get('activation_key')

        try:
            account = Account.objects.get_by_natural_key(username)
        except Account.DoesNotExist:
            self.add_error(None, _('Account doesn\'t exist, verification failed.'))
        else:
            self.instance = account
            if account.email_activated:
                self.add_error(None, _('Your email is already activated.'))
            elif not account.email_activation_key or not account.email_key_expires:
                self.add_error(None, _('Your email can\'t be activated.'))
            elif timezone.now() > account.email_key_expires:
                self.add_error(None, _('Email verification time expired.'))
            elif account.email_activation_key != activation_key:
                self.add_error(None, _('Verification key is wrong.'))

        return self.cleaned_data
