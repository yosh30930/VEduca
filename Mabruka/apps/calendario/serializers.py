from rest_framework import serializers
from .models import Evento, Foro, Seminario, Panel


class EncuentroSerializer(serializers.ModelSerializer):
    tipo = serializers.SerializerMethodField('is_named_bar')
    """
    Serializing all the Authors
    """
    def is_named_bar(self, foo):
        return "encuentro"

    def create(self, validated_data):
        return Evento.objects.crear(**validated_data)

    class Meta:
        model = Evento
        fields = ("nombre", "id", "tipo")

class ForoSerializer(serializers.ModelSerializer):
    tipo = serializers.SerializerMethodField('is_named_bar')
    """
    Serializing all the Authors
    """
    def is_named_bar(self, foo):
        return "foro"

    def create(self, validated_data):
        return Foro.objects.crear(**validated_data)

    class Meta:
        model = Foro
        fields = ("nombre", "id", "tipo")

class SeminarioSerializer(serializers.ModelSerializer):
    """
    Serializing all the Authors
    """
    tipo = serializers.SerializerMethodField('is_named_bar')
    def is_named_bar(self, foo):
        return "seminario"

    def create(self, validated_data):
        return Seminario.objects.crear(**validated_data)

    class Meta:
        model = Seminario
        fields = ("nombre", "id", "tipo")

class PanelSerializer(serializers.ModelSerializer):
    """
    Serializing all the Authors
    """
    tipo = serializers.SerializerMethodField('is_named_bar')
    def is_named_bar(self, foo):
        return "panel"

    def create(self, validated_data):
        return Panel.objects.crear(**validated_data)

    class Meta:
        model = Panel
        fields = ("nombre", "id", "tipo")

#class NombreEncuentroField(serializers.Field):
