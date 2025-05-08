# gestion_cultivo/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    Sala, AreaCultivo, Planta, Genetica, Semilla, Fertilizante,
    Banco, Terpeno, Caracteristica, Lampara, Maceta, Aditivo, Base
)
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
        fields = ['nombre', 'descripcion', 'temperatura_objetivo', 'humedad_objetivo', 'tipo_iluminacion', 'horas_luz']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'temperatura_objetivo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'humedad_objetivo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'tipo_iluminacion': forms.Select(attrs={'class': 'form-control'}),
            'horas_luz': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AreaCultivoForm(forms.ModelForm):
    class Meta:
        model = AreaCultivo
        fields = [
            'nombre', 'tipo_cultivo', 'estado', 'tiene_riego_automatico',
            'sustrato', 'composicion_sustrato', 'tamano_maceta', 'tamano_balde',
            'altura', 'largo', 'ancho'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_cultivo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'tiene_riego_automatico': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sustrato': forms.TextInput(attrs={'class': 'form-control'}),
            'composicion_sustrato': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tamano_maceta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'tamano_balde': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'largo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ancho': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class GeneticaForm(forms.ModelForm):
    class Meta:
        model = Genetica
        fields = ['nombre', 'descripcion', 'tipo', 'tiempo_floracion', 'rendimiento', 'thc_estimado', 'cbd_estimado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'tiempo_floracion': forms.NumberInput(attrs={'class': 'form-control'}),
            'rendimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'thc_estimado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cbd_estimado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class SemillaForm(forms.ModelForm):
    class Meta:
        model = Semilla
        fields = [
            'nombre', 'banco', 'porcentaje_thc', 'porcentaje_cbd',
            'dias_flora', 'terpenos', 'caracteristicas', 'descripcion',
            'cantidad', 'fecha_compra'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'banco': forms.Select(attrs={'class': 'form-control'}),
            'porcentaje_thc': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'porcentaje_cbd': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'dias_flora': forms.NumberInput(attrs={'class': 'form-control'}),
            'terpenos': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'caracteristicas': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'fecha_compra': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class FertilizanteForm(forms.ModelForm):
    class Meta:
        model = Fertilizante
        fields = ['nombre', 'marca', 'tipo', 'npk', 'descripcion', 'cantidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'npk': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class PlantaForm(forms.ModelForm):
    class Meta:
        model = Planta
        fields = ['nombre_id', 'tipo_planta', 'semilla', 'planta_madre', 'es_madre', 
                 'thc_estimado', 'cbd_estimado', 'fecha_germinacion', 'etapa_actual', 'area', 'activa']
        widgets = {
            'nombre_id': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_planta': forms.Select(attrs={'class': 'form-control'}),
            'semilla': forms.Select(attrs={'class': 'form-control'}),
            'planta_madre': forms.Select(attrs={'class': 'form-control'}),
            'thc_estimado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cbd_estimado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fecha_germinacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'etapa_actual': forms.Select(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar semillas con stock disponible
        self.fields['semilla'].queryset = Semilla.objects.filter(cantidad__gt=0)
        # Hacer los campos opcionales inicialmente
        self.fields['semilla'].required = False
        self.fields['planta_madre'].required = False

    def clean(self):
        cleaned_data = super().clean()
        semilla = cleaned_data.get('semilla')
        tipo_planta = cleaned_data.get('tipo_planta')

        if tipo_planta == 'semilla' and semilla:
            if semilla.cantidad <= 0:
                self.add_error('semilla', 'No hay stock disponible de esta semilla.')

        return cleaned_data

class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class TerpenoForm(forms.ModelForm):
    class Meta:
        model = Terpeno
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CaracteristicaForm(forms.ModelForm):
    class Meta:
        model = Caracteristica
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class LamparaForm(forms.ModelForm):
    class Meta:
        model = Lampara
        fields = ['nombre', 'potencia', 'tipo', 'marca', 'descripcion', 'cantidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'potencia': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class MacetaForm(forms.ModelForm):
    class Meta:
        model = Maceta
        fields = ['nombre', 'capacidad', 'material', 'descripcion', 'cantidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'material': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AditivoForm(forms.ModelForm):
    class Meta:
        model = Aditivo
        fields = ['nombre', 'marca', 'tipo', 'descripcion', 'cantidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BaseForm(forms.ModelForm):
    class Meta:
        model = Base
        fields = ['nombre', 'marca', 'tipo', 'descripcion', 'cantidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class MoverPlantaForm(forms.ModelForm):
    class Meta:
        model = Planta
        fields = ['area']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            planta = kwargs['instance']
            self.fields['area'].queryset = AreaCultivo.objects.filter(
                sala__usuario=planta.area.sala.usuario
            ).exclude(id=planta.area.id)

class MoverAreaForm(forms.ModelForm):
    class Meta:
        model = AreaCultivo
        fields = ['sala']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'instance' in kwargs:
            area = kwargs['instance']
            self.fields['sala'].queryset = Sala.objects.filter(
                usuario=area.sala.usuario
            ).exclude(id=area.sala.id)