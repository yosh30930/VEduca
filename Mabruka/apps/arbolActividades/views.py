from django.shortcuts import render
from django.views.generic import ListView
from apps.calendario.models import Evento
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
#class Inicio(ListView, LoginRequiredMixin):
class Inicio(ListView):
    #model = Book
    template_name = "arbolActividades/inicio.html"
    queryset = Evento.objects.all()
#   def head(self, *args, **kwargs):
#       last_book = self.get_queryset().latest('publication_date')
#       response = HttpResponse('')
#       # RFC 1123 date format
#       response['Last-Modified'] = last_book.publication_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
#       return response

