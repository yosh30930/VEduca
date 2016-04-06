from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.views import login
# from django.core.urlresolvers import reverse
# Create your views here.
from django.contrib.auth.models import User
from apps.actividades.models import Encuentro, Foro, Seminario, Panel, Espacio


class InicioSesionView(View):
    def get(self, request, *args, **kwargs):
        if len(Encuentro.objects.all()) == 0:
            ResetActividades()
        if len(User.objects.all()) == 0:
            print(len(User.objects.all()))
            ResetUsuarios()
            print(len(User.objects.all()))
        if len(Espacio.objects.all()) == 0:
            ResetEspacios()
        if request.user.is_authenticated():
        #   return HttpResponseRedirect(reverse('login'))
            return HttpResponseRedirect('/inicio/')
        else:
            template_name = 'sesion/inicio_sesion.html'
            return login(request, *args, template_name=template_name, **kwargs)

    def post(self, request, *args, **kwargs):
        return login(request, *args, **kwargs)


@transaction.atomic
def crea_actividad(Modelo, nombre, padre, *args, **kwargs):
    try:
        with transaction.atomic():
            actividad = Modelo.objects.crear(nombre=nombre, padre=padre, *args, **kwargs)
            return actividad
    except IntegrityError as e:
        raise e


def ResetActividades():
    modelos = [Encuentro, Foro, Seminario, Panel]
    for modelo in modelos:
        modelo.objects.all().delete()
    encuentro = Encuentro.objects.crear(nombre="Encuentro Internacional 2016 Costa Rica")
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
        crea_actividad(Panel, "Panel 1." + str(idx), seminario11, calId="0")
    for idx in range(3):
        crea_actividad(Panel, "Panel 2." + str(idx), seminario21, calId="0")
    return


def ResetUsuarios():
    User.objects.all().delete()
    User.objects.create_superuser('foo', email='sainoba@gmail.com', password='bar').save()
    User.objects.create_user('Fernando Gamboa', email='mabruka1@mailinator.com', password='bar', is_staff=True).save()
    User.objects.create_user('Elena García', email='mabruka2@mailinator.com', password='bar', is_staff=True).save()
    User.objects.create_user('Pedro Rocha', email='mabruka3@mailinator.com', password='bar', is_staff=True).save()
    User.objects.create_user('Juan Luis Valdés', email='mabruka4@mailinator.com', password='bar', is_staff=True).save()
    User.objects.create_user('Julieta Palma', email='mabruka5@mailinator.com', password='bar', is_staff=True).save()
    User.objects.create_user('Juan Manuel Valdés', email='mabruka6@mailinator.com', password='bar', is_staff=True).save()
    User.objects.create_user('Luis Andrés Ochoa', email='mabruka7@mailinator.com', password='bar', is_staff=True).save()
    User.objects.create_user('Alejandro Llovet', email='mabruka8@mailinator.com', password='bar', is_staff=True).save()


def ResetEspacios():
    Espacio.objects.all().delete()
    encuentros = Encuentro.objects.all()
    idx = 1
    for encuentro in encuentros:
        for _ in range(10):
            nombre = "Espacio " + str(idx)
            Espacio(nombre=nombre, encuentro=encuentro).save()
            idx += 1
