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
        """
        Función test de UserPassesTestMixin para indicar si una persona
        tiene derecho a ver esta vista
        """
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


class ActualizarActividadView(LoginRequiredMixin,
                              UserPassesTestMixin, View):

    def test_func(self, user):
        """
        Función test de UserPassesTestMixin para indicar si una persona
        tiene derecho a ver esta vista
        """
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
