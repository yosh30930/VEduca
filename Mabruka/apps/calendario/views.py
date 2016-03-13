from django.apps import apps
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import TemplateView

from drf_multiple_model.views import MultipleModelAPIView
from rest_framework import status, generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import json

from .models import Evento, Foro, Seminario, Panel
from .models import Evento
from .serializers import EncuentroSerializer, ForoSerializer, SeminarioSerializer, PanelSerializer
# Create your views here.


@api_view(['GET', 'POST'])
def get_encuentros(request):
    """
    Regresa una lista de todos los encuentros.
    """
    if request.method == "GET":
        encuentros = Evento.objects.all()
        serializer = EncuentroSerializer(encuentros, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = EncuentroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HijosListView(MultipleModelAPIView):
    def get_queryList(self):
        queryList = []
        tipo_padre = self.kwargs['tipo_padre']
        id_padre = self.kwargs['id_padre']
        tipos_padres = {'encuentro': Evento, 'foro': Foro, 'seminario': Seminario, 'panel': Panel}
        if tipo_padre not in tipos_padres:
            raise Http404
        Modelo = tipos_padres[tipo_padre]
        print(tipo_padre, Modelo, id_padre)
        padre = Modelo.objects.get(id=id_padre)
        nodo = padre.nodos.all().first()
        nodos_hijos = nodo.get_children()
        conjunto_hijos = {
            Foro:([],ForoSerializer,'foros'),
            Evento:([],EncuentroSerializer,'encuentros'),
            Panel:([],PanelSerializer,'paneles'),
            Seminario:([],SeminarioSerializer,'seminarios'),
        }
        for nodo_hijo in nodos_hijos:
            hijo = nodo_hijo.elemento
            conjunto_hijos[type(hijo)][0].append(hijo)

        for llave, valor in conjunto_hijos.items():
            if len(valor[0]) > 0:
                queryList.append(valor)
        return queryList


class EncuentroListView(generics.ListCreateAPIView):
    """
    Regresa una lista de todos los **encuentros** (GET)

    Agrega un nuevo encuentro (POST)

    Actualiza todos los encuentros (PUT)

    Elimina todos los encuentros en el sistema (DELETE)
    """
    model = Evento
    serializer_class = EncuentroSerializer
    queryset = Evento.objects.all()
    def post(self, request, format=None):
        data = {'nombre':request.data.get('nombre')}
        serializer = EncuentroSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EncuentroDetailView(APIView):
    """
    Regresa un encuentro (GET)
    Actualiza un encuentro (PUT)
    Elimina un encuentro (DELETE)
    """
    def get_object(self, id):
        try:
            return Evento.objects.get(pk=id)
        except Evento.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        encuentro = self.get_object(id)
        serializer = EncuentroSerializer(encuentro)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        encuentro = self.get_object(id)
        serializer = EncuentroSerializer(encuentro, data=request.data)
        if serializer.is_valid():
            serializer.save()
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
    queryset = Foro.objects.all()
    def post(self, request, format=None):
        data = {'nombre':request.data.get('nombre'), 'padre_id':request.data.get('padre_id')}
        serializer = ForoSerializer(data=data)
        if serializer.is_valid():
            #serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForoDetailView(APIView):
    """
    Regresa un encuentro (GET)
    Actualiza un encuentro (PUT)
    Elimina un encuentro (DELETE)
    """
    def get_object(self, id):
        try:
            return Foro.objects.get(pk=id)
        except Foro.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        encuentro = self.get_object(id)
        serializer = ForoSerializer(encuentro)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        foro = self.get_object(id)
        serializer = ForoSerializer(foro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        foro = self.get_object(id)
        foro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ForosView(generics.ListAPIView):
    """
    Regresa una lista de todos los **foros** en el sistema.
    Opciones:
    + padre_id (Se obtendrán sólo los hijos que sean hijos de la actividad con este identificador)
    """
    serializer_class = ForoSerializer
    def get_queryset(self):
        padre_id = self.request.query_params.get('padre_id', None)
        queryset = []
        if padre_id is not None:
            queryset = Foro.objects.all()
        else:
            queryset = Foro.objects.all()
        return queryset


class SeminariosView(generics.ListAPIView):
    """
    Returns a list of all **active** accounts in the system.

    For more details on how accounts are activated please [see here][ref].

    [ref]: http://example.com/activating-accounts
    """
    serializer_class = SeminarioSerializer
    def get_queryset(self):
        padre_id = self.request.query_params.get('padre_id', None)
        queryset = []
        if padre_id is not None:
            queryset = Seminario.objects.all()
        else:
            queryset = Seminario.objects.all()
        return queryset


class PanelesView(generics.ListAPIView):
    serializer_class = PanelSerializer
    def get_queryset(self):
        padre_id = self.request.query_params.get('padre_id', None)
        queryset = []
        if padre_id is not None:
            queryset = Panel.objects.all()
        else:
            queryset = Panel.objects.all()
        return queryset

class CalendarioHome(TemplateView):
    template_name = "calendario/calendario_home.html"

    def get_context_data(self, **kwargs):
        context = super(CalendarioHome, self).get_context_data(**kwargs)
        ResetActividades()
        context['evento_id'] = kwargs['id']
#       context['latest_articles'] = Article.objects.all()[:5]
        return context


@transaction.atomic
def crea_actividad(Modelo, nombre, padre, *args, **kwargs):
    try:
        with transaction.atomic():
            actividad = Modelo.objects.crear(nombre=nombre, padre=padre, *args, **kwargs)
            return actividad
    except IntegrityError as e:
        raise e


def ResetActividades():
    modelos = [Evento, Foro, Seminario, Panel]
    for modelo in modelos:
        modelo.objects.all().delete()
    evento = Evento.objects.crear(nombre="Encuentro Internacional 2016 Costa Rica")
    foro1 = crea_actividad(
        Foro, "Educación Superior, Innovación e Internacionalización", evento,
        nombre_corto="Educación Superior")
    foro2 = crea_actividad(
        Foro, "Investigación, Desarrollo e Innovación (I+D+i) ", evento,
        nombre_corto="(I+D+i) ")
    seminario11 = crea_actividad(
        Seminario, "Programa Piloto Inclusión Digital, Estrategia Digital\
        Nacional, Gobierno de México", foro1)
    seminario21 = crea_actividad(
        Seminario, "Programa Piloto de Inclusión Digital, Estrategia Digital\
        Nacional, Gobierno de México", foro2)
    for idx in range(3):
        crea_actividad(Panel, "Panel 1." + str(idx), seminario11, calId="0")
    for idx in range(3):
        crea_actividad(Panel, "Panel 2." + str(idx), seminario21, calId="0")
    return


def BuscarActividades(request):
    if request.method != 'GET':
        raise Http404
    eventos = Evento.objects.all()
    if len(eventos) == 0:
        ResetActividades()
    if len(User.objects.all()) == 0:
        ResetUsuarios()
    try:
        evento = Evento.objects.get(pk=request.GET['id'])
    except Exception:
        return HttpResponseBadRequest()
    arbol = obten_hijos(evento)
    data = serializa(arbol)
    data_json = json.dumps(data)
    return HttpResponse(data_json, content_type='application/json')


def obten_hijos(padre):
    return {'padre': padre, 'hijos': []}


def serializa(arbol):
    padre = arbol['padre']
    hijos = arbol['hijos']
    padre_json = serializers.serialize('json', [padre])
    padre = json.loads(padre_json)[0]
    hijos = [serializa(hijo) for hijo in hijos]
    data = {'padre': padre, 'hijos': hijos}
    return data


def ActualizarEvento(request):
    pk = request.GET['pk']
    modelo = request.GET['modelo']
    nombre = request.GET['nombre']
    calId = request.GET['calId']
    allDay = request.GET['allDay']
    start = request.GET['start']
    end = request.GET['end']
    print('pk', type(pk), pk)
    print('nombre', type(nombre), nombre)
    print('calId', type(calId), calId)
    print('allDay', type(allDay), allDay)
    print('start', type(start), start)
    print('end', type(end), end)
    print('modelo', type(modelo), modelo)
    app_label, nombre_modelo = modelo.split(".")
    ModeloActividad = apps.get_model(app_label, nombre_modelo)
    actividad = ModeloActividad.objects.get(pk=int(pk))
    actividad.nombre = nombre
    actividad.calId = calId
    actividad.allDay = allDay == "true"
    actividad.start = start
    actividad.end = None if end == "null" else end
    actividad.save()
    #actividad = Actividad.objects.get(pk=int(pk))
#    print(actividad.nombre, actividad.calId, actividad.allDay, actividad.start, actividad.end)
    return HttpResponse('<h1>Page was found</h1>')


def ResetUsuarios():
    User.objects.all().delete()
    User.objects.create_user('foo', email='sainoba@gmail.com', password='bar', is_superuser=True, is_staff=True).save()
    User.objects.create_user('Fernando Gamboa', email='mabruka1@mailinator.com', password='bar', is_staff=True).save()
    User.objects.create_user('Elena García', email='mabruka2@mailinator.com', password='bar', is_staff=True).save()
    User.objects.create_user('Pedro Rocha', email='mabruka3@mailinator.com', password='bar', is_staff=True).save()
    User.objects.create_user('Juan Luis Valdés', email='mabruka4@mailinator.com', password='bar', is_staff=True).save()
    User.objects.create_user('Julieta Palma', email='mabruka5@mailinator.com', password='bar', is_staff=True).save()
    User.objects.create_user('Juan Manuel Valdés', email='mabruka6@mailinator.com', password='bar', is_staff=True).save()
    User.objects.create_user('Luis Andrés Ochoa', email='mabruka7@mailinator.com', password='bar', is_staff=True).save()
    User.objects.create_user('Alejandro Llovet', email='mabruka8@mailinator.com', password='bar', is_staff=True).save()
