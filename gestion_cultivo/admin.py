# gestion_cultivo/admin.py
from django.contrib import admin
from .models import Sala, AreaCultivo, Planta, Genetica, Semilla, Fertilizante, Base, Lampara, Maceta, Aditivo, Banco, Terpeno, Caracteristica

# Clases de Administración (Opcional pero recomendado para personalizar el admin)
class AreaCultivoInline(admin.StackedInline): # O admin.TabularInline para vista más compacta
    model = AreaCultivo
    extra = 1 # Cuántos formularios de áreas vacías mostrar al crear/editar una Sala

class PlantaInline(admin.StackedInline):
    model = Planta
    extra = 1 # Cuántos formularios de plantas vacías mostrar

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'tipo_iluminacion', 'temperatura_objetivo', 'humedad_objetivo')
    list_filter = ('tipo_iluminacion', 'usuario')
    search_fields = ('nombre', 'descripcion')

@admin.register(AreaCultivo)
class AreaCultivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sala', 'tipo_cultivo', 'estado')
    list_filter = ('tipo_cultivo', 'estado', 'sala')
    search_fields = ('nombre', 'descripcion')

@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    list_display = ('nombre_id', 'tipo_planta', 'etapa_actual', 'area', 'activa')
    list_filter = ('tipo_planta', 'etapa_actual', 'area', 'activa')
    search_fields = ('nombre_id',)

@admin.register(Genetica)
class GeneticaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'tiempo_floracion', 'thc_estimado', 'cbd_estimado')
    list_filter = ('tipo',)
    search_fields = ('nombre', 'descripcion')

@admin.register(Semilla)
class SemillaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'banco', 'porcentaje_thc', 'porcentaje_cbd', 'cantidad')
    list_filter = ('banco',)
    search_fields = ('nombre', 'descripcion')

@admin.register(Fertilizante)
class FertilizanteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'tipo', 'npk', 'cantidad')
    list_filter = ('marca', 'tipo')
    search_fields = ('nombre', 'descripcion')

@admin.register(Base)
class BaseAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'tipo', 'cantidad')
    list_filter = ('marca', 'tipo')
    search_fields = ('nombre', 'descripcion')

@admin.register(Lampara)
class LamparaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'potencia', 'tipo', 'marca', 'cantidad')
    list_filter = ('tipo', 'marca')
    search_fields = ('nombre', 'descripcion')

@admin.register(Maceta)
class MacetaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'capacidad', 'material', 'cantidad')
    list_filter = ('material',)
    search_fields = ('nombre', 'descripcion')

@admin.register(Aditivo)
class AditivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'tipo', 'cantidad')
    list_filter = ('marca', 'tipo')
    search_fields = ('nombre', 'descripcion')

@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre', 'descripcion')

@admin.register(Terpeno)
class TerpenoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre', 'descripcion')

@admin.register(Caracteristica)
class CaracteristicaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre', 'descripcion')