from django.shortcuts import render, redirect
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
        'encuestas/detalle_encuesta.html',{'encuesta': encuesta}
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