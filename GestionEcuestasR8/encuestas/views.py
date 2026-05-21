from django.shortcuts import render, redirect
from .models import Encuesta
from .forms import EncuestaForm

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