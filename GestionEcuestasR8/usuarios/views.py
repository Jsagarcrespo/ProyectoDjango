from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Usuario
from .forms import UsuarioForm
from .decorators import admin_required


def login_usuario(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('encuestas')
        return redirect('mis_encuestas')

    if request.method == 'POST':
        formulario = AuthenticationForm(
            request,
            data=request.POST
        )

        if formulario.is_valid():
            usuario_login = formulario.get_user()
            login(request, usuario_login)

            if usuario_login.is_staff:
                return redirect('encuestas')

            return redirect('mis_encuestas')

    else:
        formulario = AuthenticationForm()

    return render(
        request,
        'usuarios/login.html',
        {
            'formulario': formulario
        }
    )


@login_required(login_url='login_usuario')
def logout_usuario(request):
    logout(request)
    return redirect('login_usuario')


@login_required(login_url='login_usuario')
def mis_encuestas(request):
    """
    Pagina principal del usuario normal.

    El usuario normal no ve todos los CRUD.
    Solo ve las encuestas en las que aparece como destinatario.
    """
    if request.user.is_staff:
        return redirect('encuestas')

    try:
        usuario = request.user.perfil_usuario
    except Usuario.DoesNotExist:
        return render(request, 'usuarios/sin_perfil.html')

    encuestas = usuario.encuestas_destinatarias.all().order_by('fecha_cierre', 'titulo')

    return render(
        request,
        'usuarios/mis_encuestas.html',
        {
            'usuario': usuario,
            'encuestas': encuestas
        }
    )


@admin_required
def lista_usuarios(request):
    usuarios = Usuario.objects.all().order_by('apellidos', 'nombre')

    return render(
        request,
        'usuarios/lista_usuarios.html',
        {
            'usuarios': usuarios
        }
    )


@admin_required
def crear_usuario(request):
    """
    Crea dos cosas:
    1. Un User de Django para poder iniciar sesión.
    2. Un Usuario del reto para poder responder encuestas.
    """
    if request.method == 'POST':
        formulario = UsuarioForm(request.POST)

        if formulario.is_valid():
            auth_user = User.objects.create_user(
                username=formulario.cleaned_data['username'],
                password=formulario.cleaned_data['password'],
                email=formulario.cleaned_data['email'],
                first_name=formulario.cleaned_data['nombre'],
                last_name=formulario.cleaned_data['apellidos']
            )

            usuario = formulario.save(commit=False)
            usuario.auth_user = auth_user
            usuario.save()

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


@admin_required
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


@admin_required
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
            usuario_editado = formulario.save(commit=False)

            # Si ya tiene cuenta de login, la actualizamos.
            if usuario_editado.auth_user:
                auth_user = usuario_editado.auth_user
                auth_user.username = formulario.cleaned_data['username']
                auth_user.email = formulario.cleaned_data['email']
                auth_user.first_name = formulario.cleaned_data['nombre']
                auth_user.last_name = formulario.cleaned_data['apellidos']

                if formulario.cleaned_data['password']:
                    auth_user.set_password(formulario.cleaned_data['password'])

                auth_user.save()

            # Si no tenía cuenta de login, la creamos.
            else:
                auth_user = User.objects.create_user(
                    username=formulario.cleaned_data['username'],
                    password=formulario.cleaned_data['password'],
                    email=formulario.cleaned_data['email'],
                    first_name=formulario.cleaned_data['nombre'],
                    last_name=formulario.cleaned_data['apellidos']
                )
                usuario_editado.auth_user = auth_user

            usuario_editado.save()

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


@admin_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(
        Usuario,
        id=usuario_id
    )

    if request.method == 'POST':
        auth_user = usuario.auth_user
        usuario.delete()

        # Borramos también la cuenta de login asociada si existe.
        if auth_user:
            auth_user.delete()

        return redirect('lista_usuarios')

    return render(
        request,
        'usuarios/eliminar_usuario.html',
        {
            'usuario': usuario
        }
    )
