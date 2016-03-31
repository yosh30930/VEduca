from rest_framework import serializers
from .models import Evento, Foro, Seminario, Panel


class EncuentroSerializer(serializers.ModelSerializer):
    tipo = serializers.SerializerMethodField('tipo_str')
    """
    Serializing all the Authors
    """

    def tipo_str(self, foo):
        return "encuentro"

    def create(self, validated_data):
        modelo = Evento
        return modelo.objects.crear(**validated_data)

    class Meta:
        model = Evento
        fields = ("nombre", "id", "tipo")


class ForoSerializer(serializers.ModelSerializer):
    tipo = serializers.SerializerMethodField('tipo_str')
    """
    Serializing all the Authors
    """

    def tipo_str(self, foo):
        return "foro"

    def create(self, validated_data):
        modelo = Foro
        return modelo.objects.crear(**validated_data)

    class Meta:
        model = Foro
        fields = ("nombre", "id", "tipo")


class SeminarioSerializer(serializers.ModelSerializer):
    """
    Serializing all the Authors
    """
    tipo = serializers.SerializerMethodField('tipo_str')

    def tipo_str(self, foo):
        return "seminario"

    def create(self, validated_data):
        modelo = Seminario
        return modelo.objects.crear(**validated_data)

    class Meta:
        model = Seminario
        fields = ("nombre", "id", "tipo")


class PanelSerializer(serializers.ModelSerializer):
    """
    Serializing all the Authors
    """
    tipo = serializers.SerializerMethodField('tipo_str')

    def tipo_str(self, foo):
        return "panel"

    def create(self, validated_data):
        modelo = Panel
        return modelo.objects.crear(**validated_data)

    class Meta:
        model = Panel
        fields = ("nombre", "id", "tipo")
