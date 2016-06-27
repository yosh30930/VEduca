from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from .views import InicioSesionView, UsuarioResetView

urlpatterns = [
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}),
    url(r'^$', InicioSesionView.as_view(), name='inicio_sesion'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^restaurar_contraseña_hecho/$', auth_views.password_reset_done,
        {'template_name': 'sesion/restaura_contrasena_hecho.html'},
        name="restaurar_contraseña_hecho"),
    url(r'^restaurar_contraseña/$', UsuarioResetView.as_view(),
        name="restaura_contraseña"),
    url(r'^restaurar_contraseña_confirmacion/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name': 'sesion/restaura_contrasena_confirmacion.html',
        'post_reset_redirect': '/restaurar_contraseña_hecho/'}),
    url(r'^restaurar_contraseña_hecho/$', auth_views.password_reset_complete,
        {'template_name': 'sesion/restaura_contrasena_hecho.html'},
        name="restaura_contraseña_hecho"),
]
