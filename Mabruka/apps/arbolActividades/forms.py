from django import forms
from apps.calendario.models import Evento


class ModificacionEventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ["nombre"]
        exclude = []
