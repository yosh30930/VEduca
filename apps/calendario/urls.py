from django.conf.urls import url
from .views import CalendarioHome, ActualizarActividadView

urlpatterns = [
    url(r'^gestion_encuentro/(?P<id>\d+)/$', CalendarioHome.as_view()),
    url(r'^actualizar_actividad/(?P<tipo>\w+)/(?P<id>\d+)/$',
        ActualizarActividadView.as_view()),
]
