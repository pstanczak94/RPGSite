from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import Http404
from django.urls.base import reverse, reverse_lazy
from django.views.generic.edit import DeleteView

from apps.guilds.forms import CreateForm
from apps.guilds.models import Guild
from apps.tools.views import CustomFormView

from django.utils.translation import ugettext_lazy as _

class CreateView(LoginRequiredMixin, CustomFormView):
    form_class = CreateForm
    template_name = 'guilds/create.html'
    title = 'Guild creation'
    success_title = 'Guild created'

    def get_form_kwargs(self):
        kwargs = super(CreateView, self).get_form_kwargs()
        kwargs['account'] = self.request.user.account
        return kwargs

    def form_valid(self, form):
        form.save()

        return self.render_success(
            next = reverse('accounts:profile'),
            name = form.instance.name,
        )

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Guild
    template_name = 'guilds/delete.html'
    success_url = reverse_lazy('accounts:profile')

    def check_owner(self, request):
        if self.get_object().owner not in request.user.account.players.all():
            raise Http404(_('You can\'t delete this guild.'))

    def get(self, request, *args, **kwargs):
        self.check_owner(request)
        return super(DeleteView, self).get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.check_owner(request)
        return super(DeleteView, self).delete(request, *args, **kwargs)