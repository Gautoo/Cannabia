# gestion_cultivo/admin.py
from django.contrib import admin
from .models import (
    Sala, AreaCultivo, Planta, Genetica, Semilla, Fertilizante,
    Banco, Terpeno, Caracteristica, Contenedor, Maquinaria, 
    Stock, PresentacionFertilizante
)

# Clases de Administración (Opcional pero recomendado para personalizar el admin)
class AreaCultivoInline(admin.StackedInline): # O admin.TabularInline para vista más compacta
    model = AreaCultivo
    extra = 1 # Cuántos formularios de áreas vacías mostrar al crear/editar una Sala

class PlantaInline(admin.StackedInline):
    model = Planta
    extra = 1 # Cuántos formularios de plantas vacías mostrar

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_iluminacion', 'temperatura_objetivo', 'humedad_objetivo')
    list_filter = ('tipo_iluminacion',)
    search_fields = ('nombre', 'descripcion')

@admin.register(AreaCultivo)
class AreaCultivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sala', 'tipo_cultivo', 'estado')
    list_filter = ('tipo_cultivo', 'estado', 'sala')
    search_fields = ('nombre', 'descripcion')

@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    list_display = ('nombre_id', 'tipo_planta', 'etapa_actual', 'activa', 'es_madre')
    list_filter = ('tipo_planta', 'etapa_actual', 'activa', 'es_madre')
    search_fields = ('nombre_id', 'descripcion')

@admin.register(Genetica)
class GeneticaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'tiempo_floracion', 'thc_estimado', 'cbd_estimado')
    list_filter = ('tipo',)
    search_fields = ('nombre', 'descripcion')

@admin.register(Semilla)
class SemillaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'banco', 'variedad', 'thc', 'cbd', 'fecha_compra')
    list_filter = ('banco', 'variedad', 'fecha_compra')
    search_fields = ('nombre', 'variedad', 'banco__nombre')
    date_hierarchy = 'fecha_compra'

@admin.register(Fertilizante)
class FertilizanteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'tipo', 'etapa_uso', 'precio')
    list_filter = ('tipo', 'etapa_uso', 'medio_compatible')
    search_fields = ('nombre', 'marca')

@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')

@admin.register(Terpeno)
class TerpenoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')

@admin.register(Caracteristica)
class CaracteristicaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')

@admin.register(Contenedor)
class ContenedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'capacidad', 'precio')
    list_filter = ('tipo', 'material')
    search_fields = ('nombre', 'descripcion')

@admin.register(Maquinaria)
class MaquinariaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'marca', 'modelo', 'precio')
    list_filter = ('tipo', 'marca')
    search_fields = ('nombre', 'marca', 'modelo')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('tipo_producto', 'cantidad', 'fecha_compra', 'precio_compra')
    list_filter = ('tipo_producto', 'fecha_compra')
    search_fields = ('tipo_producto', 'proveedor')

@admin.register(PresentacionFertilizante)
class PresentacionFertilizanteAdmin(admin.ModelAdmin):
    list_display = ('fertilizante', 'tamano', 'precio')
    list_filter = ('fertilizante',)
    search_fields = ('fertilizante__nombre', 'tamano')