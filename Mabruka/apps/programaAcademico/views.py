from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class ProgramaAcademico(TemplateView):
    template_name = "programaAcademico/programa_academico.html"

    def get_context_data(self, **kwargs):
        context = super(ProgramaAcademico, self).get_context_data(**kwargs)
        context['evento_id'] = kwargs['id']
        return context
