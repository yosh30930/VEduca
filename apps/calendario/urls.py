from django.conf.urls import url
from .views import CalendarioHome, ActualizarActividadView
"""from .views import (
    CalendarioHome,
    BuscarActividades,
    ActualizarEvento
)

urlpatterns = [
    url(r'^calendario/$', CalendarioHome.as_view()),
    url(r'^gestion_evento/(?P<id>\d+)/$', CalendarioHome.as_view()),
    url(r'^buscar-actividades/$', BuscarActividades, name='buscar'),
    url(r'^actualizar-evento/$', ActualizarEvento, name='actualizar'),
]
"""
urlpatterns = [
    url(r'^gestion_encuentro/(?P<id>\d+)/$', CalendarioHome.as_view()),
    url(r'^actualizar_actividad/(?P<tipo>\w+)/(?P<id>\d+)/$',
        ActualizarActividadView.as_view()),
]
