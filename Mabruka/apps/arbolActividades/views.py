from django.apps import apps
from django.shortcuts import render
from django.views.generic import TemplateView
from apps.calendario.models import Evento
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers
import json
from .forms import ModificacionEventoForm
from django.views.generic.edit import FormView


# Create your views here.
#class Inicio(TemplateView, LoginRequiredMixin):
class Inicio(TemplateView):
    #model = Book
    template_name = "arbolActividades/inicio.html"
    #queryset = Evento.objects.all()
#   def head(self, *args, **kwargs):
#       last_book = self.get_queryset().latest('publication_date')
#       response = HttpResponse('')
#       # RFC 1123 date format
#       response['Last-Modified'] = last_book.publication_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
#       return response


def CrearEvento(request):
    if request.method != 'POST':
        raise Http404
    try:
        nombre = request.POST['nombre']
        evento = Evento(nombre=nombre)
        evento.save()
    except Exception as e:
        print(e)
        return HttpResponseBadRequest()
    return HttpResponse('<h1>Page was found</h1>')


def ObtenerHijos(request):
    if request.method != 'GET':
        raise Http404
    padre = None
    try:
        modelo_str = request.GET['model']
        pk_str = request.GET['pk']
        app_label, nombre_modelo = modelo_str.split(".")
        Modelo = apps.get_model(app_label, nombre_modelo)
        padre = Modelo.objects.get(pk=int(pk_str))
    except Exception:
        pass
    hijos = []
    if padre is None:
        hijos = Evento.objects.all()
    else:
        hijos = Evento.objects.all()
    data_json = serializers.serialize('json', hijos)
    return HttpResponse(data_json, content_type='application/json')


class ModificacionEventoView(FormView):
    template_name = 'arbolActividades/modificacion_evento.html'
    form_class = ModificacionEventoForm
    success_url = '/actividades/'

    def get_form(self, form_class):
        """
        Check if the user already saved contact details. If so, then show
        the form populated with those details, to let user change them.
        """
        try:
            evento = Evento.objects.get(pk=self.kwargs['id'])
            return form_class(instance=evento, **self.get_form_kwargs())
        except Evento.DoesNotExist:
            return form_class(**self.get_form_kwargs())

    def form_valid(self, form):
        #form.instance.nombre = self.request.nombre
        form.save()
        return super(ModificacionEventoView, self).form_valid(form)
