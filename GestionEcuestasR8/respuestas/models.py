from django.db import models
from usuarios.models import Usuario
from encuestas.models import Pregunta, Opcion


class Respuesta(models.Model):

    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='respuestas'
    )

    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.CASCADE,
        related_name='respuestas'
    )

    opcion = models.ForeignKey(
        Opcion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='respuestas'
    )

    contenido = models.TextField(
        null=True,
        blank=True
    )

    fecha_respuesta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.usuario} - {self.pregunta}'