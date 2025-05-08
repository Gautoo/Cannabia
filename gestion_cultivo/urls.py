# gestion_cultivo/urls.py
from django.urls import path
from . import views

app_name = 'gestion_cultivo'

urlpatterns = [
    # URLs de autenticación
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    
    # URLs principales
    path('', views.dashboard, name='index'),  # Cambiamos dashboard a index
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inventario/', views.inventario, name='inventario'),
    path('cultivo/', views.cultivo, name='cultivo'),
    path('configuracion/', views.configuracion, name='configuracion'),
    
    # URLs de Salas
    path('salas/', views.lista_salas, name='lista_salas'),
    path('salas/crear/', views.crear_sala, name='crear_sala'),
    path('salas/<int:pk>/', views.detalle_sala, name='detalle_sala'),
    path('salas/<int:pk>/editar/', views.editar_sala, name='editar_sala'),
    path('salas/<int:pk>/eliminar/', views.eliminar_sala, name='eliminar_sala'),
    
    # URLs de Áreas de Cultivo
    path('areas/<int:sala_id>/crear/', views.crear_area, name='crear_area'),
    path('areas/<int:pk>/', views.detalle_area, name='detalle_area'),
    path('areas/<int:pk>/editar/', views.editar_area, name='editar_area'),
    path('areas/<int:pk>/eliminar/', views.eliminar_area, name='eliminar_area'),
    path('areas/<int:pk>/mover/', views.mover_area, name='mover_area'),
    
    # URLs de Plantas
    path('plantas/<int:area_id>/crear/', views.crear_planta, name='crear_planta'),
    path('plantas/<int:pk>/', views.detalle_planta, name='detalle_planta'),
    path('plantas/<int:pk>/editar/', views.editar_planta, name='editar_planta'),
    path('plantas/<int:pk>/eliminar/', views.eliminar_planta, name='eliminar_planta'),
    path('plantas/<int:pk>/mover/', views.mover_planta, name='mover_planta'),
    
    # URLs de Genética
    path('genetica/', views.lista_geneticas, name='lista_genetica'),
    path('genetica/crear/', views.crear_genetica, name='crear_genetica'),
    path('genetica/<int:genetica_id>/', views.detalle_genetica, name='detalle_genetica'),
    path('genetica/<int:genetica_id>/editar/', views.editar_genetica, name='editar_genetica'),
    path('genetica/<int:genetica_id>/eliminar/', views.eliminar_genetica, name='eliminar_genetica'),
    
    # URLs de Semillas
    path('semillas/', views.lista_semillas, name='lista_semillas'),
    path('semillas/crear/', views.crear_semilla, name='crear_semilla'),
    path('semillas/<int:pk>/', views.detalle_semilla, name='detalle_semilla'),
    path('semillas/<int:pk>/editar/', views.editar_semilla, name='editar_semilla'),
    path('semillas/<int:pk>/eliminar/', views.eliminar_semilla, name='eliminar_semilla'),
    
    # URLs de Fertilizantes
    path('fertilizantes/', views.lista_fertilizantes, name='lista_fertilizantes'),
    path('fertilizantes/crear/', views.crear_fertilizante, name='crear_fertilizante'),
    path('fertilizantes/<int:pk>/', views.detalle_fertilizante, name='detalle_fertilizante'),
    path('fertilizantes/<int:pk>/editar/', views.editar_fertilizante, name='editar_fertilizante'),
    path('fertilizantes/<int:pk>/eliminar/', views.eliminar_fertilizante, name='eliminar_fertilizante'),
    
    # URLs de Lámparas
    path('lamparas/', views.lista_lamparas, name='lista_lamparas'),
    path('lamparas/crear/', views.crear_lampara, name='crear_lampara'),
    path('lamparas/<int:pk>/', views.detalle_lampara, name='detalle_lampara'),
    path('lamparas/<int:pk>/editar/', views.editar_lampara, name='editar_lampara'),
    path('lamparas/<int:pk>/eliminar/', views.eliminar_lampara, name='eliminar_lampara'),
    
    # URLs de Macetas
    path('macetas/', views.lista_macetas, name='lista_macetas'),
    path('macetas/crear/', views.crear_maceta, name='crear_maceta'),
    path('macetas/<int:pk>/', views.detalle_maceta, name='detalle_maceta'),
    path('macetas/<int:pk>/editar/', views.editar_maceta, name='editar_maceta'),
    path('macetas/<int:pk>/eliminar/', views.eliminar_maceta, name='eliminar_maceta'),
    
    # URLs de Aditivos
    path('aditivos/', views.lista_aditivos, name='lista_aditivos'),
    path('aditivos/crear/', views.crear_aditivo, name='crear_aditivo'),
    path('aditivos/<int:pk>/', views.detalle_aditivo, name='detalle_aditivo'),
    path('aditivos/<int:pk>/editar/', views.editar_aditivo, name='editar_aditivo'),
    path('aditivos/<int:pk>/eliminar/', views.eliminar_aditivo, name='eliminar_aditivo'),
    
    # URLs de Bases
    path('bases/', views.lista_bases, name='lista_bases'),
    path('bases/crear/', views.crear_base, name='crear_base'),
    path('bases/<int:pk>/', views.detalle_base, name='detalle_base'),
    path('bases/<int:pk>/editar/', views.editar_base, name='editar_base'),
    path('bases/<int:pk>/eliminar/', views.eliminar_base, name='eliminar_base'),
    
    # URLs de Bancos
    path('bancos/', views.lista_bancos, name='lista_bancos'),
    path('bancos/crear/', views.crear_banco, name='crear_banco'),
    path('bancos/<int:pk>/', views.detalle_banco, name='detalle_banco'),
    path('bancos/<int:pk>/editar/', views.editar_banco, name='editar_banco'),
    path('bancos/<int:pk>/eliminar/', views.eliminar_banco, name='eliminar_banco'),
    
    # URLs de Terpenos
    path('terpenos/', views.lista_terpenos, name='lista_terpenos'),
    path('terpenos/crear/', views.crear_terpeno, name='crear_terpeno'),
    path('terpenos/<int:pk>/', views.detalle_terpeno, name='detalle_terpeno'),
    path('terpenos/<int:pk>/editar/', views.editar_terpeno, name='editar_terpeno'),
    path('terpenos/<int:pk>/eliminar/', views.eliminar_terpeno, name='eliminar_terpeno'),
    
    # URLs de Características
    path('caracteristicas/', views.lista_caracteristicas, name='lista_caracteristicas'),
    path('caracteristicas/crear/', views.crear_caracteristica, name='crear_caracteristica'),
    path('caracteristicas/<int:pk>/', views.detalle_caracteristica, name='detalle_caracteristica'),
    path('caracteristicas/<int:pk>/editar/', views.editar_caracteristica, name='editar_caracteristica'),
    path('caracteristicas/<int:pk>/eliminar/', views.eliminar_caracteristica, name='eliminar_caracteristica'),
]