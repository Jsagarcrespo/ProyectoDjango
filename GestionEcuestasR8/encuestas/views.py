from django.shortcuts import render, redirect, get_object_or_404
from .models import Encuesta
from .forms import EncuestaForm

from .models import Pregunta
from .forms import PreguntaForm

# Create your views here.
def index(request):
    return render(request, 'encuestas/encuesta.html')


def lista_encuestas(request):
    encuestas = Encuesta.objects.all()

    print(encuestas)

    return render(request, 'encuestas/lista_encuestas.html', {'encuestas': encuestas})


def crear_encuesta(request):

    if request.method == 'POST':

        formulario = EncuestaForm(request.POST)

        if formulario.is_valid():

            formulario.save()

            return redirect('lista_encuestas')

    else:

        formulario = EncuestaForm()

    return render(
        request,'encuestas/crear_encuesta.html',{'formulario': formulario}

    )


def detalle_encuesta(request, encuesta_id):

    encuesta = Encuesta.objects.get(id=encuesta_id) ## Devolvemos solo un objeto

    return render(
        request,
        'encuestas/detalle_encuesta.html',{'encuesta': encuesta} ## envia el objeto al HTML/template
    )


def editar_encuesta(request, encuesta_id):

    encuesta = Encuesta.objects.get(id=encuesta_id)

    if request.method == 'POST':

        formulario = EncuestaForm(
            request.POST,
            instance=encuesta
        )

        if formulario.is_valid():

            formulario.save()

            return redirect(
                'detalle_encuesta',
                encuesta_id=encuesta.id
            )

    else:

        formulario = EncuestaForm(
            instance=encuesta
        )

    return render(
        request,
        'encuestas/editar_encuesta.html',
        {
            'formulario': formulario,
            'encuesta': encuesta
        }
    )


def eliminar_encuesta(request, encuesta_id):

    encuesta = Encuesta.objects.get(id=encuesta_id)

    if request.method == 'POST':

        encuesta.delete()

        return redirect('lista_encuestas')

    return render(
        request,'encuestas/eliminar_encuesta.html',{'encuesta': encuesta}
    )



## PREGUNTAS
def crear_pregunta(request, encuesta_id):

    encuesta = Encuesta.objects.get(id=encuesta_id)

    if request.method == 'POST':

        formulario = PreguntaForm(request.POST)

        if formulario.is_valid():

            pregunta = formulario.save(commit=False)

            pregunta.encuesta = encuesta

            pregunta.save()

            return redirect(
                'detalle_encuesta',
                encuesta_id=encuesta.id
            )

    else:

        formulario = PreguntaForm()

    return render(
        request,
        'encuestas/crear_pregunta.html',
        {
            'formulario': formulario,
            'encuesta': encuesta
        }
    )


def detalle_pregunta(request, encuesta_id, pregunta_id):
    ## Busca en la BBDD mediante el id (sql: where id = id)
    ## Si no existe devuelve error 404
    ## id viene desde la url
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)

    ## sql: where id = pregunta_id and encuesta_id = encuesta.id, con esto nos aseguramos que la pregunta pertenece a la encuesta
    pregunta = get_object_or_404(
        Pregunta,
        id=pregunta_id,
        encuesta=encuesta
    )

    return render(
        request,
        'encuestas/detalle_pregunta.html',
        {
            'encuesta': encuesta,
            'pregunta': pregunta
        }
    )