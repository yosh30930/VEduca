from swampdragon.serializers.model_serializer import ModelSerializer as swampModelSerializer


class EncuentroSwampSerializer(swampModelSerializer):
    class Meta:
        model = 'calendario.Evento'
        publis_fields = ('nombre')


class ForoSwampSerializer(swampModelSerializer):
    class Meta:
        model = 'calendario.Foro'
        publis_fields = ('nombre')


class PanelSwampSerializer(swampModelSerializer):
    class Meta:
        model = 'calendario.Panel'
        publis_fields = ('nombre')


class SeminarioSwampSerializer(swampModelSerializer):
    class Meta:
        model = 'calendario.Seminario'
        publis_fields = ('nombre')
