from django.conf.urls import url
from .views import Inicio

urlpatterns = [
    url(r'^actividades/$', Inicio.as_view()),
]
