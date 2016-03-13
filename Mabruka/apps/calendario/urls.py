from django.conf.urls import url
from .views import (
    CalendarioHome,
    BuscarActividades,
    ActualizarEvento,
    EncuentroListView,
    EncuentroDetailView,
    ForoListView,
    SeminariosView,
    PanelesView,
    HijosListView,
)

urlpatterns = [
    url(r'^calendario/$', CalendarioHome.as_view()),
    url(r'^gestion_evento/(?P<id>\d+)/$', CalendarioHome.as_view()),
    url(r'^buscar-actividades/$', BuscarActividades, name='buscar'),
    url(r'^actualizar-evento/$', ActualizarEvento, name='actualizar'),
    url(r'^encuentros/$', EncuentroListView.as_view(), name='encuentro-list'),
    url(r'^encuentros/(?P<id>\d+)/$', EncuentroDetailView.as_view(), name='encuentro-list'),
    url(r'^encuentros/crear/$', EncuentroListView.as_view(), name='encuentro-list'),
    url(r'^foros/$', ForoListView.as_view()),
    url(r'^foros/crear/$', ForoListView.as_view()),
    url(r'^seminarios/$', SeminariosView.as_view()),
    url(r'^seminarios/crear/$', SeminariosView.as_view()),
    url(r'^paneles/$', PanelesView.as_view()),
    url(r'^paneles/crear/$', PanelesView.as_view()),
    url(r'^hijos/(?P<tipo_padre>\w+)/(?P<id_padre>\d+)/$', HijosListView.as_view()),
]
