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
]