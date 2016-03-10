from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class Actividad(models.Model):
    nombre = models.CharField(max_length=300)
    relacion = models.OneToOneField(
        'Relacion', on_delete=models.CASCADE, null=True)

    class Meta:
        abstract = True


class Programables(models.Model):
    allDay = models.NullBooleanField(default=True)
    start = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True)
    calId = models.CharField(max_length=60)

    class Meta:
        abstract = True


class Espacio(models.Model):
    nombre = models.CharField(max_length=300)


class Relacion(models.Model):
    padre_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_as_padre")
    padre_id = models.PositiveIntegerField()
    padre = GenericForeignKey('padre_type', 'padre_id')
    hijo_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_as_hijo")
    hijo_id = models.PositiveIntegerField()
    hijo = GenericForeignKey('hijo_type', 'hijo_id')


class Responsables(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    actividad_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    actividad_id = models.PositiveIntegerField()
    actividad = GenericForeignKey('actividad_type', 'actividad_id')


class Evento(models.Model):
    nombre = models.CharField(max_length=120)


class EncuentroInternacional(Evento):
    class Meta:
        verbose_name_plural = "Encuentros Internacionales"


class Foro(Actividad):
    nombre_corto = models.CharField(max_length=60)


class Seminario(Actividad):
    pass


class Panel(Actividad, Programables):
    pass

    class Meta:
        verbose_name_plural = "Paneles"
