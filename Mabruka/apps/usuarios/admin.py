from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Usuario
from .forms import UsuarioChangeForm, UsuarioCreationForm


class UsuarioAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('correo', 'password')}),
        ('Información personal', {'fields': ('nombres', 'apellidos')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'fecha_registro')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('correo', 'password1', 'password2')}
        ),
    )
    form = UsuarioChangeForm
    add_form = UsuarioCreationForm
    list_display = ('correo', 'nombres', 'apellidos', 'is_staff')
    search_fields = ('correo', 'nombres', 'apellidos')
    ordering = ('correo',)

admin.site.register(Usuario, UsuarioAdmin)