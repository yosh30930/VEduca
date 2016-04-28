from django.conf.urls import url
from .views import PersonaDetailView, PersonaListView, ResponsableListView
# from .views import ParticipanteListView

urlpatterns = [
    url(r'^responsables/$', ResponsableListView.as_view(),
        name='responsable-list'),
    url(r'^personas/$', PersonaListView.as_view(), name='personas-list'),
    url(r'^personas/(?P<id>\d+)/$', PersonaDetailView.as_view(),
        name='personas-detail'),
    # url(r'^participantes/$', ParticipanteListView.as_view(), name='participante-list'),
]
