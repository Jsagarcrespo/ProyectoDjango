from django.urls import path
from . import views_api


urlpatterns = [
    path(
        'encuestas/',
        views_api.api_lista_encuestas,
        name='api_lista_encuestas'
    ),

    path(
        'encuestas/<int:encuesta_id>/',
        views_api.api_detalle_encuesta,
        name='api_detalle_encuesta'
    ),
]
