from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario
from .forms import UsuarioForm

# Create your views here.

def lista_usuarios(request):

    ## Ordenamos primero por apellidos y despues por nombre
    usuarios = Usuario.objects.all().order_by('apellidos', 'nombre')

    return render(
        request,
        'usuarios/lista_usuarios.html',
        {
            'usuarios': usuarios
        }
    )

def crear_usuario(request):

    if request.method == 'POST':

        formulario = UsuarioForm(request.POST)

        if formulario.is_valid():

            usuario = formulario.save()

            return redirect(
                'detalle_usuario',
                usuario_id=usuario.id
            )

    else:

        formulario = UsuarioForm()

    return render(
        request,
        'usuarios/crear_usuario.html',
        {
            'formulario': formulario
        }
    )


def detalle_usuario(request, usuario_id):

    usuario = get_object_or_404(
        Usuario,
        id=usuario_id
    )

    return render(
        request,
        'usuarios/detalle_usuario.html',
        {
            'usuario': usuario
        }
    )


def editar_usuario(request, usuario_id):

    usuario = get_object_or_404(
        Usuario,
        id=usuario_id
    )

    if request.method == 'POST':

        formulario = UsuarioForm(
            request.POST,
            instance=usuario
        )

        if formulario.is_valid():

            formulario.save()

            return redirect(
                'detalle_usuario',
                usuario_id=usuario.id
            )

    else:

        formulario = UsuarioForm(
            instance=usuario
        )

    return render(
        request,
        'usuarios/editar_usuario.html',
        {
            'formulario': formulario,
            'usuario': usuario
        }
    )


def eliminar_usuario(request, usuario_id):

    usuario = get_object_or_404(
        Usuario,
        id=usuario_id
    )

    if request.method == 'POST':

        usuario.delete()

        return redirect('lista_usuarios')

    return render(
        request,
        'usuarios/eliminar_usuario.html',
        {
            'usuario': usuario
        }
    )