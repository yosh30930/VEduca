from django.apps import apps
#  from django.shortcuts import render
from django.views.generic import TemplateView
from django.core import serializers
from django.http import HttpResponse
from .models import Evento, Foro, Seminario, Panel, Relacion
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.http import Http404, HttpResponseBadRequest
import json

# Create your views here.


class CalendarioHome(TemplateView):
    template_name = "calendario/calendario_home.html"

    def get_context_data(self, **kwargs):
        context = super(CalendarioHome, self).get_context_data(**kwargs)
        context['evento_id'] = kwargs['id']
#       context['latest_articles'] = Article.objects.all()[:5]
        return context


@transaction.atomic
def crea_actividad(Modelo, nombre, padre, *args, **kwargs):
    try:
        with transaction.atomic():
            actividad = Modelo(nombre=nombre, *args, **kwargs)
            actividad.save()
            relacion = Relacion(padre=padre, hijo=actividad)
            relacion.save()
            actividad.relacion = relacion
            actividad.save()
            return actividad
    except IntegrityError as e:
        raise e


def ResetActividades():
    modelos = [Evento, Foro, Seminario, Panel, Relacion]
    for modelo in modelos:
        modelo.objects.all().delete()
    evento = Evento(nombre="Encuentro Internacional 2016 Costa Rica")
    evento.save()
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
    if request.method != 'POST':
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
    relaciones = Relacion.objects.filter(
            padre_id=padre.id,
            padre_type=ContentType.objects.get_for_model(padre)
        )
    hijos = [obten_hijos(relacion.hijo) for relacion in relaciones]
    return {'padre': padre, 'hijos': hijos}


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
