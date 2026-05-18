from django.db import models

# Create your models here.
class Encuesta(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    
    
class Pregunta(models.Model):
    encuesta = models.ForeignKey(
        Encuesta, 
        on_delete=models.CASCADE, 
        related_name='preguntas'
    )

    texto = models.CharField(max_length=300)

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
