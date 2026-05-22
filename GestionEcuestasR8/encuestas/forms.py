from django import forms
from .models import Encuesta
from .models import Pregunta

class EncuestaForm(forms.ModelForm):
    
    class Meta: 

        model = Encuesta
        fields = ['titulo', 'descripcion']


class PreguntaForm(forms.ModelForm):

    class Meta:

        model = Pregunta

        fields = [
            'texto','tipo_pregunta','obligatoriedad'
        ]