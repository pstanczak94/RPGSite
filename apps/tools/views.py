from django.views.generic import FormView
from django.forms.forms import Form

class SuccessViewMixin(object):

    def render_success(self, **kwargs):
        title = getattr(self, 'title_success', 'Title')
        context = self.get_context_data(success=True, title=title, **kwargs)
        return self.render_to_response(context)

    def render_failed(self, **kwargs):
        title = getattr(self, 'title_failed', 'Title')
        context = self.get_context_data(success=False, title=title, **kwargs)
        return self.render_to_response(context)

class CustomFormView(FormView):
    
    form_class = Form
    
    title = 'CustomFormView.Title'
    success_title = None
    
    _success = False

    def get(self, request, *args, **kwargs):
        return self.render_clean()
    
    def form_valid(self, form):
        return self.render_success()
    
    def form_invalid(self, form):
        return self.render_failed()
    
    @property
    def get_title(self):
        if self._success and self.success_title:
            return self.success_title
        else:
            return self.title
    
    @property
    def is_success(self):
        return self._success
    
    def render_clean(self):
        return self.render_form()

    def render_success(self, **kwargs):
        self._success = True
        return self.render_form(**kwargs)
    
    def render_failed(self, **kwargs):
        self._success = False
        return self.render_form(**kwargs)
    
    def render_form(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))
    
    