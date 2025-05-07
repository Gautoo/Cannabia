# gestion_cultivo/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User # Importa el modelo User
from .models import Sala, AreaCultivo, Planta, Genetica

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
        model = Sala
        fields = ['nombre', 'tipo', 'altura', 'largo', 'ancho']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la sala'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Altura en metros', 'step': '0.01'}),
            'largo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Largo en metros', 'step': '0.01'}),
            'ancho': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ancho en metros', 'step': '0.01'}),
        }
        labels = {
            'nombre': 'Nombre de la Sala',
            'tipo': 'Tipo de Sala',
            'altura': 'Altura (metros)',
            'largo': 'Largo (metros)',
            'ancho': 'Ancho (metros)',
        }
        help_texts = {
            'nombre': 'Ingrese un nombre descriptivo para la sala',
            'tipo': 'Seleccione el tipo de sala según su uso',
            'altura': 'Altura máxima disponible en metros',
            'largo': 'Largo total de la sala en metros',
            'ancho': 'Ancho total de la sala en metros',
        }

class AreaCultivoForm(forms.ModelForm):
    class Meta:
        model = AreaCultivo
        fields = ['nombre', 'tipo_cultivo', 'tiene_riego_automatico', 'altura', 'largo', 'ancho']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_cultivo': forms.Select(attrs={'class': 'form-select'}),
            'tiene_riego_automatico': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'largo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'ancho': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }
        labels = {
            'nombre': 'Nombre del Área',
            'tipo_cultivo': 'Tipo de Cultivo',
            'tiene_riego_automatico': '¿Tiene Riego Automático?',
            'altura': 'Altura (metros)',
            'largo': 'Largo (metros)',
            'ancho': 'Ancho (metros)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ya no necesitamos establecer campos como no requeridos ya que no existen

class GeneticaForm(forms.ModelForm):
    class Meta:
        model = Genetica
        fields = ['nombre', 'descripcion', 'thc_estimado', 'cbd_estimado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la genética'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción de la genética'}),
            'thc_estimado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Porcentaje estimado de THC', 'step': '0.01'}),
            'cbd_estimado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Porcentaje estimado de CBD', 'step': '0.01'}),
        }
        labels = {
            'nombre': 'Nombre de la Genética',
            'descripcion': 'Descripción',
            'thc_estimado': 'THC Estimado (%)',
            'cbd_estimado': 'CBD Estimado (%)',
        }
        help_texts = {
            'nombre': 'Ingrese el nombre de la genética',
            'descripcion': 'Descripción detallada de la genética (opcional)',
            'thc_estimado': 'Porcentaje estimado de THC (opcional)',
            'cbd_estimado': 'Porcentaje estimado de CBD (opcional)',
        }

class PlantaForm(forms.ModelForm):
    class Meta:
        model = Planta
        fields = ['nombre_id', 'genetica', 'thc_estimado', 'cbd_estimado', 'fecha_germinacion', 'etapa_actual', 'activa']
        widgets = {
            'nombre_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre o ID de la planta'}),
            'genetica': forms.Select(attrs={'class': 'form-select'}),
            'thc_estimado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Porcentaje estimado de THC', 'step': '0.01'}),
            'cbd_estimado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Porcentaje estimado de CBD', 'step': '0.01'}),
            'fecha_germinacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'etapa_actual': forms.Select(attrs={'class': 'form-select'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre_id': 'Nombre/ID de la Planta',
            'genetica': 'Genética',
            'thc_estimado': 'THC Estimado (%)',
            'cbd_estimado': 'CBD Estimado (%)',
            'fecha_germinacion': 'Fecha de Germinación',
            'etapa_actual': 'Etapa Actual',
            'activa': 'Planta Activa',
        }
        help_texts = {
            'nombre_id': 'Ingrese un nombre o ID único para identificar la planta',
            'genetica': 'Seleccione la genética de la planta',
            'thc_estimado': 'Porcentaje estimado de THC (opcional)',
            'cbd_estimado': 'Porcentaje estimado de CBD (opcional)',
            'fecha_germinacion': 'Fecha en que germinó la semilla (opcional)',
            'etapa_actual': 'Etapa actual del ciclo de vida de la planta',
            'activa': 'Indica si la planta está activa o ha sido cosechada/descartada',
        }