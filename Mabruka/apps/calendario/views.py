from django.apps import apps
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import TemplateView, View

from braces.views import LoginRequiredMixin, UserPassesTestMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def get_encuentros(request):
    """
    Regresa una lista de todos los encuentros.
    """
    if request.method == "GET":
        encuentros = Encuentro.objects.all()
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


class CalendarioHome(TemplateView):
    template_name = "calendario/calendario_home.html"

    def get_context_data(self, **kwargs):
        context = super(CalendarioHome, self).get_context_data(**kwargs)
        context['encuentro_id'] = kwargs['id']
#       context['latest_articles'] = Article.objects.all()[:5]
        return context


def ActualizarActividad(request):
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


class ActualizarActividadView(LoginRequiredMixin,
                              UserPassesTestMixin, View):

    def test_func(self, user):
        return True

    def post(self, request, *args, **kwargs):
        fecha_inicio = request.POST['fecha_inicio']
        fecha_fin = request.POST['fecha_fin']
        modelo = kwargs['tipo']
        pk = kwargs['id']
        Modelo = apps.get_model('actividades', modelo)
        actividad = Modelo.objects.get(pk=pk)
        actividad.fecha_inicio = fecha_inicio
        actividad.fecha_fin = None if fecha_fin == "null" else fecha_fin
        actividad.save()
        return HttpResponse('Hello, World!')
