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
        fields = ('id', 'nombres', 'apellido_paterno', 'apellido_materno',
                  'correo', 'correo_secundario', 'pais')


"""
class ParticipanteSerializer(serializers.ModelSerializer):
    pais = SerializableCountryField(allow_blank=True)

    class Meta:
        model = Participante
        fields = ('id', 'nombre', 'pais')
"""
