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

    def clean(self):
        super(LoginForm, self).clean()

        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')

            try:
                account = Account.objects.get_by_natural_key(username)
            except Account.DoesNotExist:
                self.add_form_error(_('Account with that name does not exist.'), 'username')
            else:
                if not account.user.check_password(password):
                    self.add_form_error(_('Password does not match.'), 'password')
                elif not account.user.is_active:
                    self.add_form_error(_('This account is blocked or deleted.'))
                else:
                    self.account = account

        return self.cleaned_data

class RegisterForm(CustomModelForm):
    autofocus_post_clean = True

    class Meta:
        model = Account
        fields = ['name', 'password', 'password_repeat', 'email']

    name = CharField(
        autofocus = True,
        label = _('Account name'),
        placeholder = _('Type your account name here'),
        help_text = Account._meta.get_field('name').help_text,
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
        self.instance = Account.objects.create_account(
            name = self.cleaned_data.get('name'),
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
        fields = ['name', 'activation_key']

    name = CharField(
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

        name = self.cleaned_data.get('name')
        activation_key = self.cleaned_data.get('activation_key')

        try:
            account = Account.objects.get_by_natural_key(name)
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
