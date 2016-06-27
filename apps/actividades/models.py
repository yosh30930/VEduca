import datetime

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMessage
from django.db import models, transaction, IntegrityError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from mptt.models import MPTTModel, TreeForeignKey

from apps.usuarios.models import SecretarioGeneral


class Nodo(MPTTModel):
    """
    Estructura que hace posible ver a las actividades como un árbol.

    Cada nodo está asociado a una actividad y viceversa. nodo <-> actividad

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
    Modelo base de cualquier tipo de actividad(Encuentro, Foro, Seminario, ...)
    """
    nombre = models.CharField(max_length=300)
    nodos = GenericRelation(
        'Nodo', content_type_field='content_type',
        object_id_field='content_id')
    responsables = models.ManyToManyField('usuarios.Persona', blank=True)
    anotaciones = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_edicion = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        es_creacion = self.pk is None
        # Se obtiene el elemento padre si es que se proporciona
        padre = kwargs.pop("padre", None)
        # Si es creacion se le asigna un nodo a la actividad y además se le
        # asigna un padre si es que se especificó
        if es_creacion:
            try:
                # (atomic) Evita que se cree una actividad sin nodo asociado
                with transaction.atomic():
                    super(Actividad, self).save(*args, **kwargs)
                    if padre is not None:  # Se especificó un padre
                        nodo = Nodo(
                            parent=padre.nodos.all().first(),
                            elemento=self)
                    else:  # No se especificó un padre de la actividad
                        nodo = Nodo(elemento=self)
                    nodo.save()
                    self.nodo = nodo
                    self.save()
            except IntegrityError as e:
                raise e
        else:  # Caso de modificación de la actividad
            super(Actividad, self).save(*args, **kwargs)

    def es_responsable(self, usuario, checar_padres=False):
        """
        Verifica si un usuario es responsable de la actividad
        """
        if not usuario.is_authenticated():
            return False
        if self.responsables.filter(pk=usuario.pk):
            return True
        if checar_padres and self.es_super_responsable(usuario):
            return True
        return False

    def es_super_responsable(self, usuario):
        """
        Verifica si un usuario es responsable de alguna actividad
        con jerarquía superior, es responsable de programa o
        tiene privilegios de secretario general
        """
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
        """
        Verifica si un usuario puede o no ver una actividad.
        Un usuario puede ver una actividad si tiene nivel de secretario
        general, si es responsable del programa o si tiene derecho de
        ver/modificar alguna actividad que sea descendiente de la que se
        está verificando.
        """
        return self.puede_ver_nodo(usuario)

    def puede_ver_nodo(self, usuario):
        """
        Verifica si un usuario puede o no ver un nodo.
        Un usuario puede ver un nodo si tiene nivel de secretario
        general, si es responsable del programa o si tiene derecho de
        ver/modificar algún nodo que sea descendiente de la que se
        está verificando.
        """
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
        ordering = ["fecha_creacion", "nombre"]


class Encuentro(Actividad):
    tipo = "encuentro"
    fecha_inicio = models.DateField(default=datetime.date.today)
    fecha_fin = models.DateField(default=datetime.date.today)
    pais = models.CharField(max_length=100, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        es_creacion = self.pk is None
        # Se obtiene el elemento padre
        nombres_sedes = None
        if "sedes" in kwargs:
            nombres_sedes = kwargs.pop("sedes", None)
            nombres_sedes = [x.lower() for x in nombres_sedes]
        try:
            with transaction.atomic():
                super(Encuentro, self).save(*args, **kwargs)
                if es_creacion and (nombres_sedes is not None):
                    for nombre_sede in nombres_sedes:
                        sede = Sede(nombre=nombre_sede, encuentro=self)
                        sede.save()
                elif nombres_sedes is not None:
                    sedes = Sede.objects.filter(encuentro=self)
                    sedes.exclude(nombre__in=nombres_sedes).delete()
                    for nombre_sede in nombres_sedes:
                        if len(sedes.filter(nombre=nombre_sede)) == 0:
                            sede = Sede(nombre=nombre_sede, encuentro=self)
                            sede.save()
        except IntegrityError as e:
            raise e


class Foro(Actividad):
    tipo = "foro"
    nombre_corto = models.CharField(max_length=200, blank=True)
    descripcion = models.TextField(default="", blank=True)


class Taller(Actividad):
    tipo = "taller"
    fecha = models.DateTimeField(null=True, blank=True)
    duracion_mins = models.PositiveSmallIntegerField(default=180)
    publico_objetivo = models.CharField(max_length=200, blank=True)
    espacio = models.ForeignKey(
        'Espacio', models.SET_NULL, blank=True, null=True)
    """
    organizan: compañía, institucion
    a cargo de persona
    ##
    organiza institucion
    coordina persona, institucion
    imparten personas,
    ##"""

    class Meta:
        verbose_name_plural = "talleres"


class Reunion(Actividad):
    tipo = "reunión"
    fecha = models.DateTimeField(null=True, blank=True)
    duracion_mins = models.PositiveSmallIntegerField(default=180)
    espacio = models.ForeignKey(
        'Espacio', models.SET_NULL, blank=True, null=True)
    tipo_asistencia = models.CharField(max_length=200, blank=True)
    """
    Auspicioan:
    Organizan: compañía, institucion
    Coordinan:
    """

    class Meta:
        verbose_name_plural = "talleres"


class Seminario(Actividad):
    tipo = "seminario"
    nombre_corto = models.CharField(max_length=60, blank=True)
    # fecha_tentativa = models.DateField(null=True, blank=True)
    # hora_tentativa = models.TimeField(null=True, blank=True)


class PresentacionPonencia(Actividad):
    tipo = "presentación de ponencia"
    fecha = models.DateTimeField(null=True, blank=True)
    duracion_mins = models.PositiveSmallIntegerField(default=60)
    orden = models.PositiveSmallIntegerField()


class SesionEspecial(Actividad):
    tipo = "sesión especial"
    fecha = models.DateTimeField(null=True, blank=True)
    duracion_mins = models.PositiveSmallIntegerField(default=60)
    orden = models.PositiveSmallIntegerField()


class OtraActividadSeminario(Actividad):
    tipo = "otra actividad de seminario"
    fecha = models.DateTimeField(null=True, blank=True)
    duracion_mins = models.PositiveSmallIntegerField(default=60)
    orden = models.PositiveSmallIntegerField()


class Panel(Actividad):
    tipo = "panel"
    nombre_corto = models.CharField(max_length=200, blank=True)
    espacio = models.ForeignKey(
        'Espacio', models.SET_NULL, blank=True, null=True)
    fecha = models.DateTimeField(null=True, blank=True)
    duracion = models.PositiveSmallIntegerField(default=1 * 60)
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = "paneles"


# Lista de Clases de las distintas Actividades
modelosActividades = [Encuentro, Foro, Seminario, Panel]

"""
def encuentro_responsables_cambiados(sender, instance, **kwargs):
    # Sólo se ejecuta en el post_add y no en el pre_add
    if kwargs['action'] != "post_add":
        return
    asunto = "Virtual Educa - Se te asignó como responsable"
    remitente = "sainoba@gmail.com"
    destinatarios = [responsable.email for responsable in  Usuario.objects.filter(pk__in=kwargs['pk_set'])]
    ctx = {
        'nombre_actividad': instance.nombre,
        'protocol': "http",
        'domain': "127.0.0.1:8000/",
        'site_name': "Virtual Educa",
    }
    mensaje = render_to_string("sesion/asignacion_responsable_correo.html", ctx)
    EmailMessage(asunto, mensaje,
                 to=destinatarios, from_email=remitente).send()


m2m_changed.connect(
    encuentro_responsables_cambiados, sender=Encuentro.responsables.through)
"""

"""
class Participante(models.Model):

    Representan a los participantes de los encuentro, si este tiene asociado
    un encuentro entonces sólo será recomendado en ese encuentro

    nombre = models.CharField(max_length=100)
    puesto = models.TextField()
    pais = CountryField(blank=True, null=True)
    encuentro = models.ForeignKey(
        'Encuentro', blank=True, null=True,
        on_delete=models.SET_NULL)
"""

"""
class ParticipanteActividad(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_id = models.PositiveIntegerField()
    actividad = GenericForeignKey('content_type', 'content_id')
    rol = models.ForeignKey('Rol', models.CASCADE)
    participante = models.ForeignKey('Usuario', models.CASCADE)
    institucion = models.ForeignKey(
        'Institucion', blank=True, null=True,
        on_delete=models.SET_NULL)


class Rol(models.Model):
    nombre = models.CharField(max_length=100)
    checa_conflictos = models.BooleanField(default=True)
"""


class Sede(models.Model):
    """
    Lugar donde se encuentran los espacios disponibles para las distintas
    actividades de un encuentro, como talleres, palenes, magistrales, etc...
    """
    nombre = models.CharField(max_length=100)
    encuentro = models.ForeignKey('Encuentro', models.CASCADE)


class Espacio(models.Model):
    """
    Espacios disponibles en un encuentro para ser asignado a alguna actividad.
    Cade encuentro tiene una o más sedes y cada sede tiene espacios.
    """
    nombre = models.CharField(max_length=100)
    sede = models.ForeignKey('Sede', models.CASCADE)
    cupo = models.PositiveIntegerField(null=True, blank=True)

    def get_actividades(self):
        """
        Obtiene la lista de actividades que están asociadas a este espacio
        """
        lista_querys = []
        relaciones = self._meta.related_objects
        for relacion in relaciones:
            Modelo = getattr(relacion, 'related_model', None)
            if Modelo is None or (not isinstance(Modelo, Actividad)):
                continue
            query_result = Modelo.objects.filter(espacio=self)
            if query_result:  # Si hubo al menos un resultado
                lista_querys.append(query_result)
        return lista_querys
