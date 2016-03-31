from django.conf.urls import url
from .views import (
    InicioEncuentros,
    ModificacionEncuentroView,
    ModificacionForoView,
    ModificacionSeminarioView,
    ModificacionPanelView,
    EncuentroListView,
    EncuentroDetailView,
    ForoListView,
    ForoDetailView,
    SeminarioListView,
    SeminarioDetailView,
    PanelListView,
    PanelDetailView,
    HijosListView,)

urlpatterns = [
    url(r'^inicio/$', InicioEncuentros.as_view()),
    url(
        r'^modificacion_encuentro/(?P<id>\d+)/$',
        ModificacionEncuentroView.as_view()),
    url(
        r'^modificacion_foro/(?P<id>\d+)/$',
        ModificacionForoView.as_view()),
    url(
        r'^modificacion_seminario/(?P<id>\d+)/$',
        ModificacionSeminarioView.as_view()),
    url(
        r'^modificacion_panel/(?P<id>\d+)/$',
        ModificacionPanelView.as_view()),
    url(r'^encuentros/$', EncuentroListView.as_view(), name='encuentro-list'),
    url(
        r'^encuentros/(?P<id>\d+)/$',
        EncuentroDetailView.as_view(), name='encuentro-detail'),
    url(r'^foros/$', ForoListView.as_view(), name='foro-list'),
    url(r'^foros/(?P<id>\d+)/$', ForoDetailView.as_view(), name='foro-detail'),
    url(r'^seminarios/$', SeminarioListView.as_view(), name='seminario-list'),
    url(
        r'^seminarios/(?P<id>\d+)/$',
        SeminarioDetailView.as_view(), name='seminario-detail'),
    url(r'^paneles/$', PanelListView.as_view(), name='panel-list'),
    url(
        r'^paneles/(?P<id>\d+)/$',
        PanelDetailView.as_view(), name='panel-detail'),
    url(
        r'^hijos/(?P<tipo_padre>\w+)/(?P<id_padre>\d+)/$',
        HijosListView.as_view(), name='hijos-list'),
]
