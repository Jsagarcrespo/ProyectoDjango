from django import forms
from django.contrib.auth.models import User
from .models import Usuario


class UsuarioForm(forms.ModelForm):
    # Estos campos NO pertenecen directamente a Usuario.
    # Sirven para crear o actualizar el User de Django que permite iniciar sesión.
    username = forms.CharField(
        label='Nombre de usuario para login',
        max_length=150
    )

    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        required=False,
        help_text='Al crear un usuario es obligatoria. Al editar, déjala vacía si no quieres cambiarla.'
    )

    class Meta:
        model = Usuario
        fields = [
            'dni',
            'nombre',
            'apellidos',
            'email',
            'telefono',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si estamos editando un Usuario que ya tiene cuenta de login,
        # rellenamos el username actual para que se vea en el formulario.
        if self.instance and self.instance.pk and self.instance.auth_user:
            self.fields['username'].initial = self.instance.auth_user.username
        else:
            # Si estamos creando un usuario nuevo, la contraseña sí debe ser obligatoria.
            self.fields['password'].required = True

    def clean_username(self):
        username = self.cleaned_data['username']

        consulta = User.objects.filter(username=username)

        # Si estamos editando, permitimos mantener el mismo username del usuario actual.
        if self.instance and self.instance.pk and self.instance.auth_user:
            consulta = consulta.exclude(id=self.instance.auth_user.id)

        if consulta.exists():
            raise forms.ValidationError('Ya existe un usuario con ese nombre de login.')

        return username
