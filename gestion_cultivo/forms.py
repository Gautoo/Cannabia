# gestion_cultivo/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User # Importa el modelo User
from .models import Sala

class RegistroUsuarioForm(UserCreationForm):
    # UserCreationForm ya incluye campos para username y passwords
    # Vamos a añadir campos para email, nombre y apellido, y hacer el email requerido.
    email = forms.EmailField(
        required=True,
        help_text='Requerido. Por favor, introduce una dirección de email válida.'
    )
    first_name = forms.CharField(required=False, label="Nombre") # Hacemos el nombre opcional
    last_name = forms.CharField(required=False, label="Apellido") # Hacemos el apellido opcional

    class Meta(UserCreationForm.Meta):
        model = User # El modelo sobre el que se basa este formulario
        # Los campos que se mostrarán en el formulario.
        # 'username' y los campos de contraseña vienen de UserCreationForm.
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')
        # Alternativamente, para un orden específico y solo los campos que quieres:
        # fields = ('username', 'email', 'first_name', 'last_name')
        # Pero recuerda que UserCreationForm maneja los campos de contraseña, así que la primera opción es mejor.

    def clean_email(self):
        # Validación personalizada para asegurar que el email no esté ya en uso.
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists(): # iexact para case-insensitive
            raise forms.ValidationError("Ya existe una cuenta registrada con esta dirección de email.")
        return email
    
    # NUEVO FORMULARIO para crear y editar Salas
class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala # El modelo en el que se basa este formulario
        fields = ['nombre', 'descripcion'] # Los campos del modelo que el usuario podrá editar
        # Personalización de widgets (opcional, pero útil para la apariencia)
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Sala de Vegetación A'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Pequeña descripción de la sala (opcional)'}),
        }
        labels = {
            'nombre': 'Nombre de la Sala',
            'descripcion': 'Descripción (Opcional)',
        }
        help_texts = {
            'nombre': 'Un nombre descriptivo para identificar esta sala de cultivo.',
        }