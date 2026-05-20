from django.db import models
from django.contrib.auth.models import User
from encuestas.models import Pregunta, Opcion


class Respuesta(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.CASCADE
    )

    opcion = models.ForeignKey(
        Opcion,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    contenido = models.TextField(
        null=True,
        blank=True
    )

    fecha_respuesta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.pregunta.texto}"