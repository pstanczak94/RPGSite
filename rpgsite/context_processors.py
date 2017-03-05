from django.urls.base import reverse
from django.utils.translation import ugettext_lazy as _

class NavigationItem(object):
    def __init__(self, name, link, use_reverse=True):
        self.name = name
        self.link = reverse(link) if use_reverse else link

RPGSITE_NAVIGATION = [
    NavigationItem(_('Main page'), 'index'),
    NavigationItem(_('Statistics'), 'players:stats'),
    NavigationItem(_('Create account'), 'accounts:create'),
    NavigationItem(_('Profile'), 'accounts:profile'),
    NavigationItem(_('Administration'), 'admin:index'),
]

def navigation_context_processor(request):
    # Add navigation items to context
    return {'navigation': RPGSITE_NAVIGATION}
