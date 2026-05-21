#from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='encuestas'),
    path('lista/', views.lista_encuestas, name='lista_encuestas'),
    path('crear/', views.crear_encuesta, name='crear_encuesta'),
    path('<int:encuesta_id>/', views.detalle_encuesta, name='detalle_encuesta'),
    path('<int:encuesta_id>/editar/',views.editar_encuesta,name='editar_encuesta'),
]
