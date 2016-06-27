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
                  'correo', 'correo_secundario', 'pais')

    def create(self, *args, **kwargs):
        obj = None
        try:
            with transaction.atomic():
                print("Correoooooooooo", obj.correo)
                Usuario.objects.create_user(correo=obj.correo)
        except IntegrityError as e:
            raise e
        return obj


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
