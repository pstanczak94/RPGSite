from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

class IndexView(TemplateView):
	template_name = 'rpgsite/index.html'

class FaviconView(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		return settings.STATIC_URL + 'icons/rpgsite.ico'

class RobotsView(RedirectView):
	def get_redirect_url(self, *args, **kwargs):
		return settings.STATIC_URL + 'robots.txt'
