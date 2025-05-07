# gestion_cultivo/admin.py
from django.contrib import admin
from .models import Sala, AreaCultivo, Planta # Importa tus modelos

# Clases de Administración (Opcional pero recomendado para personalizar el admin)
class AreaCultivoInline(admin.StackedInline): # O admin.TabularInline para vista más compacta
    model = AreaCultivo
    extra = 1 # Cuántos formularios de áreas vacías mostrar al crear/editar una Sala

class PlantaInline(admin.StackedInline):
    model = Planta
    extra = 1 # Cuántos formularios de plantas vacías mostrar

class SalaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'usuario', 'descripcion') # Columnas a mostrar en la lista de Salas
    list_filter = ('usuario',) # Permite filtrar por usuario
    search_fields = ('nombre',) # Añade un campo de búsqueda por nombre
    inlines = [AreaCultivoInline] # Permite añadir/editar Áreas directamente desde la Sala

class AreaCultivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'sala', 'get_sala_usuario') # Muestra el nombre, la sala y el usuario de la sala
    list_filter = ('sala__usuario', 'sala') # Permite filtrar por usuario (a través de la sala) o por sala
    search_fields = ('nombre', 'sala__nombre')
    inlines = [PlantaInline] # Permite añadir/editar Plantas directamente desde el Área

    # Función para mostrar el usuario de la sala en la lista
    @admin.display(description='Usuario de la Sala')
    def get_sala_usuario(self, obj):
        return obj.sala.usuario

class PlantaAdmin(admin.ModelAdmin):
    list_display = ('nombre_id', 'genetica', 'area', 'etapa_actual', 'activa')
    list_filter = ('etapa_actual', 'activa', 'area__sala__usuario', 'area__sala', 'area') # Filtros útiles
    search_fields = ('nombre_id', 'genetica', 'area__nombre', 'area__sala__nombre')
    list_editable = ('etapa_actual', 'activa') # Permite editar estos campos directamente en la lista

# Registra tus modelos con sus clases de administración personalizadas
admin.site.register(Sala, SalaAdmin)
admin.site.register(AreaCultivo, AreaCultivoAdmin)
admin.site.register(Planta, PlantaAdmin)