from django.shortcuts import render
from .models import Encuesta

# Create your views here.
def index(request):
    return render(request, 'encuestas/encuesta.html')


def lista_encuestas(request):
    encuestas = Encuesta.objects.all()

    print(encuestas)

    return render(request, 'encuestas/lista_encuestas.html', {'encuestas': encuestas})
