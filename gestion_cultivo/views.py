# gestion_cultivo/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from .forms import SalaForm, RegistroUsuarioForm
from .models import Sala, AreaCultivo, Planta

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

@login_required
def crear_sala(request):
    if request.method == 'POST':
        form = SalaForm(request.POST)
        if form.is_valid():
            sala = form.save(commit=False)
            sala.usuario = request.user
            sala.save()
            messages.success(request, f"La sala '{sala.nombre}' ha sido creada exitosamente.")
            return redirect('gestion_cultivo:lista_salas')
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = SalaForm()

    context = {
        'form': form,
        'accion': 'Crear Nueva'
    }
    return render(request, 'gestion_cultivo/crear_editar_sala.html', context)

@login_required
def detalle_sala(request, sala_id):
    # Obtiene la sala específica o devuelve un 404 si no existe
    sala = get_object_or_404(Sala, id=sala_id, usuario=request.user)
    # Obtiene todas las áreas de cultivo asociadas a esta sala
    areas = sala.areas.all().order_by('nombre')
    
    context = {
        'sala': sala,
        'areas': areas
    }
    return render(request, 'gestion_cultivo/detalle_sala.html', context)

@login_required
def editar_sala(request, sala_id):
    # Obtiene la sala a editar (solo si pertenece al usuario actual)
    sala = get_object_or_404(Sala, id=sala_id, usuario=request.user)
    
    if request.method == 'POST':
        form = SalaForm(request.POST, instance=sala)  # Crea un formulario con los datos existentes
        if form.is_valid():
            form.save()  # Guarda los cambios
            messages.success(request, f"La sala '{sala.nombre}' ha sido actualizada exitosamente.")
            return redirect('gestion_cultivo:detalle_sala', sala_id=sala.id)
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = SalaForm(instance=sala)  # Crea un formulario prellenado con los datos de la sala
    
    context = {
        'form': form,
        'accion': 'Editar',
        'sala': sala
    }
    return render(request, 'gestion_cultivo/crear_editar_sala.html', context)

@login_required
def eliminar_sala(request, sala_id):
    # Obtiene la sala a eliminar (solo si pertenece al usuario actual)
    sala = get_object_or_404(Sala, id=sala_id, usuario=request.user)
    
    if request.method == 'POST':
        nombre_sala = sala.nombre
        sala.delete()
        messages.success(request, f"La sala '{nombre_sala}' ha sido eliminada exitosamente.")
        return redirect('gestion_cultivo:lista_salas')
    
    context = {
        'sala': sala
    }
    return render(request, 'gestion_cultivo/confirmar_eliminar.html', context)