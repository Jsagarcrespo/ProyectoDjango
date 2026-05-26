from django.shortcuts import render, redirect, get_object_or_404
from .models import Encuesta, Pregunta, Opcion
from .forms import EncuestaForm

from .models import Pregunta
from .forms import PreguntaForm

from .models import Opcion
from .forms import OpcionForm

from datetime import date

from usuarios.decorators import admin_required


def index(request):
   ## Va a ser la primera pagina del proyecto, verificamos si hay login. 
   ## El usuario puede ser: Admin o Normal
   ## Si es admin ira al panel de administrador. Si es usuairo normal vera sus encuestas

    if not request.user.is_authenticated:
        return redirect('login_usuario')

    if request.user.is_staff:
        return render(request, 'encuestas/encuesta.html')

    return redirect('mis_encuestas')


@admin_required
def lista_encuestas(request):
    encuestas = Encuesta.objects.all().order_by('fecha_cierre', 'titulo')

    # Revisamos el cierre automático al entrar al listado.
    for encuesta in encuestas:
        update_cierre(encuesta)

    return render(
        request,
        'encuestas/lista_encuestas.html',
        {
            'encuestas': encuestas
        }
    )


@admin_required
def crear_encuesta(request):
    if request.method == 'POST':
        formulario = EncuestaForm(request.POST)

        if formulario.is_valid():
            formulario.save()
            return redirect('lista_encuestas')

    else:
        formulario = EncuestaForm()

    return render(
        request,
        'encuestas/crear_encuesta.html',
        {
            'formulario': formulario
        }
    )


@admin_required
def detalle_encuesta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)

    update_cierre(encuesta)

    return render(
        request,
        'encuestas/detalle_encuesta.html',
        {
            'encuesta': encuesta
        }
    )


@admin_required
def editar_encuesta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)

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


@admin_required
def eliminar_encuesta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)

    if request.method == 'POST':
        encuesta.delete()
        return redirect('lista_encuestas')

    return render(
        request,
        'encuestas/eliminar_encuesta.html',
        {
            'encuesta': encuesta
        }
    )


@admin_required
def crear_pregunta(request, encuesta_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)

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


@admin_required
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

    ## Cargamos el html y enviamos variable al template
    ## Ahora en el html cuando vea {{ objeto.campo }} pondra los datos de la BBDD
    return render(
        request,
        'encuestas/detalle_pregunta.html',
        {
            'encuesta': encuesta,
            'pregunta': pregunta
        }
    )


@admin_required
def editar_pregunta(request, encuesta_id, pregunta_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)

    pregunta = get_object_or_404(
        Pregunta,
        id=pregunta_id,
        encuesta=encuesta
    )

    if request.method == 'POST':

        ## Se crea formulario con los datos enviados
        ## Con instance le indicamos que modifique la pregunta existente y no genere ninguna nueva
        formulario = PreguntaForm(
            request.POST,
            instance=pregunta
        )

        ## Comprovacion que el formulario esta bien
        if formulario.is_valid():
            formulario.save()

            ## Una vez guardado volvemos a detalle
            return redirect(
                'detalle_pregunta',
                encuesta_id=encuesta.id,
                pregunta_id=pregunta.id
            )

    ## Si se edita por primera vez
    else:

        ## El usuario solo esta entrando a la pagina
        ## Crea el formulario con los datos actuales de la pregunta
        formulario = PreguntaForm(
            instance=pregunta
        )

    return render(
        request,
        'encuestas/editar_pregunta.html',
        {
            'formulario': formulario,
            'encuesta': encuesta,
            'pregunta': pregunta,
        }
    )


@admin_required
def eliminar_pregunta(request, encuesta_id, pregunta_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)

    pregunta = get_object_or_404(
        Pregunta,
        id=pregunta_id,
        encuesta=encuesta
    )

    if request.method == 'POST':
        pregunta.delete()

        return redirect(
            'detalle_encuesta',
            encuesta_id=encuesta.id
        )

    return render(
        request,
        'encuestas/eliminar_pregunta.html',
        {
            'encuesta': encuesta,
            'pregunta': pregunta,
        }
    )



## Opciones

@admin_required
def crear_opcion(request, encuesta_id, pregunta_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)

    pregunta = get_object_or_404(
        Pregunta,
        id=pregunta_id,
        encuesta=encuesta
    )

    if request.method == 'POST':
        formulario = OpcionForm(request.POST)

        if formulario.is_valid():

            ## Creamos el objeto pero sin guardarlo
            opcion = formulario.save(commit=False)
            ## con esto referenciamos a la pregunta que pertenece
            opcion.pregunta = pregunta
            opcion.save()

            return redirect(
                'detalle_opcion',
                encuesta_id=encuesta.id,
                pregunta_id=pregunta.id,
                opcion_id=opcion.id
            )

    else:
        formulario = OpcionForm()

    return render(
        request,
        'encuestas/crear_opcion.html',
        {
            'formulario': formulario,
            'encuesta': encuesta,
            'pregunta': pregunta
        }
    )


@admin_required
def detalle_opcion(request, encuesta_id, pregunta_id, opcion_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)

    pregunta = get_object_or_404(
        Pregunta,
        id=pregunta_id,
        encuesta=encuesta
    )

    opcion = get_object_or_404(
        Opcion,
        id=opcion_id,
        pregunta=pregunta
    )

    return render(
        request,
        'encuestas/detalle_opcion.html',
        {
            'encuesta': encuesta,
            'pregunta': pregunta,
            'opcion': opcion
        }
    )


@admin_required
def editar_opcion(request, encuesta_id, pregunta_id, opcion_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)

    pregunta = get_object_or_404(
        Pregunta,
        id=pregunta_id,
        encuesta=encuesta
    )

    opcion = get_object_or_404(
        Opcion,
        id=opcion_id,
        pregunta=pregunta
    )

    if request.method == 'POST':
        formulario = OpcionForm(
            request.POST,
            instance=opcion
        )

        if formulario.is_valid():
            formulario.save()

            return redirect(
                'detalle_opcion',
                encuesta_id=encuesta.id,
                pregunta_id=pregunta.id,
                opcion_id=opcion.id
            )

    else:
        formulario = OpcionForm(
            instance=opcion
        )

    return render(
        request,
        'encuestas/editar_opcion.html',
        {
            'formulario': formulario,
            'encuesta': encuesta,
            'pregunta': pregunta,
            'opcion': opcion
        }
    )


@admin_required
def eliminar_opcion(request, encuesta_id, pregunta_id, opcion_id):
    encuesta = get_object_or_404(Encuesta, id=encuesta_id)

    pregunta = get_object_or_404(
        Pregunta,
        id=pregunta_id,
        encuesta=encuesta
    )

    opcion = get_object_or_404(
        Opcion,
        id=opcion_id,
        pregunta=pregunta
    )

    if request.method == 'POST':
        opcion.delete()

        return redirect(
            'detalle_pregunta',
            encuesta_id=encuesta.id,
            pregunta_id=pregunta.id
        )

    return render(
        request,
        'encuestas/eliminar_opcion.html',
        {
            'encuesta': encuesta,
            'pregunta': pregunta,
            'opcion': opcion
        }
    )


def update_cierre(encuesta):
    ## Cierra automaticamente si pasa la fecha de cierre
    if encuesta.fecha_cierre is not None:
        if encuesta.fecha_cierre < date.today() and encuesta.estado != 'cerrada':
            encuesta.estado = 'cerrada'
            encuesta.save()
