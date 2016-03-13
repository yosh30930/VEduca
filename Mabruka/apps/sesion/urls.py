from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^logout/$', auth_views.logout, {'next_page': '/inicio_sesion/'}),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^inicio_sesion/$', auth_views.login,{'template_name': 'sesion/inicio_sesion.html'}, name='inicio_sesion'),
    url(r'^restaurar_contraseña_hecho/$', auth_views.password_reset_done, {'template_name': 'sesion/restaura_contrasena_hecho.html'}),
    url(r'^restaurar_contraseña/$', auth_views.password_reset,
        {'template_name': 'sesion/restaura_contrasena.html', 'post_reset_redirect': '/restaurar_contraseña_hecho/'}, name="restaura_contraseña"),



#    url(r'^user/password/reset$', auth_views.password_reset,
#        {'template_name': 'sesion/restaura_contrasena.html',
#            'post_reset_redirect': '/user/password/reset/done/'},
#        name="restaura_contraseña"),
    url(r'^restaurar_contraseña_confirmacion/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name':'sesion/restaura_contrasena_confirmacion.html', 'post_reset_redirect': '/restaurar_contraseña_hecho/'}),
    url(r'^restaurar_contraseña_hecho/$', auth_views.password_reset_complete, {'template_name':'sesion/restaura_contrasena_hecho.html'}),
]
