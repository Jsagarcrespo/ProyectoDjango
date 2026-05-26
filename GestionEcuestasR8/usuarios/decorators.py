from functools import wraps
from django.shortcuts import redirect


def admin_required(view_func):
    """
    Decorador sencillo para proteger las páginas de administración propias del proyecto.

    - Si no hay usuario logueado, manda al login.
    - Si el usuario está logueado pero NO es admin/staff, manda a sus encuestas.
    - Si es admin/staff, le deja entrar.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login_usuario')

        if not request.user.is_staff:
            return redirect('mis_encuestas')

        return view_func(request, *args, **kwargs)

    return wrapper
