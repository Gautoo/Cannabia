# gestion_cultivo/urls.py
from django.urls import path
from . import views

app_name = 'gestion_cultivo'

urlpatterns = [
    path('inicio/', views.pagina_inicio_cultivo, name='pagina_inicio_cultivo'),
    path('salas/', views.lista_salas, name='lista_salas'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('salas/crear/', views.crear_sala, name='crear_sala'),
    # Nuevas rutas para el CRUD de Salas
    path('salas/<int:sala_id>/', views.detalle_sala, name='detalle_sala'),
    path('salas/<int:sala_id>/editar/', views.editar_sala, name='editar_sala'),
    path('salas/<int:sala_id>/eliminar/', views.eliminar_sala, name='eliminar_sala'),
    # URLs para el CRUD de Áreas de Cultivo
    path('salas/<int:sala_id>/areas/crear/', views.crear_area, name='crear_area'),
    path('areas/<int:area_id>/', views.detalle_area, name='detalle_area'),
    path('areas/<int:area_id>/editar/', views.editar_area, name='editar_area'),
    path('areas/<int:area_id>/eliminar/', views.eliminar_area, name='eliminar_area'),
    # URLs para el CRUD de Plantas
    path('areas/<int:area_id>/plantas/crear/', views.crear_planta, name='crear_planta'),
    path('plantas/<int:planta_id>/', views.detalle_planta, name='detalle_planta'),
    path('plantas/<int:planta_id>/editar/', views.editar_planta, name='editar_planta'),
    path('plantas/<int:planta_id>/eliminar/', views.eliminar_planta, name='eliminar_planta'),
    # URLs para el CRUD de Genéticas
    path('geneticas/', views.lista_geneticas, name='lista_geneticas'),
    path('geneticas/crear/', views.crear_genetica, name='crear_genetica'),
    path('geneticas/<int:genetica_id>/', views.detalle_genetica, name='detalle_genetica'),
    path('geneticas/<int:genetica_id>/editar/', views.editar_genetica, name='editar_genetica'),
    path('geneticas/<int:genetica_id>/eliminar/', views.eliminar_genetica, name='eliminar_genetica'),
]