from django_countries import Countries
from rest_framework import serializers
from django.db import transaction, IntegrityError

# from apps.actividades.models import Participante
from .models import Usuario, Persona, Institucion


class ResponsableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ('id', 'nombres', 'apellido_paterno', 'apellido_materno',
                  'correo', 'correo_secundario', 'pais')

    def create(self, *args, **kwargs):
        obj = None
        try:
            with transaction.atomic():
                obj = super(ResponsableSerializer, self).create(
                    *args, **kwargs)
                print("Correoooooooooo", obj.correo)
                Usuario.objects.create_user(correo=obj.correo)
        except IntegrityError as e:
            raise e
        return obj


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ('id', 'nombres', 'apellido_paterno', 'apellido_materno',
                  'correo', 'correo_secundario', 'pais')


class InstitucionSerializer(serializers.ModelSerializer):
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
