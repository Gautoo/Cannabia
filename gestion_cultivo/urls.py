# gestion_cultivo/urls.py
from django.urls import path
from . import views

app_name = 'gestion_cultivo'

urlpatterns = [
    # URLs principales
    path('', views.index, name='index'),
    
    # URLs para Salas
    path('salas/', views.lista_salas, name='lista_salas'),
    path('salas/crear/', views.crear_sala, name='crear_sala'),
    path('salas/<int:sala_id>/', views.detalle_sala, name='detalle_sala'),
    path('salas/<int:sala_id>/editar/', views.editar_sala, name='editar_sala'),
    path('salas/<int:sala_id>/eliminar/', views.eliminar_sala, name='eliminar_sala'),
    
    # URLs para Áreas
    path('areas/crear/<int:sala_id>/', views.crear_area, name='crear_area'),
    path('areas/<int:area_id>/', views.detalle_area, name='detalle_area'),
    path('areas/<int:area_id>/editar/', views.editar_area, name='editar_area'),
    path('areas/<int:area_id>/eliminar/', views.eliminar_area, name='eliminar_area'),
    
    # URLs para Plantas
    path('plantas/crear/<int:area_id>/', views.crear_planta, name='crear_planta'),
    path('plantas/<int:planta_id>/', views.detalle_planta, name='detalle_planta'),
    path('plantas/<int:planta_id>/editar/', views.editar_planta, name='editar_planta'),
    path('plantas/<int:planta_id>/eliminar/', views.eliminar_planta, name='eliminar_planta'),
    
    # URLs para Semillas
    path('semillas/', views.lista_semillas, name='lista_semillas'),
    path('semillas/crear/', views.crear_semilla, name='crear_semilla'),
    path('semillas/<int:semilla_id>/', views.detalle_semilla, name='detalle_semilla'),
    path('semillas/<int:semilla_id>/editar/', views.editar_semilla, name='editar_semilla'),
    path('semillas/<int:semilla_id>/eliminar/', views.eliminar_semilla, name='eliminar_semilla'),
    
    # URLs para Genéticas
    path('geneticas/', views.lista_geneticas, name='lista_geneticas'),
    path('geneticas/crear/', views.crear_genetica, name='crear_genetica'),
    path('geneticas/<int:genetica_id>/', views.detalle_genetica, name='detalle_genetica'),
    path('geneticas/<int:genetica_id>/editar/', views.editar_genetica, name='editar_genetica'),
    path('geneticas/<int:genetica_id>/eliminar/', views.eliminar_genetica, name='eliminar_genetica'),
    
    # URLs para Plantas Madre
    path('plantas-madre/', views.lista_plantas_madre, name='lista_plantas_madre'),
]