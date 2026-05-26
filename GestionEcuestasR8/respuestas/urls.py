from django.urls import path
from . import views


urlpatterns = [
    path('', views.lista_respuestas, name='lista_respuestas'),
    path('encuesta/<int:encuesta_id>/', views.resp_x_enc, name='resp_x_enc'),
    path('usuario/<int:usuario_id>/', views.resp_x_usu, name='resp_x_usu'),

    # Ruta para usuarios normales: responder una encuesta asignada.
    path(
        'encuesta/<int:encuesta_id>/responder/',
        views.responder_encuesta_usuario,
        name='responder_encuesta_usuario'
    ),

    path(
        'encuesta/<int:encuesta_id>/pregunta/<int:pregunta_id>/crear/',
        views.crear_respuesta,
        name='crear_respuesta'
    ),

    path(
        'encuesta/<int:encuesta_id>/pregunta/<int:pregunta_id>/respuesta/<int:respuesta_id>/',
        views.detalle_respuesta,
        name='detalle_respuesta'
    ),

    path(
        'encuesta/<int:encuesta_id>/pregunta/<int:pregunta_id>/respuesta/<int:respuesta_id>/editar/',
        views.editar_respuesta,
        name='editar_respuesta'
    ),

    path(
        'encuesta/<int:encuesta_id>/pregunta/<int:pregunta_id>/respuesta/<int:respuesta_id>/eliminar/',
        views.eliminar_respuesta,
        name='eliminar_respuesta'
    ),

    path(
        'encuesta/<int:encuesta_id>/resultados/',
        views.resultados_encuesta,
        name='resultados_encuesta'
    ),
]
