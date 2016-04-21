from .models import Usuario
from django.http import Http404

from drf_multiple_model.views import MultipleModelAPIView
from rest_framework import status, generics
from rest_framework.response import Response

from .serializersDRF import ResponsableSerializer
# from .serializersDRF import ParticipanteSerializer
from apps.actividades.models import Encuentro
# from apps.actividades.models import Participante


class ResponsableListView(generics.ListCreateAPIView):
    """
    Regresa una lista de todos los **usuarios** (GET)
    Agrega un nuevo foro (POST)
    Actualiza todos los usuarios (PUT)
    Elimina todos los usuarios en el sistema (DELETE)
    """
    model = Usuario
    serializer_class = ResponsableSerializer
    queryset = Usuario.objects.all()

    def post(self, request, format=None):
        data = dict()
        serializer = ResponsableSerializer(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""

class ParticipanteListView(MultipleModelAPIView):

    Regresa una lista de los participantes, si se epecifica
    el id de un encuentro se regresan 2 listas, los que son locales al encuentro
    con ese id y los que son globales.


    def get_queryList(self):
        participantes = Participante.objects.order_by('nombre')
        encuentro_id = self.request.query_params.get('encuentro_id', None)
        if encuentro_id is None:
            queryList = [(participantes, ParticipanteSerializer)]
        else:
            try:
                encuentro = Encuentro.objects.get(id=encuentro_id)
                queryList = (
                    (participantes.filter(encuentro=encuentro),
                        ParticipanteSerializer, "locales"),
                    (participantes.filter(encuentro=None),
                        ParticipanteSerializer, "globales"),
                )

            except Encuentro.ObjectDoesNotExist:
                raise Http404
        return queryList
"""