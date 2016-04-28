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
        persona = Persona(**kwargs_persona)
        usuario = None
        try:
            with transaction.atomic():
                persona.save()
                usuario = self.model(is_active=True, is_staff=is_staff,
                                     is_superuser=is_superuser, correo=persona,
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
    correo = models.OneToOneField('Persona', on_delete=models.CASCADE,
                                  to_field='correo')

    USERNAME_FIELD = 'correo'
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


class SecretarioGeneral(models.Model):
    """
    Indica los usuarios que tiene permisos del nivel de secretario
    general
    """
    usuario = models.ForeignKey('Usuario', models.CASCADE)


class Persona(models.Model):
    correo = models.EmailField("correo electrónico",
                               max_length=254, unique=True)
    correo_secundario = models.EmailField(
        "correo secundario", max_length=254, blank=True)
    nombres = models.CharField("nombre(s)", max_length=100)
    apellidos = models.CharField("apellido(s)", max_length=100)
    fecha_registro = models.DateTimeField('fecha de registro',
                                          default=timezone.now)
    es_coordinador = models.BooleanField(default=False)
    pais = models.ForeignKey('Pais', default="")

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
