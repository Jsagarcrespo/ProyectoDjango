from django import forms
from .models import Respuesta


class RespuestaForm(forms.ModelForm):

    class Meta:
        model = Respuesta
        fields = [
            'usuario',
            'opcion',
            'contenido',
        ]

        widgets = {
            'contenido': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Escribe aqui la respuesta...'
                }
            )
        }

    ## Argumentos normales = *args
    ## Argumentos con nombre = **kwargs
    def __init__(self, *args, **kwargs):

        pregunta = kwargs.pop('pregunta', None)

        super().__init__(*args, **kwargs)

        if pregunta is not None:

            # Guardamos la pregunta en el formulario para poder usarla si hace falta
            self.pregunta = pregunta

            # Si la encuesta tiene destinatarios, solo dejamos elegir esos usuarios
            if pregunta.encuesta.destinatarios.exists():
                self.fields['usuario'].queryset = pregunta.encuesta.destinatarios.all()

            # Si la pregunta tiene opciones, solo mostramos sus opciones
            self.fields['opcion'].queryset = pregunta.opciones.all()

        # No obligamos siempre a elegir opcion porque las preguntas de texto no tienen opcion.
        self.fields['opcion'].required = False

        # No obligamos siempre a contenido porque las preguntas múltiples usarán opcion.
        self.fields['contenido'].required = False