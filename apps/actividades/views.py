import copy

# from django.contrib.auth.models import User
import apps
from django.http import Http404
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from braces.views import LoginRequiredMixin, UserPassesTestMixin
from drf_multiple_model.views import MultipleModelAPIView
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializersDRF import (
    EncuentroSerializer, ForoSerializer, SeminarioSerializer,
    PanelSerializer, EspacioSerializer, ActividadSerializer)
from .models import (Encuentro, Foro, Seminario, Panel, Espacio,
                     modelosActividades, Sede)
from apps.usuarios.models import SecretarioGeneral

modelo_dict = {
    'encuentro': Encuentro, 'foro': Foro, 'seminario': Seminario,
    'panel': Panel}


def get_model(nombre_str):
    Modelo = apps.get_model(
        app_label='actividades', model_name=nombre_str)
    return Modelo


class ActividadListView(generics.ListCreateAPIView):
    """
    Regresa una lista de todos los **encuentros** (GET)

    Agrega un nuevo encuentro (POST)

    Actualiza todos los encuentros (PUT)

    Elimina todos los encuentros en el sistema (DELETE)
    """
    serializer_class = ActividadSerializer

    def post(self, request, format=None):
        serializer = ActividadSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
#           #publish_data(channel='notification', data=data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        queryset = Actividad.objects.none()
        if not user.is_authenticated():
            queryset = Actividad.objects.all()
        elif tiene_permiso_absoluto(user):
            queryset = Actividad.objects.all()
        else:
            encuentros_id = set()
            for Modelo in modelosActividades:
                query_results = []
                try:
                    query_result = Modelo.objects.filter(responsables=user)
                    query_results.append(query_result)
                except Modelo.FieldDoesNotExist:
                    continue
                for query_result in query_results:
                    for actividad in query_result:
                        nodo = actividad.nodos.first()
                        ancestros = nodo.get_ancestors(include_self=True)
                        ancestro_raiz = ancestros.first()
                        actividad_raiz = ancestro_raiz.elemento
                        if type(actividad_raiz) == Actividad:
                            encuentros_id.add(actividad_raiz.pk)
                        else:
                            continue
                        # encuentros_id.add()
            queryset = Actividad.objects.filter(pk__in=encuentros_id)
        # return Purchase.objects.filter(purchaser=user)
        return queryset.order_by('-fecha_creacion')


class ActividadDetailView(APIView):
    """
    Regresa un encuentro (GET)
    Actualiza un encuentro (PUT)
    Elimina un encuentro (DELETE)
    """

    def get_object(self, id):
        try:
            return Actividad.objects.get(pk=id)
        except Actividad.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        encuentro = self.get_object(id)
        serializer = ActividadSerializer(
            encuentro, context={'request': request})
        return Response(serializer.data)

    def put(self, request, id, format=None):
        encuentro = self.get_object(id)
        serializer = ActividadSerializer(
            encuentro, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        encuentro = self.get_object(id)
        encuentro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EspacioListView(generics.ListCreateAPIView):
    """
    Regresa una lista de todos los **espacios** (GET)

    Agrega un nuevo espacio (POST)

    Actualiza todos los espacios (PUT)

    Elimina todos los espacios en el sistema (DELETE)
    """
    model = Espacio
    serializer_class = EspacioSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        id = self.kwargs['encuentro_id']
        sedes = Sede.objects.filter(encuentro=id)
        sedes_id = [sede.pk for sede in sedes]
        espacios = Espacio.objects.filter(sede__in=sedes_id)
        return espacios
"""
    def post(self, request, format=None):
        serializer = EspacioSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
#           #publish_data(channel='notification', data=data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
"""


class HijosListView(MultipleModelAPIView):
    """
    Regresa una lista de todos los hijos de una actividad
    dado su id y tipo.
    """

    def get_queryList(self):
        queryList = []
        tipo_padre = self.kwargs['tipo_padre']
        id_padre = self.kwargs['id_padre']
        if tipo_padre not in modelo_dict:
            raise Http404
        Modelo = modelo_dict[tipo_padre]
        padre = Modelo.objects.get(id=id_padre)
        nodo = padre.nodos.all().first()
        nodos_hijos = nodo.get_children()
        nodos_hijos_permitidos = []
        for nodo_hijo in nodos_hijos:
            if nodo_hijo.elemento.puede_ver_nodo(self.request.user):
                nodos_hijos_permitidos.append(nodo_hijo)
        conjunto_hijos = {
            Foro: ([], ForoSerializer, 'foros'),
            Encuentro: ([], EncuentroSerializer, 'encuentros'),
            Panel: ([], PanelSerializer, 'paneles'),
            Seminario: ([], SeminarioSerializer, 'seminarios'),
        }
        posibles_hijos = {
            Encuentro: [Foro], Foro: [Seminario], Seminario: [Panel],
            Panel: [],
        }
        for nodo_hijo in nodos_hijos_permitidos:
            hijo = nodo_hijo.elemento
            conjunto_hijos[type(hijo)][0].append(hijo)

        for llave, valor in conjunto_hijos.items():
            if (llave in posibles_hijos[Modelo]) or len(valor[0]) > 0:
                queryList.append(valor)
        return queryList


class AncestrosListView(MultipleModelAPIView):
    """
    Regresa una lista de forma descendente(abuelo, padre, hijo) con todos los
    ancestros de la actividad incluida la actividad misma.
    """
    flat = True

    def get_queryList(self):
        queryList = []
        tipo_actividad = self.kwargs['tipo_actividad']
        id_actividad = self.kwargs['id_actividad']
        if tipo_actividad not in modelo_dict:
            raise Http404
        # Se obtiene la actividad de la que se buscarán sus ancestros
        Modelo = modelo_dict[tipo_actividad]
        actividad = Modelo.objects.get(id=id_actividad)
        nodo_actividad = actividad.nodos.first()
        ancestros = nodo_actividad.get_ancestors(include_self=True)
        # Se itera sobre cada ancestro
        conjunto_hijos = {
            Foro: ([], ForoSerializer),
            Encuentro: ([], EncuentroSerializer),
            Panel: ([], PanelSerializer),
            Seminario: ([], SeminarioSerializer),
        }
        for ancestro in ancestros:
            actividad_tmp = ancestro.elemento
            serializer = conjunto_hijos[type(actividad_tmp)][1]
            queryAncestro = (
                type(actividad_tmp).objects.filter(pk=actividad_tmp.pk),
                serializer)
            queryList.append(queryAncestro)
        return queryList


class EncuentroListView(generics.ListCreateAPIView):
    """
    Regresa una lista de todos los **encuentros** (GET)

    Agrega un nuevo encuentro (POST)

    Actualiza todos los encuentros (PUT)

    Elimina todos los encuentros en el sistema (DELETE)
    """
    model = Encuentro
    serializer_class = EncuentroSerializer

    def post(self, request, format=None):
        serializer_kwargs = dict()
        if "sedes" in request.data:
            serializer_kwargs["sedes"] = request.data["sedes"]
        serializer = EncuentroSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            print("Post", serializer_kwargs)
            serializer.save(**serializer_kwargs)
#           #publish_data(channel='notification', data=data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        queryset = Encuentro.objects.none()
        if not user.is_authenticated():
            queryset = Encuentro.objects.all()
        elif tiene_permiso_absoluto(user):
            queryset = Encuentro.objects.all()
        else:
            encuentros_id = set()
            for Modelo in modelosActividades:
                query_results = []
                try:
                    query_result = Modelo.objects.filter(responsables=user)
                    query_results.append(query_result)
                except Modelo.FieldDoesNotExist:
                    continue
                for query_result in query_results:
                    for actividad in query_result:
                        nodo = actividad.nodos.first()
                        ancestros = nodo.get_ancestors(include_self=True)
                        ancestro_raiz = ancestros.first()
                        actividad_raiz = ancestro_raiz.elemento
                        if type(actividad_raiz) == Encuentro:
                            encuentros_id.add(actividad_raiz.pk)
                        else:
                            continue
                        # encuentros_id.add()
            queryset = Encuentro.objects.filter(pk__in=encuentros_id)
        # return Purchase.objects.filter(purchaser=user)
        return queryset.order_by('-fecha_creacion')


class EncuentroDetailView(APIView):
    """
    Regresa un encuentro (GET)
    Actualiza un encuentro (PUT)
    Elimina un encuentro (DELETE)
    """

    def get_object(self, id):
        try:
            return Encuentro.objects.get(pk=id)
        except Encuentro.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        encuentro = self.get_object(id)
        serializer = EncuentroSerializer(
            encuentro, context={'request': request})
        return Response(serializer.data)

    def put(self, request, id, format=None):
        encuentro = self.get_object(id)
        serializer_kwargs = dict()
        if "sedes" in request.data:
            serializer_kwargs["sedes"] = request.data["sedes"]
        serializer = EncuentroSerializer(
            encuentro, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(**serializer_kwargs)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        encuentro = self.get_object(id)
        encuentro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ForoListView(generics.ListCreateAPIView):
    """
    Regresa una lista de todos los **foros** (GET)
    Agrega un nuevo foro (POST)
    Actualiza todos los foros (PUT)
    Elimina todos los foros en el sistema (DELETE)
    """
    model = Foro
    serializer_class = ForoSerializer
    queryset = Foro.objects.all().order_by('-fecha_creacion')

    def post(self, request, format=None):
        data = request.data
        serializer = ForoSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            if ("tipo_padre" in data) and ("id_padre" in data):
                tipo_padre = data["tipo_padre"]
                id_padre = data["id_padre"]
                serializer.save(tipo_padre=tipo_padre, id_padre=id_padre)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForoDetailView(APIView):
    """
    Regresa un foro (GET)
    Actualiza un foro (PUT)
    Elimina un foro (DELETE)
    """

    def get_object(self, id):
        try:
            return Foro.objects.get(pk=id)
        except Foro.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        foro = self.get_object(id)
        serializer = ForoSerializer(foro, context={'request': request})
        return Response(serializer.data)

    def put(self, request, id, format=None):
        foro = self.get_object(id)
        serializer = ForoSerializer(
            foro, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        foro = self.get_object(id)
        foro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SeminarioListView(generics.ListCreateAPIView):
    """
    Regresa una lista de todos los **seminarios** (GET)
    Agrega un nuevo seminario (POST)
    Actualiza todos los seminarios (PUT)
    Elimina todos los seminarios en el sistema (DELETE)
    """
    model = Seminario
    serializer_class = SeminarioSerializer
    queryset = Seminario.objects.all().order_by('-fecha_creacion')

    def post(self, request, format=None):
        data = request.data
        serializer = SeminarioSerializer(
            data=data, context={'request': request})
        if serializer.is_valid():
            if ("tipo_padre" in data) and ("id_padre" in data):
                tipo_padre = data["tipo_padre"]
                id_padre = data["id_padre"]
                serializer.save(tipo_padre=tipo_padre, id_padre=id_padre)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SeminarioDetailView(APIView):
    """
    Regresa un seminario (GET)
    Actualiza un seminario (PUT)
    Elimina un seminario (DELETE)
    """

    def get_object(self, id):
        try:
            return Seminario.objects.get(pk=id)
        except Seminario.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        seminario = self.get_object(id)
        serializer = SeminarioSerializer(
            seminario, context={'request': request})
        return Response(serializer.data)

    def put(self, request, id, format=None):
        seminario = self.get_object(id)
        serializer = SeminarioSerializer(
            seminario, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        seminario = self.get_object(id)
        seminario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PanelListView(generics.ListCreateAPIView):
    """
    Regresa una lista de todos los **paneles** (GET)
    Agrega un nuevo panel (POST)
    Actualiza todos los paneles (PUT)
    Elimina todos los paneles en el sistema (DELETE)
    """
    model = Panel
    serializer_class = PanelSerializer
    queryset = Panel.objects.all().order_by('-fecha_creacion')

    def post(self, request, format=None):
        data = request.data
        serializer = PanelSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            if ("tipo_padre" in data) and ("id_padre" in data):
                tipo_padre = data["tipo_padre"]
                id_padre = data["id_padre"]
                serializer.save(tipo_padre=tipo_padre, id_padre=id_padre)
            else:
                serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PanelDetailView(APIView):
    """
    Regresa un panel (GET)
    Actualiza un panel (PUT)
    Elimina un panel (DELETE)
    """

    def get_object(self, id):
        try:
            return Panel.objects.get(pk=id)
        except Panel.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        panel = self.get_object(id)
        serializer = PanelSerializer(panel, context={'request': request})
        return Response(serializer.data)

    def put(self, request, id, format=None):
        panel = self.get_object(id)
        serializer = PanelSerializer(
            panel, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        panel = self.get_object(id)
        panel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Vistas con html
def tiene_permiso_absoluto(usuario, actividad=None):
    if not usuario.is_active:
        return False
    if (usuario.is_superuser or
            SecretarioGeneral.objects.filter(usuario=usuario)):
        return True
    if actividad is None:
        return False
    nodo_actividad = actividad.nodos.all().first()
    nodos = nodo_actividad.get_ancestors()
    for nodo in nodos:
        if usuario in nodo.elemento.responsables.all():
            return True
    return False


def tiene_permiso_restringido(usuario, actividad):
    return usuario in actividad.responsables.all()


class InicioEncuentros(LoginRequiredMixin, TemplateView):
    """
    Vista donde se muestran todos los encuentros sobre los que el usuario
    tiene privilegios
    """
    login_url = "/"
    template_name = "actividades/encuentros.html"

    def get_context_data(self, **kwargs):
        context = super(
            InicioEncuentros, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_superuser or SecretarioGeneral.objects.filter(usuario=user):
            context['es_secretario'] = True
        return context
