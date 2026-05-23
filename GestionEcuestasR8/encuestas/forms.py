from django import forms
from .models import Encuesta
from .models import Pregunta
from .models import Opcion

class EncuestaForm(forms.ModelForm):
    
    class Meta: 

        model = Encuesta
        fields = ['titulo', 'descripcion','estado', 'fecha_cierre', 'destinatarios']

    widgets = {
            'fecha_cierre': forms.DateInput(attrs={'type': 'date'}),
            'destinatarios': forms.CheckboxSelectMultiple(),
        }


class PreguntaForm(forms.ModelForm):

    class Meta:

        model = Pregunta

        fields = [
            'texto','tipo_pregunta','obligatoriedad'
        ]


class OpcionForm(forms.ModelForm):

    class Meta: 

        model = Opcion

        fields = [
            'texto'
        ]