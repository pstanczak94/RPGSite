from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls.base import reverse

from apps.guilds.forms import CreateForm
from apps.tools.views import CustomFormView

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