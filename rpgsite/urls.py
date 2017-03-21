"""rpgsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^accounts/', include('apps.accounts.urls')),
    url(r'^players/', include('apps.players.urls')),
    url(r'^guilds/', include('apps.guilds.urls')),
    url(r'^administration/', admin.site.urls),
    url(r'^emoji/', include('emoji.urls')),
    url(r'^favicon\.ico$', views.FaviconView.as_view()),
    url(r'^robots\.txt$', views.RobotsView.as_view()),
]
