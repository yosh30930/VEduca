from django.conf.urls import url
#from .views import Inicio, CrearEvento, ObtenerHijos, ModificacionEventoView
from .views import ProgramaAcademico

urlpatterns = [
     url(r'^programa_academico/(?P<id>\d+)/$', ProgramaAcademico.as_view()),
#    url(r'^crear_evento/$', CrearEvento),
#    url(r'^obtener_hijos/$', ObtenerHijos),
#   url(r'^gestion_evento/(?P<id>\d+)/$', Inicio.as_view()),
#    url(r'^modificacion_evento/(?P<id>\d+)/$', ModificacionEventoView.as_view()),
]
