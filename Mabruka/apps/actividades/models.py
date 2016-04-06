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

    def get_actividades(self):
        lista_querys = []
        relaciones = self._meta.related_objects
        for relacion in relaciones:
            Modelo = relacion.related_model
            query_result = Modelo.objects.filter(espacio=self)
            if query_result:  # Si hubo al menos un resultado
                lista_querys.append(query_result)
        return lista_querys


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


class Actividad(models.Model):
    """
    Base de cualquier tipo de actividad(Encuentro, Foro, Seminario, ...)
    """
    nombre = models.CharField(max_length=300)
    nodos = GenericRelation(
        'Nodo', content_type_field='content_type',
        object_id_field='content_id')
    responsables = models.ManyToManyField(User, blank=True)
    anotaciones = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        es_creacion = self.pk is None
        # Se obtiene el elemento padre
        padre = None
        if "padre" in kwargs:
            padre = kwargs.pop("padre", None)
        print("Salvando al soldado", self)
        super(Actividad, self).save(*args, **kwargs)

        # Le asigna un nodo a la actividad y se
        # le asigna un padre si es que se especificó
        if es_creacion:
            # Se encarga del nodo
            if padre is not None:
                nodo = Nodo(
                    parent=padre.nodos.all().first(),
                    elemento=self)
            else:
                nodo = Nodo(elemento=self)
            nodo.save()
            self.nodo = nodo
            # Se encarga de las horas
            self.save()

    class Meta:
        abstract = True


class ConFecha(Actividad):
    """
    Base de las actividades que pueden ser programadas a alguna hora
    en específico
    """
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class ConLocacion(Actividad):
    espacio = models.ForeignKey(
        'Espacio', models.SET_NULL, blank=True, null=True)

    class Meta:
        abstract = True


class ConLocacionYFecha(ConLocacion):
    fecha_inicio = models.DateTimeField(auto_now_add=True)
    fecha_fin = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class Encuentro(Actividad):
    fecha_inicio = models.DateField(default=datetime.date.today)
    fecha_fin = models.DateField(default=datetime.date.today)
    tipo = "encuentro"


class Foro(Actividad):
    nombre_corto = models.CharField(max_length=60, blank=True)
    descripcion = models.TextField(default="", blank=True)
    tipo = "foro"


class Taller(ConLocacionYFecha):
    tipo = "taller"

    class Meta:
        verbose_name_plural = "talleres"


class Reunion(ConLocacionYFecha):
    tipo = "reunion"

    class Meta:
        verbose_name_plural = "reuniones"


class Sesion(Actividad):
    tipo = "sesion"

    class Meta:
        verbose_name_plural = "sesiones"


class Seminario(Actividad):
    tipo = "seminario"

    pass


class Panel(ConLocacionYFecha):
    tipo = "panel"

    class Meta:
        verbose_name_plural = "paneles"
