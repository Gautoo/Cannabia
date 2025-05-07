# gestion_cultivo/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages

from .forms import SalaForm
from .forms import RegistroUsuarioForm # Importa el formulario de registro
from .models import Sala # Importa el modelo Sala

def pagina_inicio_cultivo(request):
    return render(request, 'gestion_cultivo/inicio_cultivo.html')

@login_required
def lista_salas(request):
    # Filtra las salas para que solo muestre las del usuario actualmente logueado
    # y las ordena por nombre.
    salas = Sala.objects.filter(usuario=request.user).order_by('nombre')
    context = {
        'salas': salas
    }
    return render(request, 'gestion_cultivo/lista_salas.html', context)

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Ahora estás logueado.')
            return redirect('gestion_cultivo:pagina_inicio_cultivo')
        else:
            messages.error(request, 'Hubo errores en el formulario. Por favor, corrígelos.')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'gestion_cultivo/registro_usuario.html', {'form': form})

@login_required # Solo usuarios logueados pueden crear salas
def crear_sala(request):
    if request.method == 'POST':
        # Si el formulario se ha enviado (es una petición POST)
        form = SalaForm(request.POST) # Crea una instancia del formulario con los datos enviados
        if form.is_valid(): # Verifica si los datos son válidos
            sala = form.save(commit=False) # No guardes el objeto Sala en la BD todavía
            sala.usuario = request.user # Asigna el usuario actual a la sala
            sala.save() # Ahora sí, guarda la sala en la BD
            messages.success(request, f"La sala '{sala.nombre}' ha sido creada exitosamente.")
            return redirect('gestion_cultivo:lista_salas') # Redirige a la lista de salas
        else:
            # Si el formulario no es válido, se mostrarán los errores en la plantilla.
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        # Si es una petición GET (el usuario acaba de llegar a la página),
        # crea una instancia vacía del formulario.
        form = SalaForm()

    # Pasa el formulario y un título de 'acción' a la plantilla
    context = {
        'form': form,
        'accion': 'Crear Nueva' # Para usar en el título y botón de la plantilla
    }
    return render(request, 'gestion_cultivo/crear_editar_sala.html', context)