from rest_framework import serializers
from .models import Encuentro, Foro, Seminario, Panel


class EncuentroSerializer(serializers.ModelSerializer):
    """
    Serializa todos los Encuentros
    """
    tipo = serializers.SerializerMethodField('tipo_str')

    def tipo_str(self, foo):
        return "encuentro"

    def create(self, validated_data):
        modelo = Encuentro
        return modelo.objects.crear(**validated_data)

    class Meta:
        model = Encuentro
        fields = ("nombre", "id", "tipo")


class ForoSerializer(serializers.ModelSerializer):
    """
    Serializa todos los Foros
    """
    tipo = serializers.SerializerMethodField('tipo_str')

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
    Serializa todos los Seminarios
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
    Serializa todos los Paneles
    """
    tipo = serializers.SerializerMethodField('tipo_str')

    def tipo_str(self, foo):
        return "panel"

    def create(self, validated_data):
        modelo = Panel
        return modelo.objects.crear(**validated_data)

    class Meta:
        model = Panel
        fields = ("nombre", "id", "tipo", "fecha_inicio", "fecha_fin")
