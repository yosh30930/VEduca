from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django import forms

from apps.usuarios.models import Persona


class UsuarioResetForm(PasswordResetForm):
    """
    Forma para iniciar el reestablecimiento de contraseña
    """

    def get_users(self, email):
        active_users = get_user_model()._default_manager.filter(
            email=email, is_active=True)
        return (u for u in active_users if u.has_usable_password())

    def clean_email(self):
        correo = self.cleaned_data['email']
        usuario = Persona.objects.filter(correo=correo).first()
        if usuario:
            return super(UsuarioResetForm, self).clean_email()
        usuario = Persona.objects.filter(correo_secundario=correo).first()
        if usuario:
            self.cleaned_data['email'] = usuario.correo_secundario
            return super(UsuarioResetForm, self).clean_email()
        raise forms.ValidationError(
            "Este correo no está registrado. Verifique y vuelva a intentar.")
