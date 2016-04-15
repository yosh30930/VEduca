from django.conf.urls import url
from .views import ResponsableListView, ParticipanteListView

urlpatterns = [
    url(r'^responsables/$', ResponsableListView.as_view(), name='responsable-list'),
    url(r'^participantes/$', ParticipanteListView.as_view(), name='participante-list'),
]
