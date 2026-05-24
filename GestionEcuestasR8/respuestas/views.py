from django.shortcuts import render, redirect, get_object_or_404

from .models import Respuesta
from .forms import RespuestaForm

from encuestas.models import Encuesta, Pregunta
from usuarios.models import Usuario

from django.db.models import Count
# Create your views here.

## Comprobar si una pregunta tiene opcion multiple
def es_pregunta_multiple(pregunta):
    return pregunta.tipo_pregunta == 'multiple'


def lista_respuestas(request):

    # Sacamos respusetas con sus relaciones
    respuestas = Respuesta.objects.select_related(
        'usuario',
        'pregunta',
        'pregunta__encuesta', ## doble guion bajo para acceder a relaciones en modelos
        'opcion'
    ).all().order_by('-fecha_respuesta') ## Ordenar de forma descendente

    return render(
        request,
        'respuestas/lista_respuestas.html',
        {
            'respuestas': respuestas
        }
    )


def detalle_respuesta(request, encuesta_id, pregunta_id, respuesta_id):

    encuesta = get_object_or_404(Encuesta, id=encuesta_id)

    pregunta = get_object_or_404(
        Pregunta,
        id=pregunta_id,
        encuesta=encuesta
    )

    respuesta = get_object_or_404(
        Respuesta,
        id=respuesta_id,
        pregunta=pregunta
    )

    return render(
        request,
        'respuestas/detalle_respuesta.html',
        {
            'encuesta': encuesta,
            'pregunta': pregunta,
            'respuesta': respuesta
        }
    )


def crear_respuesta(request, encuesta_id, pregunta_id):

    encuesta = get_object_or_404(Encuesta, id=encuesta_id)

    pregunta = get_object_or_404(
        Pregunta,
        id=pregunta_id,
        encuesta=encuesta
    )

    if request.method == 'POST':

        formulario = RespuestaForm(
            request.POST,
            pregunta=pregunta
        )

        if formulario.is_valid():

            ## para ver si hay errores manuales
            hay_error = False

            if es_pregunta_multiple(pregunta):

                ## optenemos los datos ya validados
                opcion = formulario.cleaned_data.get('opcion')

                ## si no se elige opcion saltara el error
                if opcion is None:
                    formulario.add_error(
                        'opcion',
                        'Debes elegir una opcion para esta pregunta.'
                    )
                    hay_error = True

            else:

                contenido = formulario.cleaned_data.get('contenido')

                if not contenido:
                    formulario.add_error(
                        'contenido',
                        'Debes escribir una respuesta de texto.'
                    )
                    hay_error = True

            if not hay_error:

                respuesta = formulario.save(commit=False)

                # La pregunta no esta en el formulario porque viene indicada por la URL. Se lo asignamos manualmente
                respuesta.pregunta = pregunta

                # Si es de opcion multiple, guardamos también el texto de la opcion en contenido.
                if es_pregunta_multiple(pregunta) and respuesta.opcion:
                    respuesta.contenido = respuesta.opcion.texto

                respuesta.save()

                return redirect(
                    'detalle_respuesta',
                    encuesta_id=encuesta.id,
                    pregunta_id=pregunta.id,
                    respuesta_id=respuesta.id
                )

    else:

        formulario = RespuestaForm(
            pregunta=pregunta
        )

    return render(
        request,
        'respuestas/formulario_respuesta.html',
        {
            'formulario': formulario,
            'encuesta': encuesta,
            'pregunta': pregunta,
            'modo': 'crear'
        }
    )


def editar_respuesta(request, encuesta_id, pregunta_id, respuesta_id):

    encuesta = get_object_or_404(Encuesta, id=encuesta_id)

    pregunta = get_object_or_404(
        Pregunta,
        id=pregunta_id,
        encuesta=encuesta
    )

    respuesta = get_object_or_404(
        Respuesta,
        id=respuesta_id,
        pregunta=pregunta
    )

    if request.method == 'POST':

        formulario = RespuestaForm(
            request.POST,
            instance=respuesta,
            pregunta=pregunta
        )

        if formulario.is_valid():

            hay_error = False

            if es_pregunta_multiple(pregunta):

                opcion = formulario.cleaned_data.get('opcion')

                if opcion is None:
                    formulario.add_error(
                        'opcion',
                        'Debes elegir una opcion para esta pregunta.'
                    )
                    hay_error = True

            else:

                contenido = formulario.cleaned_data.get('contenido')

                if not contenido:
                    formulario.add_error(
                        'contenido',
                        'Debes escribir una respuesta de texto.'
                    )
                    hay_error = True

            if not hay_error:

                respuesta_editada = formulario.save(commit=False)
                respuesta_editada.pregunta = pregunta

                if es_pregunta_multiple(pregunta) and respuesta_editada.opcion:
                    respuesta_editada.contenido = respuesta_editada.opcion.texto

                respuesta_editada.save()

                return redirect(
                    'detalle_respuesta',
                    encuesta_id=encuesta.id,
                    pregunta_id=pregunta.id,
                    respuesta_id=respuesta.id
                )

    else:

        formulario = RespuestaForm(
            instance=respuesta,
            pregunta=pregunta
        )

    return render(
        request,
        'respuestas/formulario_respuesta.html',
        {
            'formulario': formulario,
            'encuesta': encuesta,
            'pregunta': pregunta,
            'respuesta': respuesta,
            'modo': 'editar'
        }
    )


def eliminar_respuesta(request, encuesta_id, pregunta_id, respuesta_id):

    encuesta = get_object_or_404(Encuesta, id=encuesta_id)

    pregunta = get_object_or_404(
        Pregunta,
        id=pregunta_id,
        encuesta=encuesta
    )

    respuesta = get_object_or_404(
        Respuesta,
        id=respuesta_id,
        pregunta=pregunta
    )

    if request.method == 'POST':

        respuesta.delete()

        return redirect(
            'resp_x_enc',
            encuesta_id=encuesta.id
        )

    return render(
        request,
        'respuestas/eliminar_respuesta.html',
        {
            'encuesta': encuesta,
            'pregunta': pregunta,
            'respuesta': respuesta
        }
    )


def resp_x_enc(request, encuesta_id):

    encuesta = get_object_or_404(Encuesta, id=encuesta_id)

    respuestas = Respuesta.objects.filter(
        pregunta__encuesta=encuesta
    ).select_related(
        'usuario',
        'pregunta',
        'opcion'
    ).order_by('pregunta__id', 'usuario__apellidos')

    return render(
        request,
        'respuestas/resp_x_enc.html',
        {
            'encuesta': encuesta,
            'respuestas': respuestas
        }
    )


def resp_x_usu(request, usuario_id):

    usuario = get_object_or_404(Usuario, id=usuario_id)

    respuestas = Respuesta.objects.filter(
        usuario=usuario
    ).select_related(
        'pregunta',
        'pregunta__encuesta',
        'opcion'
    ).order_by('pregunta__encuesta__titulo', 'pregunta__id')

    return render(
        request,
        'respuestas/resp_x_usu.html',
        {
            'usuario': usuario,
            'respuestas': respuestas
        }
    )


def resultados_encuesta(request, encuesta_id):

    encuesta = get_object_or_404(
        Encuesta,
        id=encuesta_id
    )

    ## Filtramos las preguntas que solo pertencen a esta encuesta
    preguntas = Pregunta.objects.filter(
        encuesta=encuesta
    )

    ## donde meteremos los resultado
    resultados = []

    for pregunta in preguntas:

        if es_pregunta_multiple(pregunta):

            conteos = Respuesta.objects.filter( ## buscamos respuestas
                pregunta=pregunta, ## solo respuestas de la pregunta
                opcion__isnull=False
            ).values(
                'opcion__texto'
            ).annotate(
                total=Count('id') ## contamos cuantas veces aparece cada opcion
            ).order_by(
                'opcion__texto' ## ordenado alfabeticamente
            )

            resultados.append({ ## añadimos a la lista vacia
                'pregunta': pregunta,
                'tipo': 'multiple',
                'conteos': conteos
            })

        else:

            ## Busca respuestas de esa pregunta
            respuestas_texto = Respuesta.objects.filter(
                pregunta=pregunta
            ).select_related( ## traemos los datos del usuario
                'usuario'
            ).order_by(
                'fecha_respuesta'
            )

            resultados.append({
                'pregunta': pregunta,
                'tipo': 'texto',
                'respuestas_texto': respuestas_texto
            })

    return render(
        request,
        'respuestas/resultados_encuesta.html',
        {
            'encuesta': encuesta,
            'resultados': resultados
        }
    )