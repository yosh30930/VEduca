from django_countries import Countries
from rest_framework import serializers

# from apps.actividades.models import Participante
from .models import Usuario, Persona


class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ('id', 'nombres')


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ('id', 'nombres', 'apellidos', 'correo', 'correo_secundario',
                  'es_coordinador', 'pais')


"""
class ParticipanteSerializer(serializers.ModelSerializer):
    pais = SerializableCountryField(allow_blank=True)

    class Meta:
        model = Participante
        fields = ('id', 'nombre', 'pais')
"""
