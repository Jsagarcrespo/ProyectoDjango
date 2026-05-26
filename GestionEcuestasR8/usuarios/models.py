from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    # Usuario de login de Django asociado a este usuario del reto.
    # La contraseña NO se guarda aquí: Django la guarda cifrada/hasheada en auth.User.
    auth_user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='perfil_usuario'
    )

    dni = models.CharField(max_length=9, unique=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
