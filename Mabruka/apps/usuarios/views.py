from django.contrib.auth.models import User

from rest_framework import status, generics
from rest_framework.response import Response

from .serializersDRF import ResponsableSerializer
# Create your views here.


class ResponsableListView(generics.ListCreateAPIView):
    """
    Regresa una lista de todos los **usuarios** (GET)
    Agrega un nuevo foro (POST)
    Actualiza todos los usuarios (PUT)
    Elimina todos los usuarios en el sistema (DELETE)
    """
    model = User
    serializer_class = ResponsableSerializer
    queryset = User.objects.all()

    def post(self, request, format=None):
        data = dict()
        serializer = ResponsableSerializer(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
