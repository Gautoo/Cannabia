# gestion_cultivo/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

from .forms import SalaForm, RegistroUsuarioForm, AreaCultivoForm, PlantaForm, GeneticaForm
from .models import Sala, AreaCultivo, Planta, Genetica

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
    # Obtiene la sala o devuelve 404 si no existe
    sala = get_object_or_404(Sala, id=sala_id, usuario=request.user)
    # Obtiene las áreas de cultivo de esta sala
    areas = sala.areas.all().order_by('nombre')
    
    context = {
        'sala': sala,
        'areas': areas
    }
    return render(request, 'gestion_cultivo/detalle_sala.html', context)

@login_required
def editar_sala(request, sala_id):
    # Obtiene la sala o devuelve 404 si no existe
    sala = get_object_or_404(Sala, id=sala_id, usuario=request.user)
    
    if request.method == 'POST':
        form = SalaForm(request.POST, instance=sala)
        if form.is_valid():
            form.save()
            messages.success(request, f"La sala '{sala.nombre}' ha sido actualizada exitosamente.")
            return redirect('gestion_cultivo:detalle_sala', sala_id=sala.id)
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = SalaForm(instance=sala)
    
    context = {
        'form': form,
        'sala': sala
    }
    return render(request, 'gestion_cultivo/editar_sala.html', context)

@login_required
def eliminar_sala(request, sala_id):
    # Obtiene la sala o devuelve 404 si no existe
    sala = get_object_or_404(Sala, id=sala_id, usuario=request.user)
    
    if request.method == 'POST':
        nombre_sala = sala.nombre
        sala.delete()
        messages.success(request, f"La sala '{nombre_sala}' ha sido eliminada exitosamente.")
        return redirect('gestion_cultivo:lista_salas')
    
    context = {
        'sala': sala
    }
    return render(request, 'gestion_cultivo/eliminar_sala.html', context)

# Vistas para el CRUD de Áreas de Cultivo
@login_required
def crear_area(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    
    if request.method == 'POST':
        form = AreaCultivoForm(request.POST)
        if form.is_valid():
            area = form.save(commit=False)
            area.sala = sala
            area.save()
            messages.success(request, 'Área creada exitosamente.')
            return redirect('gestion_cultivo:detalle_sala', sala_id=sala.id)
    else:
        form = AreaCultivoForm()
    
    return render(request, 'gestion_cultivo/crear_area.html', {
        'form': form,
        'sala': sala
    })

@login_required
def detalle_area(request, area_id):
    area = get_object_or_404(AreaCultivo, id=area_id)
    plantas = area.planta_set.all().order_by('nombre_id')
    return render(request, 'gestion_cultivo/detalle_area.html', {
        'area': area,
        'plantas': plantas
    })

@login_required
def editar_area(request, area_id):
    # Obtiene el área o devuelve 404 si no existe
    area = get_object_or_404(AreaCultivo, id=area_id, sala__usuario=request.user)
    
    if request.method == 'POST':
        form = AreaCultivoForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            messages.success(request, f"El área '{area.nombre}' ha sido actualizada exitosamente.")
            return redirect('gestion_cultivo:detalle_area', area_id=area.id)
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = AreaCultivoForm(instance=area)
    
    context = {
        'form': form,
        'area': area,
        'sala': area.sala
    }
    return render(request, 'gestion_cultivo/editar_area.html', context)

@login_required
def eliminar_area(request, area_id):
    # Obtiene el área o devuelve 404 si no existe
    area = get_object_or_404(AreaCultivo, id=area_id, sala__usuario=request.user)
    
    if request.method == 'POST':
        nombre_area = area.nombre
        sala_id = area.sala.id
        area.delete()
        messages.success(request, f"El área '{nombre_area}' ha sido eliminada exitosamente.")
        return redirect('gestion_cultivo:detalle_sala', sala_id=sala_id)
    
    context = {
        'area': area,
        'sala': area.sala
    }
    return render(request, 'gestion_cultivo/eliminar_area.html', context)

# Vistas para el CRUD de Plantas
@login_required
def crear_planta(request, area_id):
    # Obtiene el área o devuelve 404 si no existe
    area = get_object_or_404(AreaCultivo, id=area_id, sala__usuario=request.user)
    
    if request.method == 'POST':
        form = PlantaForm(request.POST)
        if form.is_valid():
            planta = form.save(commit=False)
            planta.area = area
            planta.save()
            messages.success(request, f"La planta '{planta.nombre_id}' ha sido creada exitosamente.")
            return redirect('gestion_cultivo:detalle_area', area_id=area.id)
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = PlantaForm()
    
    context = {
        'form': form,
        'area': area,
        'sala': area.sala
    }
    return render(request, 'gestion_cultivo/crear_planta.html', context)

@login_required
def detalle_planta(request, planta_id):
    # Obtiene la planta o devuelve 404 si no existe
    planta = get_object_or_404(Planta, id=planta_id, area__sala__usuario=request.user)
    
    context = {
        'planta': planta,
        'area': planta.area,
        'sala': planta.area.sala
    }
    return render(request, 'gestion_cultivo/detalle_planta.html', context)

@login_required
def editar_planta(request, planta_id):
    # Obtiene la planta o devuelve 404 si no existe
    planta = get_object_or_404(Planta, id=planta_id, area__sala__usuario=request.user)
    
    if request.method == 'POST':
        form = PlantaForm(request.POST, instance=planta)
        if form.is_valid():
            form.save()
            messages.success(request, f"La planta '{planta.nombre_id}' ha sido actualizada exitosamente.")
            return redirect('gestion_cultivo:detalle_planta', planta_id=planta.id)
        else:
            messages.error(request, "Por favor, corrige los errores en el formulario.")
    else:
        form = PlantaForm(instance=planta)
    
    context = {
        'form': form,
        'planta': planta,
        'area': planta.area,
        'sala': planta.area.sala
    }
    return render(request, 'gestion_cultivo/editar_planta.html', context)

@login_required
def eliminar_planta(request, planta_id):
    # Obtiene la planta o devuelve 404 si no existe
    planta = get_object_or_404(Planta, id=planta_id, area__sala__usuario=request.user)
    
    if request.method == 'POST':
        nombre_planta = planta.nombre_id
        area_id = planta.area.id
        planta.delete()
        messages.success(request, f"La planta '{nombre_planta}' ha sido eliminada exitosamente.")
        return redirect('gestion_cultivo:detalle_area', area_id=area_id)
    
    context = {
        'planta': planta,
        'area': planta.area,
        'sala': planta.area.sala
    }
    return render(request, 'gestion_cultivo/eliminar_planta.html', context)

# Vistas para el CRUD de Genéticas
@login_required
def lista_geneticas(request):
    geneticas = Genetica.objects.all().order_by('nombre')
    return render(request, 'gestion_cultivo/lista_geneticas.html', {
        'geneticas': geneticas
    })

@login_required
def crear_genetica(request):
    if request.method == 'POST':
        form = GeneticaForm(request.POST)
        if form.is_valid():
            genetica = form.save()
            messages.success(request, 'Genética creada exitosamente.')
            return redirect('gestion_cultivo:detalle_genetica', genetica_id=genetica.id)
    else:
        form = GeneticaForm()
    
    return render(request, 'gestion_cultivo/crear_genetica.html', {
        'form': form
    })

@login_required
def detalle_genetica(request, genetica_id):
    genetica = get_object_or_404(Genetica, id=genetica_id)
    plantas = Planta.objects.filter(genetica=genetica)
    return render(request, 'gestion_cultivo/detalle_genetica.html', {
        'genetica': genetica,
        'plantas': plantas
    })

@login_required
def editar_genetica(request, genetica_id):
    genetica = get_object_or_404(Genetica, id=genetica_id)
    if request.method == 'POST':
        form = GeneticaForm(request.POST, instance=genetica)
        if form.is_valid():
            form.save()
            messages.success(request, 'Genética actualizada exitosamente.')
            return redirect('gestion_cultivo:detalle_genetica', genetica_id=genetica.id)
    else:
        form = GeneticaForm(instance=genetica)
    
    return render(request, 'gestion_cultivo/editar_genetica.html', {
        'form': form,
        'genetica': genetica
    })

@login_required
def eliminar_genetica(request, genetica_id):
    genetica = get_object_or_404(Genetica, id=genetica_id)
    if request.method == 'POST':
        genetica.delete()
        messages.success(request, 'Genética eliminada exitosamente.')
        return redirect('gestion_cultivo:lista_geneticas')
    
    return render(request, 'gestion_cultivo/eliminar_genetica.html', {
        'genetica': genetica
    })