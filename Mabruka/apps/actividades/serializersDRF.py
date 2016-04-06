from django.apps import apps

from rest_framework import serializers

from .models import Encuentro, Foro, Seminario, Panel, Espacio


class EspacioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espacio
        fields = ("nombre", "id")


class ActividadSerializer(serializers.ModelSerializer):
    modelo = None
    tipo = serializers.SerializerMethodField('tipo_modelo')
    tipo_padre = serializers.SerializerMethodField('tipo_padre_fun')
    id_padre = serializers.SerializerMethodField('id_padre_fun')

    def create(self, validated_data):
        print('validate', validated_data)
        # Se remueven los responsables de los datos
        responsables = []
        if 'responsables' in validated_data:
            responsables = validated_data['responsables']
            del(validated_data['responsables'])
        # Se remueven datatos del padre
        padre = None
        tipo_padre = None
        id_padre = None
        print("validated_data", validated_data)
        if "tipo_padre" in validated_data:
            tipo_padre = validated_data["tipo_padre"]
            del(validated_data["tipo_padre"])
        if "id_padre" in validated_data:
            id_padre = validated_data["id_padre"]
            del(validated_data["id_padre"])
        print("tipo_padre", tipo_padre)
        print("id_padre", id_padre)
        if (tipo_padre is not None) and (id_padre is not None):
            try:
                Modelo_padre = apps.get_model(
                    app_label='actividades', model_name=tipo_padre)
                padre = Modelo_padre.objects.get(id=id_padre)
            except Exception as e:
                raise e
        actividad = self.modelo(**validated_data)
        if padre:
            actividad.save(padre=padre)
        else:
            actividad.save()
        # Asignación de responsables
        if responsables:
            actividad.responsables.add(*responsables)
        return actividad

    def tipo_modelo(self, obj):
        return obj.tipo

    def tipo_padre_fun(self, obj):
        nodo = obj.nodos.first()
        ancestros = nodo.get_ancestors()
        if ancestros:
            padre = ancestros.first().elemento
            return padre.tipo
        else:
            return None

    def id_padre_fun(self, obj):
        nodo = obj.nodos.first()
        ancestros = nodo.get_ancestors()
        if ancestros:
            padre = ancestros.first().elemento
            return padre.id
        else:
            return None


class EncuentroSerializer(ActividadSerializer):
    """
    Serializa todos los Encuentros
    """
    tipo_str = "encuentro"
    modelo = Encuentro

    class Meta:
        model = Encuentro
        fields = ("nombre", "id",
                  "fecha_inicio", "fecha_fin", "tipo", "responsables",
                  "tipo_padre", "id_padre")


class ForoSerializer(ActividadSerializer):
    """
    Serializa todos los Foros
    """
    tipo_str = "foro"
    modelo = Foro

    class Meta:
        model = Foro
        fields = ("nombre", "id", "tipo", "tipo_padre", "id_padre",
                  "descripcion", "nombre_corto", "responsables")


class SeminarioSerializer(ActividadSerializer):
    """
    Serializa todos los Seminarios
    """
    tipo_str = "seminario"
    modelo = Seminario

    class Meta:
        model = Seminario
        fields = ("nombre", "id", "tipo", "tipo_padre", "id_padre",
                  "responsables")


class PanelSerializer(ActividadSerializer):
    """
    Serializa todos los Paneles
    """
    tipo_str = "panel"
    modelo = Panel

    class Meta:
        model = Panel
        fields = ("nombre", "id", "tipo", "fecha_inicio", "fecha_fin",
                  "espacio", "tipo_padre", "id_padre")
