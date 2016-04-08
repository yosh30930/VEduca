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

from apps.programaAcademico.views import set_context_tab_menu
from apps.actividades.models import Encuentro
from apps.usuarios.models import SecretarioGeneral


class CalendarioHome(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "calendario/calendario_home.html"

    def test_func(self, user):
        if not user.is_staff:
            return False
        if (SecretarioGeneral.objects.filter(usuario=user) or
                user.is_superuser):
            return True
        try:
            encuentro = Encuentro.objects.get(id=self.kwargs['id'])
            if encuentro.responsables.filter(pk=user.pk):
                return True
        except Encuentro.ObjectDoesNotExist:
            raise Http404
        return False

    def get_context_data(self, **kwargs):
        context = super(CalendarioHome, self).get_context_data(**kwargs)
        context['encuentro_id'] = kwargs['id']
        try:
            encuentro = Encuentro.objects.get(id=kwargs['id'])
        except Encuentro.ObjectDoesNotExist:
            raise Http404
        set_context_tab_menu(context, self.request.user, encuentro)
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
