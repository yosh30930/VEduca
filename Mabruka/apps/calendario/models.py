from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from mptt.models import MPTTModel, TreeForeignKey


class Nodo(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    elemento = GenericForeignKey('content_type', 'content_id')

    def obten_nodo(objeto_relacionado):
        tipo_objeto_relacionado = ContentType.objects.get_for_model(objeto_relacionado)
        nodo = Nodo.objects.filter(content_type__pk=tipo_objeto_relacionado.id, content_id=objeto_relacionado.id).first()
        return nodo

class ActividadManager(models.Manager):
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
                nodo = Nodo(parent=padre.nodos.all().first(), elemento=actividad).save()
            actividad.nodo = nodo
            return actividad
        except Exception as e:
            raise e
        # do something with the book


# Create your models here.
class Actividad(models.Model):
    nombre = models.CharField(max_length=300)
    nodos = GenericRelation('Nodo', content_type_field='content_type', object_id_field='content_id')
    objects = ActividadManager()


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


class Responsables(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    actividad_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    actividad_id = models.PositiveIntegerField()
    actividad = GenericForeignKey('actividad_type', 'actividad_id')


class Evento(Actividad):
    pass


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
