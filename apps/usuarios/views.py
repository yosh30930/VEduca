from django.http import Http404

from drf_multiple_model.views import MultipleModelAPIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializersDRF import ResponsableSerializer, PersonaSerializer
from .serializersDRF import InstitucionSerializer
# from .serializersDRF import ParticipanteSerializer
from .models import Usuario, Persona, Institucion
# from apps.actividades.models import Participante


class ResponsableListView(generics.ListCreateAPIView):
    """
    Regresa una lista de todos los **usuarios** (GET)
    Agrega un nuevo foro (POST)
    """
    model = Persona
    serializer_class = PersonaSerializer
    queryset = Persona.objects.all()

    def post(self, request, format=None):
        data = request.data
        serializer = ResponsableSerializer(
            data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParticipanteListView(MultipleModelAPIView):
    """Regresa una lista de los participantes, si se epecifica
    el id de un encuentro se regresan 2 listas, los que son locales al
    encuentro con ese id y los que son globales."""

    def get_queryList(self):
        participantes = Persona.objects.order_by('nombres')
        # encuentro_id = self.request.query_params.get('encuentro_id', None)
        queryList = [(participantes, PersonaSerializer)]
        return queryList


class PersonaListView(generics.ListCreateAPIView):
    """
    Regresa una lista de todos los **foros** (GET)
    Agrega un nuevo foro (POST)
    """
    model = Persona
    serializer_class = PersonaSerializer
    queryset = Persona.objects.all().order_by('nombres')

    def post(self, request, format=None):
        data = request.data
        serializer = PersonaSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonaDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Regresa un persona (GET)
    Actualiza un persona (PUT)
    Elimina un persona (DELETE)
    """

    def get_object(self, id):
        try:
            return Persona.objects.get(pk=id)
        except Persona.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        persona = self.get_object(id)
        serializer = PersonaSerializer(
            persona, context={'request': request})
        return Response(serializer.data)

    def put(self, request, id, format=None):
        persona = self.get_object(id)
        serializer = PersonaSerializer(
            persona, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        persona = self.get_object(id)
        persona.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InstitucionListView(generics.ListCreateAPIView):
    """
    Regresa una lista de todos los **foros** (GET)
    Agrega un nuevo foro (POST)
    """
    model = Institucion
    serializer_class = InstitucionSerializer
    queryset = Institucion.objects.all().order_by('nombre')
