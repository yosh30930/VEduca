from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

urlpatterns = patterns("",
    url(r'^logos/$', auth_views.login, {'template_name': 'sesion/inicio_sesion.html'}, name='sesion'),
)
