# gestion_cultivo/admin.py
from django.contrib import admin
from .models import Sala, AreaCultivo, Planta, Genetica, Semilla

# Clases de Administración (Opcional pero recomendado para personalizar el admin)
class AreaCultivoInline(admin.StackedInline): # O admin.TabularInline para vista más compacta
    model = AreaCultivo
    extra = 1 # Cuántos formularios de áreas vacías mostrar al crear/editar una Sala

class PlantaInline(admin.StackedInline):
    model = Planta
    extra = 1 # Cuántos formularios de plantas vacías mostrar

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'tipo', 'fecha_creacion')
    list_filter = ('tipo', 'usuario')
    search_fields = ('nombre',)

@admin.register(AreaCultivo)
class AreaCultivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sala', 'tipo_cultivo', 'tiene_riego_automatico', 'fecha_creacion')
    list_filter = ('tipo_cultivo', 'tiene_riego_automatico', 'sala')
    search_fields = ('nombre',)

@admin.register(Planta)
class PlantaAdmin(admin.ModelAdmin):
    list_display = ('nombre_id', 'tipo_planta', 'etapa_actual', 'area', 'activa', 'fecha_creacion')
    list_filter = ('tipo_planta', 'etapa_actual', 'activa', 'area')
    search_fields = ('nombre_id',)
    date_hierarchy = 'fecha_creacion'

@admin.register(Genetica)
class GeneticaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'thc_estimado', 'cbd_estimado', 'fecha_creacion')
    search_fields = ('nombre',)
    date_hierarchy = 'fecha_creacion'

@admin.register(Semilla)
class SemillaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad_disponible', 'fecha_compra', 'fecha_creacion')
    list_filter = ('fecha_compra',)
    search_fields = ('nombre',)
    date_hierarchy = 'fecha_creacion'