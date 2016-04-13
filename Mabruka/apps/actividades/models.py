import datetime

from django.db import models, transaction, IntegrityError
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

from mptt.models import MPTTModel, TreeForeignKey

from apps.usuarios.models import SecretarioGeneral


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
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_edicion = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        es_creacion = self.pk is None
        # Se obtiene el elemento padre
        padre = None
        if "padre" in kwargs:
            padre = kwargs.pop("padre", None)
        # Le asigna un nodo a la actividad y se
        # le asigna un padre si es que se especificó
        if es_creacion:
            # Se encarga del nodo
            try:
                with transaction.atomic():
                    super(Actividad, self).save(*args, **kwargs)
                    if padre is not None:
                        nodo = Nodo(
                            parent=padre.nodos.all().first(),
                            elemento=self)
                    else:
                        nodo = Nodo(elemento=self)
                    nodo.save()
                    self.nodo = nodo
                    self.save()
            except IntegrityError as e:
                raise e
        else:
            super(Actividad, self).save(*args, **kwargs)

    def es_responsable(self, usuario, checar_padres=False):
        if not usuario.is_authenticated():
            return False
        if self.responsables.filter(pk=usuario.pk):
            return True
        if checar_padres and self.es_super_responsable(usuario):
            return True
        return False

    def es_super_responsable(self, usuario):
        if not usuario.is_authenticated():
            return False
        if (usuario.is_superuser or
                SecretarioGeneral.objects.filter(usuario=usuario)):
            return True
        # Se verifica si es responsable de alguna actividad de mayor
        # jerarquía
        nodo_actividad = self.nodos.first()
        ancestros_actividad = nodo_actividad.get_ancestors()
        if ancestros_actividad:
            query_results = []  # Querys donde es responsable de alguna actividad
            for Modelo in modelosActividades:
                query_result = Modelo.objects.filter(responsables=usuario)
                query_results.append(query_result)
                for query_result in query_results:
                    for actividad_tmp in query_result:
                        nodo_tmp = actividad_tmp.nodos.first()
                        if nodo_tmp in ancestros_actividad:
                            return True
        return False

    def puede_ver_actividad(self, usuario):
        return self.puede_ver_nodo(usuario)

    def puede_ver_nodo(self, usuario):
        nodo_actividad = self.nodos.first()
        if not usuario.is_authenticated():
            return True
        # Verifica si el usuario es super usuario o Secretari General
        if (usuario.is_superuser or
                SecretarioGeneral.objects.filter(usuario=usuario)):
            return True
        # Verifica si el usuario es responsable de alguno
        # de los hijos de la actividad
        ancestros_actividad = nodo_actividad.get_ancestors(include_self=True)

        query_results = []  # Querys donde es responsable de alguna actividad
        for Modelo in modelosActividades:
            try:
                query_result = Modelo.objects.filter(responsables=usuario)
                query_results.append(query_result)
            except Modelo.FieldDoesNotExist:
                continue
            for query_result in query_results:
                for actividad_tmp in query_result:
                    nodo_tmp = actividad_tmp.nodos.first()
                    # Pregunta si es responsable de una actividad
                    # de mayor jerarquía
                    if nodo_tmp in ancestros_actividad:
                        return True
                    arbol_actividad_tmp = nodo_tmp.get_ancestors(
                        include_self=True)
                    if nodo_actividad in arbol_actividad_tmp:
                        return True
        # Verifica si es responsable de los espacios del encuentro
        return False

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
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)

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


class Panel(ConLocacionYFecha):
    tipo = "panel"
    intervienen = models.ManyToManyField('usuarios.Participante', blank=True)
    coordinador = models.ForeignKey(
        'usuarios.Participante', models.SET_NULL, blank=True, null=True,
        related_name="coordiandor_panel")
    moderador = models.ForeignKey(
        'usuarios.Participante', models.SET_NULL, blank=True, null=True,
        related_name="moderador_panel")

    class Meta:
        verbose_name_plural = "paneles"

modelosActividades = [Encuentro, Foro, Seminario, Panel]
