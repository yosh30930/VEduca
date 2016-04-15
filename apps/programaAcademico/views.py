from django.http import Http404
# from django.shortcuts import render
from django.views.generic import TemplateView

from braces.views import LoginRequiredMixin

from apps.actividades.models import Encuentro
from apps.usuarios.models import SecretarioGeneral


class ProgramaAcademico(LoginRequiredMixin, TemplateView):
    template_name = "programaAcademico/programa_academico.html"

    login_url = "/"

    def get_context_data(self, **kwargs):
        context = super(ProgramaAcademico, self).get_context_data(**kwargs)
        context['encuentro_id'] = kwargs['id']
        try:
            encuentro = Encuentro.objects.get(id=kwargs['id'])
        except Encuentro.ObjectDoesNotExist:
            raise Http404
        set_context_tab_menu(context, self.request.user, encuentro)
        return context


def set_context_tab_menu(context, usuario, encuentro):
    if not usuario.is_authenticated():
        return
    # Indica quienes pueden ver el prográma académico
    if encuentro.puede_ver_actividad(usuario):
        context['puede_programa_academico'] = True
    # Indica quienes pueden ver el calendario del programa académico
    if (usuario.is_superuser or
            SecretarioGeneral.objects.filter(usuario=usuario) or
            encuentro.responsables.filter(pk=usuario.pk)):
        context['puede_logistica'] = True
    # Indica quienes pueden ver los espacios disponibles para el encuentro
    if (usuario.is_superuser or
            SecretarioGeneral.objects.filter(usuario=usuario) or
            encuentro.responsables.filter(pk=usuario.pk)):
        context['puede_espacios'] = True
