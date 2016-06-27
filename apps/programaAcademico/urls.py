from django.conf.urls import url
from .views import ProgramaAcademico

urlpatterns = [
    url(r'^programa_academico/(?P<id>\d+)/$', ProgramaAcademico.as_view())]
