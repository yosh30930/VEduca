from django.conf.urls import url
from .views import (
    EspacioListView,
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
    HijosListView,
    AncestrosListView,)

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
    url(r'^espacios/(?P<encuentro_id>\d+)/$', EspacioListView.as_view(),
        name='espacio-list'),
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
    url(
        r'^ancestros/(?P<tipo_actividad>\w+)/(?P<id_actividad>\d+)/$',
        AncestrosListView.as_view(), name='ancestros-list'),
]
