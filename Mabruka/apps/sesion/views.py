from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.views import login
# from django.core.urlresolvers import reverse
# Create your views here.
from apps.usuarios.models import Usuario
from apps.actividades.models import Encuentro, Foro, Seminario, Panel, Espacio


class InicioSesionView(View):
    def get(self, request, *args, **kwargs):
        if len(Encuentro.objects.all()) == 0:
            ResetActividades()
        if len(Usuario.objects.all()) == 0:
            print(len(Usuario.objects.all()))
            ResetUsuarios()
            print(len(Usuario.objects.all()))
        if len(Espacio.objects.all()) == 0:
            ResetEspacios()
        if request.user.is_authenticated():
        #   return HttpResponseRedirect(reverse('login'))
            return HttpResponseRedirect('/inicio/')
        else:
            template_name = 'sesion/inicio_sesion.html'
            return login(request, *args, template_name=template_name, **kwargs)

    def post(self, request, *args, **kwargs):
        template_name = 'sesion/inicio_sesion.html'
        return login(request, *args, template_name=template_name, **kwargs)


@transaction.atomic
def crea_actividad(Modelo, nombre, padre, *args, **kwargs):
    try:
        with transaction.atomic():
            actividad = Modelo(nombre=nombre, *args, **kwargs)
            actividad.save(padre=padre)
            return actividad
    except IntegrityError as e:
        raise e


def ResetActividades():
    modelos = [Encuentro, Foro, Seminario, Panel]
    for modelo in modelos:
        modelo.objects.all().delete()
    encuentro = Encuentro.objects.create(nombre="Encuentro Internacional 2016 Costa Rica")
    foro1 = crea_actividad(
        Foro, "Educación Superior, Innovación e Internacionalización", encuentro,
        nombre_corto="Educación Superior")
    foro2 = crea_actividad(
        Foro, "Investigación, Desarrollo e Innovación (I+D+i) ", encuentro,
        nombre_corto="(I+D+i) ")
    seminario11 = crea_actividad(
        Seminario, "Programa Piloto Inclusión Digital, Estrategia Digital\
        Nacional, Gobierno de México", foro1)
    seminario21 = crea_actividad(
        Seminario, "Programa Piloto de Inclusión Digital, Estrategia Digital\
        Nacional, Gobierno de México", foro2)
    for idx in range(3):
        crea_actividad(Panel, "Panel 1." + str(idx), seminario11)
    for idx in range(3):
        crea_actividad(Panel, "Panel 2." + str(idx), seminario21)
    return


def ResetUsuarios():
    Usuario.objects.all().delete()
    Usuario.objects.create_superuser('sainoba@gmail.com', nombres='Marco Nila', contrasena='bar').save()
    Usuario.objects.create_user('mabruka1@mailinator.com', nombres='Fernando Gamboa', contrasena='bar', is_staff=True).save()
    Usuario.objects.create_user('mabruka2@mailinator.com', nombres='Elena García', contrasena='bar', is_staff=True).save()
    Usuario.objects.create_user('mabruka3@mailinator.com', nombres='Pedro Rocha', contrasena='bar', is_staff=True).save()
    Usuario.objects.create_user('mabruka4@mailinator.com', nombres='Juan Luis Valdés', contrasena='bar', is_staff=True).save()
    Usuario.objects.create_user('mabruka5@mailinator.com', nombres='Julieta Palma', contrasena='bar', is_staff=True).save()
    Usuario.objects.create_user('mabruka6@mailinator.com', nombres='Juan Manuel Valdés', contrasena='bar', is_staff=True).save()
    Usuario.objects.create_user('mabruka7@mailinator.com', nombres='Luis Andrés Ochoa', contrasena='bar', is_staff=True).save()
    Usuario.objects.create_user('mabruka8@mailinator.com', nombres='Alejandro Llovet', contrasena='bar', is_staff=True).save()


def ResetEspacios():
    Espacio.objects.all().delete()
    encuentros = Encuentro.objects.all()
    idx = 1
    for encuentro in encuentros:
        for _ in range(10):
            nombre = "Espacio " + str(idx)
            Espacio(nombre=nombre, encuentro=encuentro).save()
            idx += 1
