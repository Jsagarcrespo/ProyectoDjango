from django.contrib import admin

from .models import Encuesta, Pregunta, Opcion

# Register your models here.

admin.site.register(Encuesta)
admin.site.register(Pregunta)
admin.site.register(Opcion)
