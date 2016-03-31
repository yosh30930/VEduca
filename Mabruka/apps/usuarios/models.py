from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, User)
# Create your models here.

"""
class UserManager(BaseUserManager):
    def _create_user(self, nombre_usuario, correo, contraseña, is_staff,
        is_superuser, **extra_fields):
        if not correo:
            raise ValueError('El correo es obligatorio')
        correo = self.normalize_email(correo)
        usuario = self.model(nombre_usuario=nombre_usuario, correo=correo,
            is_active=True, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        usuario.set_password(contraseña)
        usuario.save(using=self._db)
        return usuario

    def create_user(self, nombre_usuario, correo, contraseña=None, **extra_fields):
        return self._create_user(nombre_usuario, correo, contraseña, False, False, **extra_fields)

    def create_superuser(self, nombre_usuario, correo, contraseña=None, **extra_fields):
        return self._create_user(nombre_usuario, correo, contraseña, True, True, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre_usuario = models.CharField(max_length=50, unique=True)
    correo = models.EmailField(max_length=50, unique=True)
    primer_nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    objects = UserManager()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'nombre_usuario'
    REQUIRED_FIELDS = ['correo']

    def get_short_name(self):
        return self.nombre_usuario
"""


class SecretarioGeneral(models.Model):
    """
    Indica los usuarios que tiene permisos del nivel de secretario
    general
    """
    usuario = models.ForeignKey(User, models.CASCADE)
