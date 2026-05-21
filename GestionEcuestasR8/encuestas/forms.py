from django import forms
from .models import Encuesta

class EncuestaForm(forms.ModelForm):
    
    class Meta: 

        model = Encuesta
        fields = ['titulo', 'descripcion']