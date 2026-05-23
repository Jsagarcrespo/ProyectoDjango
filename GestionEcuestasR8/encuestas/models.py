from django.db import models
from usuarios.models import Usuario

# Create your models here.
class Encuesta(models.Model):

    ESTADOS = [
        ('borrador', 'Borrador'),
        ('abierta', 'Abierta'),
        ('cerrada', 'Cerrada'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='borrador'
    )

    fecha_cierre = models.DateField(
        null=True,
        blank=True
    )

    destinatarios = models.ManyToManyField(
        Usuario,
        blank=True,
        related_name='encuestas_destinatarias'
    )

    def __str__(self):
        return self.titulo
    
    
class Pregunta(models.Model):

    TIPO_PREGUNTA = [
        ('texto', 'texto libre'), 
        ('multiple', 'Opcion multiple')
    ]

    encuesta = models.ForeignKey(
        Encuesta, 
        on_delete=models.CASCADE, 
        related_name='preguntas'
    )

    texto = models.CharField(max_length=300)

    tipo_pregunta = models.CharField(
        max_length=20,
        choices=TIPO_PREGUNTA, 
        default='texto'
    )

    obligatoriedad = models.BooleanField(default=False)

    def __str__(self):
        return self.texto
    

class Opcion(models.Model):
    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.CASCADE, 
        related_name='opciones'
        )
    
    texto = models.CharField(max_length=200)

    def __str__(self):
        return self.texto
