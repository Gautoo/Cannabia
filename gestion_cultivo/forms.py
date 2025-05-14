# gestion_cultivo/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    Semilla, Fertilizante, Contenedor, Maquinaria, Stock, Sala, AreaCultivo, Planta, Genetica, Banco, Terpeno, Caracteristica, PresentacionFertilizante
)

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UsuarioForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email')

class SemillaForm(forms.ModelForm):
    class Meta:
        model = Semilla
        fields = ['nombre', 'descripcion', 'banco', 'fecha_compra', 'cbd', 'thc', 'tiempo_floracion', 'rendimiento', 'variedad', 'caracteristicas', 'terpenos', 'ciclo', 'observaciones', 'padres', 'precio', 'tamano_blister']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'fecha_compra': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cbd': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 0.01, 'class': 'form-control'}),
            'thc': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 0.01, 'class': 'form-control'}),
            'tiempo_floracion': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
            'rendimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'variedad': forms.TextInput(attrs={'class': 'form-control'}),
            'terpenos': forms.TextInput(attrs={'class': 'form-control'}),
            'ciclo': forms.TextInput(attrs={'class': 'form-control'}),
            'padres': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'min': 0, 'step': 0.01, 'class': 'form-control'}),
            'tamano_blister': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'banco': forms.Select(attrs={'class': 'form-control'}),
            'caracteristicas': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class FertilizanteForm(forms.ModelForm):
    class Meta:
        model = Fertilizante
        fields = ['nombre', 'marca', 'descripcion', 'tipo', 'etapa_uso', 'medio_compatible', 'npk', 'precio', 'instrucciones']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'instrucciones': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'min': 0, 'step': 0.01, 'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'etapa_uso': forms.Select(attrs={'class': 'form-control'}),
            'medio_compatible': forms.Select(attrs={'class': 'form-control'}),
            'npk': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ContenedorForm(forms.ModelForm):
    class Meta:
        model = Contenedor
        fields = ['nombre', 'descripcion', 'dimensiones', 'caracteristicas', 'tipo', 'capacidad', 'color', 'material', 'precio']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'caracteristicas': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'min': 0, 'step': 0.01, 'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'dimensiones': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'min': 0, 'step': 0.01, 'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'material': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MaquinariaForm(forms.ModelForm):
    class Meta:
        model = Maquinaria
        fields = ['nombre', 'descripcion', 'tipo', 'marca', 'modelo', 'potencia', 'voltaje', 'compatibilidad', 'dimensiones', 'accesorios', 'precio']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'accesorios': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'min': 0, 'step': 0.01, 'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'potencia': forms.TextInput(attrs={'class': 'form-control'}),
            'voltaje': forms.TextInput(attrs={'class': 'form-control'}),
            'compatibilidad': forms.TextInput(attrs={'class': 'form-control'}),
            'dimensiones': forms.TextInput(attrs={'class': 'form-control'}),
        }

class StockForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['semilla'].queryset = Semilla.objects.filter(usuario=user)
        self.fields['fertilizante'].queryset = Fertilizante.objects.filter(usuario=user)
        self.fields['contenedor'].queryset = Contenedor.objects.filter(usuario=user)
        self.fields['maquinaria'].queryset = Maquinaria.objects.filter(usuario=user)

    class Meta:
        model = Stock
        fields = ['tipo_producto', 'cantidad', 'fecha_compra', 'fecha_vencimiento', 'lote', 'ubicacion', 'notas', 'precio_compra', 'proveedor', 'semilla', 'fertilizante', 'contenedor', 'maquinaria']
        widgets = {
            'notas': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'precio_compra': forms.NumberInput(attrs={'min': 0, 'step': 0.01, 'class': 'form-control'}),
            'tipo_producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'min': 0, 'class': 'form-control'}),
            'fecha_compra': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'lote': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'semilla': forms.Select(attrs={'class': 'form-control'}),
            'fertilizante': forms.Select(attrs={'class': 'form-control'}),
            'contenedor': forms.Select(attrs={'class': 'form-control'}),
            'maquinaria': forms.Select(attrs={'class': 'form-control'}),
        }

class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ['nombre', 'descripcion', 'tipo_iluminacion', 'temperatura_objetivo', 'humedad_objetivo', 'horas_luz']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'temperatura_objetivo': forms.NumberInput(attrs={'min': 0, 'max': 50, 'step': 0.1, 'class': 'form-control'}),
            'humedad_objetivo': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 0.1, 'class': 'form-control'}),
            'horas_luz': forms.NumberInput(attrs={'min': 0, 'max': 24, 'class': 'form-control'}),
        }

class AreaCultivoForm(forms.ModelForm):
    class Meta:
        model = AreaCultivo
        fields = ['nombre', 'descripcion', 'tipo_cultivo', 'estado', 'tiene_riego_automatico', 'sustrato', 'composicion_sustrato']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'composicion_sustrato': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class PlantaForm(forms.ModelForm):
    class Meta:
        model = Planta
        fields = ['nombre_id', 'descripcion', 'tipo_planta', 'etapa_actual', 'activa', 'es_madre', 'planta_madre', 'semilla', 'thc_estimado', 'cbd_estimado', 'fecha_germinacion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'fecha_germinacion': forms.DateInput(attrs={'type': 'date'}),
            'thc_estimado': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 0.01}),
            'cbd_estimado': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 0.01}),
        }

class GeneticaForm(forms.ModelForm):
    class Meta:
        model = Genetica
        fields = ['nombre', 'descripcion', 'tipo', 'tiempo_floracion', 'rendimiento', 'thc_estimado', 'cbd_estimado']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'tiempo_floracion': forms.NumberInput(attrs={'min': 0}),
            'thc_estimado': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 0.01}),
            'cbd_estimado': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 0.01}),
        }

class BancoForm(forms.ModelForm):
    class Meta:
        model = Banco
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class TerpenoForm(forms.ModelForm):
    class Meta:
        model = Terpeno
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class CaracteristicaForm(forms.ModelForm):
    class Meta:
        model = Caracteristica
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

class MoverPlantaForm(forms.ModelForm):
    class Meta:
        model = Planta
        fields = ['area']

class MoverAreaForm(forms.ModelForm):
    class Meta:
        model = AreaCultivo
        fields = ['sala']

class PresentacionFertilizanteForm(forms.ModelForm):
    class Meta:
        model = PresentacionFertilizante
        fields = ['tamano', 'precio', 'fertilizante']
        widgets = {
            'precio': forms.NumberInput(attrs={'min': 0, 'step': 0.01}),
        }