from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.utils.translation import ugettext_lazy as _
from django.views import generic as views

from apps.tools.views import CustomFormView

from . import forms
from .models import Account

class IndexView(views.RedirectView):
    pattern_name = 'accounts:profile'

class ProfileView(LoginRequiredMixin, views.TemplateView):
    template_name = 'accounts/profile.html'
    
    def get(self, request, *args, **kwargs):
        kwargs.update({
            'account': request.user,
            'players': request.user.get_players,
            'players_count': request.user.get_players.count(),
            'can_add_player': request.user.can_add_character,
            'players_max': settings.MAX_PLAYERS_PER_ACCOUNT,
        })
        return super(ProfileView, self).get(request, *args, **kwargs)
    
class LoginView(CustomFormView):
    form_class = forms.LoginForm
    template_name = 'accounts/login.html'
    title = _('Login')
    success_title = _('Logged in')

    def get_initial(self):
        data = super(LoginView, self).get_initial()
        data['next'] = self.get_next_page()
        return data

    def get_next_page(self):
        if 'next' in self.request.GET:
            return self.request.GET.get('next')
        if 'next' in self.request.POST:
            return self.request.POST.get('next')
        return ''

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        if self.is_success and not self.get_next_page():
            context['next'] = settings.LOGIN_REDIRECT_URL
        else:
            context['next'] = self.get_next_page()
        return context

    def form_valid(self, form):
        
        login(self.request, form.account)
        
        return super(LoginView, self).form_valid(form)

class LogoutView(CustomFormView):
    template_name = 'accounts/logout.html'
    title = _('Logout')
    success_title = _('Logged out')

    def render_clean(self):
        if not self.request.user.is_authenticated:
            return self.render_failed()

        logout(self.request)
        
        return self.render_success(
            next = settings.LOGOUT_REDIRECT_URL
        )

class RegisterView(CustomFormView):
    form_class = forms.RegisterForm
    template_name = 'accounts/create.html'
    title = _('Account creation')
    success_title = _('Account created')

    def form_valid(self, form):

        activation_link = '{scheme}://{host}{url}?user={user}&key={key}'.format(
            scheme = self.request.scheme,
            host = self.request.get_host(),
            url = reverse('accounts:email-activation'),
            user = form.account.username,
            key = form.account.email_activation_key
        )

        # TODO: send activation link to account.email
        print(activation_link)

        return self.render_success(
            username = form.account.username,
            email = form.account.email
        )

class PasswordChangeView(LoginRequiredMixin, CustomFormView):
    form_class = forms.PasswordChangeForm
    template_name = 'accounts/password-change.html'
    title = _('Password change')
    success_title = _('Password changed')

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs['account'] = self.request.user
        return kwargs

    def form_valid(self, form):
        old_password = form.cleaned_data.get('current_password')
        new_password = form.cleaned_data.get('password')

        account = self.request.user
        account.change_password(old_password, new_password)
        user = authenticate(username=account.username, password=new_password)
        login(self.request, user)

        return self.render_success(
            next = reverse('accounts:profile')
        )

class EmailVerificationView(CustomFormView):
    form_class = forms.EmailVerificationForm
    template_name = 'accounts/email-activate.html'
    title = _('Email verification')
    success_title = _('Email activated')

    def get_initial(self):
        data = super(EmailVerificationView, self).get_initial()
        data['username'] = self.get_username()
        data['activation_key'] = self.request.GET.get('key', '')
        return data

    def get_username(self):
        if 'user' in self.request.GET:
            return self.request.GET.get('user')
        elif self.request.user.is_authenticated:
            return self.request.user.username
        else:
            return ''

    def render_clean(self):
        if not self.get_username():
            return HttpResponseRedirect('%s?next=%s' % (
                settings.LOGIN_URL, reverse('accounts:email-activation')
            ))
        
        return super(EmailVerificationView, self).render_clean()

    def form_valid(self, form):
        username = form.cleaned_data.get('username')

        account = Account.objects.get_by_natural_key(username)
        account.set_email_activated()

        return self.render_success(
            next = reverse('index')
        )
