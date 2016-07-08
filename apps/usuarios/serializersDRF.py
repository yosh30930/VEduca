from rest_framework import serializers
from django.db import transaction, IntegrityError

# from apps.actividades.models import Participante
from .models import Usuario, Persona, Institucion


class ResponsableSerializer(serializers.ModelSerializer):
    """
    Se encarga de hacer la conversión entre objetos de tipo Responsable en
    formato Python a objetos en formato json y visceversa.
    """
    class Meta:
        model = Persona
        fields = ('id', 'nombres', 'apellido_paterno', 'apellido_materno',
                  'correo', 'pais')

    def create(self, validated_data):
        persona = Persona (
                    nombres=validated_data['nombres'],
                    apellido_paterno=validated_data['apellido_paterno'],
                    apellido_materno=validated_data['apellido_materno'],
                    correo=validated_data['correo'])
        persona.save()
        return persona


class PersonaSerializer(serializers.ModelSerializer):
    """
    Se encarga de hacer la conversión entre objetos de tipo Persona en
    formato Python a objetos en formato json y visceversa.
    """
    class Meta:
        model = Persona
        fields = ('id', 'nombres', 'apellido_paterno', 'apellido_materno',
                  'correo', 'correo_secundario', 'pais')


class InstitucionSerializer(serializers.ModelSerializer):
    """
    Se encarga de hacer la conversión entre objetos de tipo Institución en
    formato Python a objetos en formato json y visceversa.
    """
    class Meta:
        model = Institucion
        fields = ('id', 'nombre', 'nombre_corto', 'pais')

"""
class ParticipanteSerializer(serializers.ModelSerializer):
    pais = SerializableCountryField(allow_blank=True)

    class Meta:
        model = Participante
        fields = ('id', 'nombre', 'pais')
"""
