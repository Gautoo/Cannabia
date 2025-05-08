# gestion_cultivo/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User # Importa el modelo User
from .models import Sala, AreaCultivo, Planta, Genetica, Semilla
from django.utils import timezone

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
        fields = ['nombre', 'descripcion', 'tipo', 'altura', 'largo', 'ancho']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'largo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ancho': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'nombre': 'Nombre de la Sala',
            'descripcion': 'Descripción',
            'tipo': 'Tipo de Sala',
            'altura': 'Altura (metros)',
            'largo': 'Largo (metros)',
            'ancho': 'Ancho (metros)',
        }
        help_texts = {
            'nombre': 'Ingresa un nombre descriptivo para la sala.',
            'descripcion': 'Proporciona detalles adicionales sobre la sala (opcional).',
            'tipo': 'Selecciona el tipo de sala según su uso principal.',
            'altura': 'Ingresa la altura de la sala en metros.',
            'largo': 'Ingresa el largo de la sala en metros.',
            'ancho': 'Ingresa el ancho de la sala en metros.',
        }

class AreaCultivoForm(forms.ModelForm):
    class Meta:
        model = AreaCultivo
        fields = ['nombre', 'tipo_cultivo', 'tiene_riego_automatico', 'altura', 'largo', 'ancho']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_cultivo': forms.Select(attrs={'class': 'form-select'}),
            'tiene_riego_automatico': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'largo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ancho': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'nombre': 'Nombre del Área',
            'tipo_cultivo': 'Tipo de Cultivo',
            'tiene_riego_automatico': '¿Tiene Riego Automático?',
            'altura': 'Altura (metros)',
            'largo': 'Largo (metros)',
            'ancho': 'Ancho (metros)',
        }
        help_texts = {
            'nombre': 'Ingresa un nombre descriptivo para el área.',
            'tipo_cultivo': 'Selecciona el tipo de cultivo que se realizará en esta área.',
            'tiene_riego_automatico': 'Marca esta casilla si el área cuenta con sistema de riego automático.',
            'altura': 'Ingresa la altura del área en metros.',
            'largo': 'Ingresa el largo del área en metros.',
            'ancho': 'Ingresa el ancho del área en metros.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ya no necesitamos establecer campos como no requeridos ya que no existen

class GeneticaForm(forms.ModelForm):
    class Meta:
        model = Genetica
        fields = ['nombre', 'descripcion', 'thc_estimado', 'cbd_estimado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'thc_estimado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'cbd_estimado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }
        labels = {
            'nombre': 'Nombre de la Genética',
            'descripcion': 'Descripción',
            'thc_estimado': 'THC Estimado (%)',
            'cbd_estimado': 'CBD Estimado (%)',
        }
        help_texts = {
            'nombre': 'Ingresa el nombre de la genética.',
            'descripcion': 'Proporciona detalles sobre la genética (opcional).',
            'thc_estimado': 'Ingresa el porcentaje estimado de THC.',
            'cbd_estimado': 'Ingresa el porcentaje estimado de CBD.',
        }

class SemillaForm(forms.ModelForm):
    class Meta:
        model = Semilla
        fields = ['nombre', 'descripcion', 'cantidad_disponible', 'fecha_compra']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cantidad_disponible': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'fecha_compra': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'nombre': 'Nombre de la Semilla',
            'descripcion': 'Descripción',
            'cantidad_disponible': 'Cantidad Disponible',
            'fecha_compra': 'Fecha de Compra',
        }
        help_texts = {
            'nombre': 'Ingresa el nombre o identificador de la semilla.',
            'descripcion': 'Proporciona detalles sobre la semilla (opcional).',
            'cantidad_disponible': 'Ingresa la cantidad de semillas disponibles.',
            'fecha_compra': 'Ingresa la fecha de compra de las semillas.',
        }

class PlantaForm(forms.ModelForm):
    class Meta:
        model = Planta
        fields = ['nombre_id', 'tipo_planta', 'semilla', 'planta_madre', 'es_madre', 'fecha_germinacion', 'etapa_actual']
        widgets = {
            'nombre_id': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_planta': forms.Select(attrs={'class': 'form-select'}),
            'semilla': forms.Select(attrs={'class': 'form-select'}),
            'planta_madre': forms.Select(attrs={'class': 'form-select'}),
            'es_madre': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fecha_germinacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'etapa_actual': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'nombre_id': 'Identificador de la Planta',
            'tipo_planta': 'Tipo de Planta',
            'semilla': 'Semilla',
            'planta_madre': 'Planta Madre',
            'es_madre': '¿Es Planta Madre?',
            'fecha_germinacion': 'Fecha de Germinación',
            'etapa_actual': 'Etapa Actual',
        }
        help_texts = {
            'nombre_id': 'Ingresa un identificador único para la planta.',
            'tipo_planta': 'Selecciona si la planta proviene de semilla o esqueje.',
            'semilla': 'Selecciona la semilla utilizada (solo si el tipo es semilla).',
            'planta_madre': 'Selecciona la planta madre (solo si el tipo es esqueje).',
            'es_madre': 'Marca esta casilla si la planta será utilizada como madre para esquejes.',
            'fecha_germinacion': 'Ingresa la fecha de germinación de la planta.',
            'etapa_actual': 'Selecciona la etapa actual de la planta.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar semillas con stock disponible
        self.fields['semilla'].queryset = Semilla.objects.filter(cantidad_disponible__gt=0)
        # Filtrar plantas madre activas
        self.fields['planta_madre'].queryset = Planta.objects.filter(es_madre=True, activa=True)
        # Hacer los campos opcionales inicialmente
        self.fields['semilla'].required = False
        self.fields['planta_madre'].required = False

    def clean(self):
        cleaned_data = super().clean()
        tipo_planta = cleaned_data.get('tipo_planta')
        semilla = cleaned_data.get('semilla')
        planta_madre = cleaned_data.get('planta_madre')

        if tipo_planta == 'semilla':
            if not semilla:
                self.add_error('semilla', 'Debes seleccionar una semilla.')
            elif semilla.cantidad_disponible <= 0:
                self.add_error('semilla', 'No hay stock disponible de esta semilla.')
            if planta_madre:
                self.add_error('planta_madre', 'No puedes seleccionar una planta madre si el tipo es semilla.')
        
        elif tipo_planta == 'esqueje':
            if not planta_madre:
                self.add_error('planta_madre', 'Debes seleccionar una planta madre.')
            if semilla:
                self.add_error('semilla', 'No puedes seleccionar una semilla si el tipo es esqueje.')

        return cleaned_data