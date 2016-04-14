from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django_countries.fields import CountryField
from django.utils import timezone


class UserManager(BaseUserManager):
    def _create_user(self, correo, contrasena, is_staff, is_superuser,
                     **extra_fields):
        now = timezone.now()
        if not correo:
            raise ValueError('El correo es obligatorio')
        correo = self.normalize_email(correo)
        usuario = self.model(correo=correo, is_active=True, is_staff=is_staff,
                             is_superuser=is_superuser, fecha_registro=now,
                             **extra_fields)
        usuario.set_password(contrasena)
        usuario.save(using=self._db)
        return usuario

    def create_user(self, nombre_usuario, correo, contrasena=None,
                    **extra_fields):
        return self._create_user(
            nombre_usuario, correo, contrasena, False, False, **extra_fields)

    def create_superuser(self, nombre_usuario, correo, contrasena=None,
                         **extra_fields):
        return self._create_user(nombre_usuario, correo, contrasena, True,
                                 True, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    correo = models.EmailField("correo electrónico",
                               max_length=254, unique=True)
    nombres = models.CharField("nombre(s)", max_length=100)
    apellidos = models.CharField("apellido(s)", max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField('fecha registro',
                                          default=timezone.now)
    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombres']

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def get_full_name(self):
        full_name = '%s %s' % (self.nombres, self.apellidos)
        return full_name.strip()

    def get_short_name(self):
        return self.nombres

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.correo])


class SecretarioGeneral(models.Model):
    """
    Indica los usuarios que tiene permisos del nivel de secretario
    general
    """
    usuario = models.ForeignKey(Usuario, models.CASCADE)


class Participante(models.Model):
    """
    Representan a los participantes de los encuentro, si este tiene asociado
    un encuentro entonces sólo será recomendado en ese encuentro
    """
    nombre = models.CharField(max_length=100)
    puesto = models.TextField()
    pais = CountryField(blank=True, null=True)
    encuentro = models.ForeignKey(
        'actividades.Encuentro', blank=True, null=True,
        on_delete=models.SET_NULL)
