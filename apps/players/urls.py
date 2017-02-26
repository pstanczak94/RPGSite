from django.conf.urls import url

app_name = 'players'

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create/$', views.CreateView.as_view(), name='create'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.DeleteView.as_view(), name='delete'),
]
