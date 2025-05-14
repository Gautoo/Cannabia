# gestion_cultivo/urls.py
from django.urls import path
from . import views

app_name = 'gestion_cultivo'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('configuracion/', views.configuracion, name='configuracion'),
    
    # URLs de Inventario
    path('inventario/', views.inventario, name='inventario'),
    path('inventario/agregar-stock/', views.agregar_stock, name='agregar_stock'),
    path('inventario/editar-stock/<int:pk>/', views.editar_stock, name='editar_stock'),
    path('inventario/nuevo-producto/', views.nuevo_producto, name='nuevo_producto'),
    
    # URLs de Semillas
    path('inventario/semillas/', views.lista_semillas, name='lista_semillas'),
    path('inventario/semillas/crear/', views.crear_semilla, name='crear_semilla'),
    path('inventario/semillas/<int:pk>/', views.detalle_semilla, name='detalle_semilla'),
    path('inventario/semillas/<int:pk>/editar/', views.editar_semilla, name='editar_semilla'),
    path('inventario/semillas/<int:pk>/eliminar/', views.eliminar_semilla, name='eliminar_semilla'),
    
    # URLs de Fertilizantes
    path('inventario/fertilizantes/', views.lista_fertilizantes, name='lista_fertilizantes'),
    path('inventario/fertilizantes/crear/', views.crear_fertilizante, name='crear_fertilizante'),
    path('inventario/fertilizantes/<int:pk>/', views.detalle_fertilizante, name='detalle_fertilizante'),
    path('inventario/fertilizantes/<int:pk>/editar/', views.editar_fertilizante, name='editar_fertilizante'),
    path('inventario/fertilizantes/<int:pk>/eliminar/', views.eliminar_fertilizante, name='eliminar_fertilizante'),
    
    # URLs de Contenedores
    path('inventario/contenedores/', views.lista_contenedores, name='lista_contenedores'),
    path('inventario/contenedores/crear/', views.crear_contenedor, name='crear_contenedor'),
    path('inventario/contenedores/<int:pk>/', views.detalle_contenedor, name='detalle_contenedor'),
    path('inventario/contenedores/<int:pk>/editar/', views.editar_contenedor, name='editar_contenedor'),
    path('inventario/contenedores/<int:pk>/eliminar/', views.eliminar_contenedor, name='eliminar_contenedor'),
    
    # URLs de Maquinaria
    path('inventario/maquinaria/', views.lista_maquinaria, name='lista_maquinaria'),
    path('inventario/maquinaria/crear/', views.crear_maquinaria, name='crear_maquinaria'),
    path('inventario/maquinaria/<int:pk>/', views.detalle_maquinaria, name='detalle_maquinaria'),
    path('inventario/maquinaria/<int:pk>/editar/', views.editar_maquinaria, name='editar_maquinaria'),
    path('inventario/maquinaria/<int:pk>/eliminar/', views.eliminar_maquinaria, name='eliminar_maquinaria'),

    # URLs de Cultivo
    path('cultivo/', views.pagina_inicio_cultivo, name='pagina_inicio_cultivo'),
    path('cultivo/salas/', views.lista_salas, name='lista_salas'),
    path('cultivo/salas/crear/', views.crear_sala, name='crear_sala'),
    path('cultivo/salas/<int:pk>/', views.detalle_sala, name='detalle_sala'),
    path('cultivo/salas/<int:pk>/editar/', views.editar_sala, name='editar_sala'),
    path('cultivo/salas/<int:pk>/eliminar/', views.eliminar_sala, name='eliminar_sala'),
    path('cultivo/areas/', views.lista_areas, name='lista_areas'),
    path('cultivo/areas/crear/<int:sala_id>/', views.crear_area, name='crear_area'),
    path('cultivo/areas/<int:pk>/', views.detalle_area, name='detalle_area'),
    path('cultivo/areas/<int:pk>/editar/', views.editar_area, name='editar_area'),
    path('cultivo/areas/<int:pk>/eliminar/', views.eliminar_area, name='eliminar_area'),
    path('cultivo/plantas/crear/<int:area_id>/', views.crear_planta, name='crear_planta'),
    path('cultivo/plantas/<int:pk>/', views.detalle_planta, name='detalle_planta'),
    path('cultivo/plantas/<int:pk>/editar/', views.editar_planta, name='editar_planta'),
    path('cultivo/plantas/<int:pk>/eliminar/', views.eliminar_planta, name='eliminar_planta'),
    path('cultivo/plantas/<int:pk>/mover/', views.mover_planta, name='mover_planta'),
    
    # URLs de Genéticas
    path('geneticas/', views.lista_geneticas, name='lista_geneticas'),
    path('geneticas/crear/', views.crear_genetica, name='crear_genetica'),
    path('geneticas/<int:pk>/', views.detalle_genetica, name='detalle_genetica'),
    path('geneticas/<int:pk>/editar/', views.editar_genetica, name='editar_genetica'),
    path('geneticas/<int:pk>/eliminar/', views.eliminar_genetica, name='eliminar_genetica'),
]