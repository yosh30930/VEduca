from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from mptt.models import MPTTModel, TreeForeignKey
import datetime


class Espacio(models.Model):
    """
    Guarda los espacios disponibles en un encuentro para ser
    asignado a alguna actividad.
    """
    nombre = models.CharField(max_length=300)
    encuentro = models.ForeignKey(
        'Encuentro', models.CASCADE)


class Nodo(MPTTModel):
    """
    Estructura que hace posible ver a las actividades como un árbol.

    Cada nodo está asociado a una actividad y viceversa.

    ¿Por qué no se hizo que cada actividad heredara de MPTTModel en vez de
    crear una estructura 'Nodo' con apuntadores a actividades?
    Una actividad no puede ser un nodo porque el árbol sólo puede tener nodos
    del mismo tipo, por lo que un Foro no podría tener hijos tipo Seminario.
    Por esto se tiene la estructura Nodo con un apuntador genérico a cualquier
    tipo de actividad.
    """
    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children', db_index=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    elemento = GenericForeignKey('content_type', 'content_id')

    def obten_nodo(objeto_relacionado):
        """Regresa el nodo asociado a una actividad"""
        tipo_objeto = ContentType.objects.get_for_model(objeto_relacionado)
        nodo = Nodo.objects.filter(
            content_type__pk=tipo_objeto.id,
            content_id=objeto_relacionado.id).first()
        return nodo


class ActividadManager(models.Manager):
    """
    Gestor de actividades que se encarga de crear un nodo y asociarlo
    a la actividad que se está creando
    """
    def crear(self, **kwargs):
        padre = None
        if "padre" in kwargs:
            padre = kwargs.pop("padre", None)
        try:
            actividad = self.create(**kwargs)
            nodo = None
            if padre is None:
                nodo = Nodo(elemento=actividad).save()
            else:
                nodo = Nodo(
                    parent=padre.nodos.all().first(),
                    elemento=actividad).save()
            actividad.nodo = nodo
            return actividad
        except Exception as e:
            raise e


class Actividad(models.Model):
    """
    Base de cualquier tipo de actividad(Encuentro, Foro, Seminario, ...)
    """
    objects = ActividadManager()
    nombre = models.CharField(max_length=300)
    nodos = GenericRelation(
        'Nodo', content_type_field='content_type',
        object_id_field='content_id')
    responsables = models.ManyToManyField(User, blank=True)

    class Meta:
        abstract = True


class Programables(models.Model):
    """
    Base de las actividades que pueden ser programadas a alguna hora
    en específico
    """
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class ConLocacion(models.Model):
    espacio = models.ForeignKey(
        'Espacio', models.SET_NULL, blank=True, null=True)

    class Meta:
        abstract = True


class Encuentro(Actividad):
    fecha_inicio = models.DateField(default=datetime.date.today)
    fecha_fin = models.DateField(default=datetime.date.today)


class Foro(Actividad):
    nombre_corto = models.CharField(max_length=60, blank=True)
    descripcion = models.TextField(default="", blank=True)


class Seminario(Actividad):
    pass


class Panel(Actividad, Programables, ConLocacion):

    class Meta:
        verbose_name_plural = "paneles"
