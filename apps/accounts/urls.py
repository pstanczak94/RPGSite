from django.conf.urls import url

app_name = 'accounts'

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^create/$', views.RegisterView.as_view(), name='create'),
    url(r'^password/$', views.PasswordChangeView.as_view(), name='password'),
    url(r'^email/activation/$', views.EmailVerificationView.as_view(), name='email-activation'),
]
