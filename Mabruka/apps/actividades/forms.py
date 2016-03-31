from django import forms
from .models import Encuentro, Foro, Seminario, Panel
# from django.contrib.auth.models import User


class EdicionEncuentroForm(forms.ModelForm):
    """
    Form para la modificación de un Encuentro
    """
    class Meta:
        model = Encuentro
        fields = ["nombre", "fecha_inicio", "fecha_fin", "responsables"]
        widgets = {
            'nombre': forms.TextInput(
                attrs={'type': 'input', 'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(
                attrs={'class': 'form-control'}, format=('%d/%m/%Y')),
            'fecha_fin': forms.DateInput(
                attrs={'class': 'form-control'}, format=('%d/%m/%Y')),
            "responsables": forms.SelectMultiple(
                attrs={
                    'class': 'selectpicker form-control',
                    'data-live-search': "true",
                    'title': "Selecciona los responsables"})
        }


class EdicionForoForm(forms.ModelForm):
    """
    Form para la modificación de un Foro
    """
    class Meta:
        model = Foro
        fields = ["nombre", "nombre_corto", "responsables", "descripcion"]
        widgets = {
            'nombre': forms.TextInput(
                attrs={'type': 'input', 'class': 'form-control'}),
            'nombre_corto': forms.TextInput(
                attrs={'type': 'input', 'class': 'form-control'}),
            "responsables": forms.SelectMultiple(
                attrs={
                    'class': 'selectpicker form-control',
                    'data-live-search': "true",
                    'title': "Selecciona los responsables"}),
            "descripcion": forms.Textarea(
                attrs={'type': 'input', 'class': 'form-control'}
                ),
        }


class EdicionSeminarioForm(forms.ModelForm):
    """
    Form para la modificación de un Seminario
    """
    class Meta:
        model = Seminario
        fields = ["nombre", "responsables"]
        widgets = {
            'nombre': forms.TextInput(
                attrs={'type': 'input', 'class': 'form-control'}),
            "responsables": forms.SelectMultiple(
                attrs={
                    'class': 'selectpicker form-control',
                    'data-live-search': "true",
                    'title': "Selecciona los responsables"}),
        }


class EdicionPanelForm(forms.ModelForm):
    """
    Form para la modificación de un Panel
    """
    class Meta:
        model = Panel
        fields = ["nombre"]
        widgets = {
            'nombre': forms.TextInput(
                attrs={'type': 'input', 'class': 'form-control'}),
        }
