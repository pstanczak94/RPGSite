from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import RedirectView

from apps.tools.views import CustomFormView
from .forms import CreateForm

from django.views import generic as django_views
from apps.players.models import Player
from django.urls.base import reverse_lazy
from django.http.response import Http404
from django.utils.translation import ugettext_lazy as _

class IndexView(RedirectView):
    pattern_name = 'players:create'

class CreateView(LoginRequiredMixin, CustomFormView):
    form_class = CreateForm
    template_name = 'players/create.html'
    title = 'Character creation'
    success_title = 'Character created'
    
    def get_form(self, form_class=None):
        form = super(CreateView, self).get_form(form_class=form_class)
        form.account = self.request.user.account
        return form
    
    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        sex = form.cleaned_data.get('sex')
        vocation = form.cleaned_data.get('vocation')
        town_id = form.cleaned_data.get('town_id')
        
        account = self.request.user.account
        
        player = account.players.create(
            name = name,
            sex = sex,
            vocation = vocation,
            town_id = town_id
        )
        
        return self.render_success(
            name = player.name
        )
    
class DeleteView(LoginRequiredMixin, django_views.DeleteView):
    model = Player
    template_name = 'players/delete.html'
    success_url = reverse_lazy('accounts:profile')
    
    def _check_player(self, request):
        if self.get_object().account != request.user.account:
            raise Http404(_('You can\'t delete this character.'))
    
    def get(self, request, *args, **kwargs):
        self._check_player(request)
        return super(DeleteView, self).get(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        self._check_player(request)
        return super(DeleteView, self).delete(request, *args, **kwargs)

class StatsView(django_views.ListView):
    model = Player
    template_name = 'players/stats.html'
