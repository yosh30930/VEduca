from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario
# Register your models here.


class UserAdmin(UserAdmin):
    fieldsets = (
        ('Usuario', {'fields': ('nombre_usuario', 'password')}),
        ('Persona Info', {'fields': ('primer_nombre', 'apellido', 'correo')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions')}),
    )
    list_display = ('nombre_usuario','correo', 'password',)
    ordering = ('nombre_usuario',)
admin.site.register(Usuario, UserAdmin)
