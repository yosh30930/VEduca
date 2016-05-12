from django.db import models, transaction, IntegrityError
from django.core.mail import send_mail
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, correo, contrasena, is_staff, is_superuser,
                     **extra_fields):
        if not correo:
            raise ValueError('El correo es obligatorio')
        correo = self.normalize_email(correo)
        kwargs_persona = {'correo': correo}
        campos_persona = ['correo_secundario', 'nombres',
                          'apellidos', 'fecha_registro', 'es_coordinador']
        for campo in campos_persona:
            val = extra_fields.pop(campo, None)
            if val is not None:
                kwargs_persona[campo] = val
        persona = None
        try:
            persona = Persona.objects.get(correo=correo)
        except Persona.DoesNotExist:
            persona = Persona(**kwargs_persona)
        usuario = None
        try:
            with transaction.atomic():
                persona.save()
                usuario = self.model(is_active=True, is_staff=is_staff,
                                     is_superuser=is_superuser, email=persona,
                                     **extra_fields)
                usuario.set_password(contrasena)
                usuario.save(using=self._db)
        except IntegrityError as e:
            raise e
        return usuario

    def create_user(self, correo, contrasena=None, is_staff=False,
                    **extra_fields):
        return self._create_user(
            correo, contrasena, is_staff, False, **extra_fields)

    def create_superuser(self, correo, contrasena=None,
                         **extra_fields):
        return self._create_user(
            correo, contrasena, True, True, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email = models.OneToOneField('Persona', on_delete=models.CASCADE,
                                 to_field='correo')

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['nombres']

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def get_full_name(self):
        full_name = '%s %s' % (self.persona.nombres, self.persona.apellidos)
        return full_name.strip()

    def get_short_name(self):
        return self.persona.nombres

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.persona.correo])

    def __str__(self):
        return self.email.correos


class SecretarioGeneral(models.Model):
    """
    Indica los usuarios que tiene permisos del nivel de secretario
    general
    """
    usuario = models.ForeignKey('Usuario', models.CASCADE)


class Persona(models.Model):
    DR_GRADO = 1
    DRA_GRADO = 2
    MTRO_GRADO = 3
    MTRA_GRADO = 4
    LIC_GRADO = 5
    OTRO_GRADO = 6
    GRADO_CHOICES = (
        (DR_GRADO, 'Dr'),
        (DRA_GRADO, 'Dra'),
        (MTRO_GRADO, 'Mtro'),
        (MTRA_GRADO, 'Mtra'),
        (LIC_GRADO, 'Lic'),
        (OTRO_GRADO, ''),
    )
    correo = models.EmailField("correo electrónico",
                               max_length=254, unique=True)
    correo_secundario = models.EmailField(
        "correo secundario", max_length=254, blank=True)
    nombres = models.CharField("nombre(s)", max_length=100)
    apellido_paterno = models.CharField("apellido paterno", max_length=100)
    apellido_materno = models.CharField("apellido materno", max_length=100,
                                        blank=True)
    fecha_registro = models.DateTimeField('fecha de registro',
                                          default=timezone.now)
    pais = models.ForeignKey('Pais', default="")
    grado = models.IntegerField(choices=GRADO_CHOICES, default=OTRO_GRADO)

    def get_full_name(self):
        full_name = '%s %s' % (self.nombres, self.apellidos)
        return full_name.strip()

    def get_short_name(self):
        return self.nombres

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        correos = [self.correo]
        if self.correo_secundario != "":
            correos.append(self.correo_secundario)
        send_mail(subject, message, from_email, correos)


class Pais(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=50)


class Puesto(models.Model):
    persona = models.ForeignKey('Persona', on_delete=models.CASCADE)
    institucion = models.ForeignKey('Institucion', on_delete=models.CASCADE)
    cargo = models.CharField(max_length=300)


class Institucion(models.Model):
    ESCOLAR_TIPO = 1
    EMPRESA_TIPO = 2
    TIPO_CHOICES = (
        (ESCOLAR_TIPO, 'Escolar'),
        (EMPRESA_TIPO, 'Empresa'),
    )
    nombre = models.CharField(max_length=150)
    nombre_corto = models.CharField(max_length=150, default="")
    pais = models.ForeignKey('Pais', default="")
