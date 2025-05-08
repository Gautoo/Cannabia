# gestion_cultivo/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import (
    SalaForm, RegistroUsuarioForm, AreaCultivoForm, PlantaForm, 
    GeneticaForm, SemillaForm, FertilizanteForm, LamparaForm, 
    MacetaForm, AditivoForm, BaseForm, BancoForm, TerpenoForm, 
    CaracteristicaForm, MoverPlantaForm, MoverAreaForm
)
from .models import (
    Sala, AreaCultivo, Planta, Genetica, Semilla, Fertilizante,
    Lampara, Maceta, Aditivo, Base, Banco, Terpeno, Caracteristica
)

def pagina_inicio_cultivo(request):
    return render(request, 'gestion_cultivo/inicio_cultivo.html')

@login_required
def lista_salas(request):
    salas = Sala.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'gestion_cultivo/cultivo/salas/lista.html', {
        'salas': salas
    })

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!')
            return redirect('dashboard')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'gestion_cultivo/usuarios/registro.html', {'form': form})

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
    return render(request, 'gestion_cultivo/cultivo/salas/crear.html', context)

@login_required
def detalle_sala(request, pk):
    sala = get_object_or_404(Sala, pk=pk, usuario=request.user)
    areas = AreaCultivo.objects.filter(sala=sala).order_by('nombre')
    return render(request, 'gestion_cultivo/cultivo/salas/detalle.html', {
        'sala': sala,
        'areas': areas
    })

@login_required
def editar_sala(request, pk):
    sala = get_object_or_404(Sala, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = SalaForm(request.POST, instance=sala)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sala actualizada correctamente')
            return redirect('gestion_cultivo:detalle_sala', pk=sala.pk)
    else:
        form = SalaForm(instance=sala)
    return render(request, 'gestion_cultivo/cultivo/salas/editar.html', {
        'form': form,
        'sala': sala
    })

@login_required
def eliminar_sala(request, pk):
    sala = get_object_or_404(Sala, pk=pk, usuario=request.user)
    if request.method == 'POST':
        sala.delete()
        messages.success(request, 'Sala eliminada correctamente')
        return redirect('gestion_cultivo:lista_salas')
    return render(request, 'gestion_cultivo/cultivo/salas/eliminar.html', {
        'sala': sala
    })

# Vistas para el CRUD de Áreas de Cultivo
@login_required
def lista_areas(request):
    areas = AreaCultivo.objects.filter(sala__usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'gestion_cultivo/cultivo/areas/lista.html', {'areas': areas})

@login_required
def crear_area(request, sala_id):
    sala = get_object_or_404(Sala, pk=sala_id, usuario=request.user)
    if request.method == 'POST':
        form = AreaCultivoForm(request.POST)
        if form.is_valid():
            area = form.save(commit=False)
            area.sala = sala
            area.save()
            messages.success(request, 'Área de cultivo creada exitosamente')
            return redirect('gestion_cultivo:detalle_sala', pk=sala.pk)
    else:
        form = AreaCultivoForm()
    return render(request, 'gestion_cultivo/cultivo/areas/crear.html', {
        'form': form,
        'sala': sala
    })

@login_required
def detalle_area(request, pk):
    area = get_object_or_404(AreaCultivo, pk=pk, sala__usuario=request.user)
    plantas = Planta.objects.filter(area=area).order_by('nombre_id')
    return render(request, 'gestion_cultivo/cultivo/areas/detalle.html', {
        'area': area,
        'plantas': plantas
    })

@login_required
def editar_area(request, pk):
    area = get_object_or_404(AreaCultivo, pk=pk, sala__usuario=request.user)
    if request.method == 'POST':
        form = AreaCultivoForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            messages.success(request, 'Área actualizada correctamente')
            return redirect('gestion_cultivo:detalle_area', pk=area.pk)
    else:
        form = AreaCultivoForm(instance=area)
    return render(request, 'gestion_cultivo/cultivo/areas/editar.html', {
        'form': form,
        'area': area
    })

@login_required
def eliminar_area(request, pk):
    area = get_object_or_404(AreaCultivo, pk=pk, sala__usuario=request.user)
    if request.method == 'POST':
        area.delete()
        messages.success(request, 'Área eliminada correctamente')
        return redirect('gestion_cultivo:detalle_sala', pk=area.sala.pk)
    return render(request, 'gestion_cultivo/cultivo/areas/eliminar.html', {
        'area': area
    })

# Vistas para el CRUD de Plantas
@login_required
def crear_planta(request, area_id):
    area = get_object_or_404(AreaCultivo, pk=area_id, sala__usuario=request.user)
    if request.method == 'POST':
        form = PlantaForm(request.POST)
        if form.is_valid():
            planta = form.save(commit=False)
            planta.area = area
            planta.save()
            messages.success(request, 'Planta creada correctamente')
            return redirect('gestion_cultivo:detalle_area', pk=area.pk)
    else:
        form = PlantaForm()
    return render(request, 'gestion_cultivo/cultivo/plantas/crear.html', {
        'form': form,
        'area': area
    })

@login_required
def detalle_planta(request, pk):
    planta = get_object_or_404(Planta, pk=pk, area__sala__usuario=request.user)
    return render(request, 'gestion_cultivo/cultivo/plantas/detalle.html', {
        'planta': planta
    })

@login_required
def editar_planta(request, pk):
    planta = get_object_or_404(Planta, pk=pk, area__sala__usuario=request.user)
    if request.method == 'POST':
        form = PlantaForm(request.POST, instance=planta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Planta actualizada correctamente')
            return redirect('gestion_cultivo:detalle_planta', pk=planta.pk)
    else:
        form = PlantaForm(instance=planta)
    return render(request, 'gestion_cultivo/cultivo/plantas/editar.html', {
        'form': form,
        'planta': planta
    })

@login_required
def eliminar_planta(request, pk):
    planta = get_object_or_404(Planta, pk=pk, area__sala__usuario=request.user)
    if request.method == 'POST':
        planta.delete()
        messages.success(request, 'Planta eliminada correctamente')
        return redirect('gestion_cultivo:detalle_area', pk=planta.area.pk)
    return render(request, 'gestion_cultivo/cultivo/plantas/eliminar.html', {
        'planta': planta
    })

@login_required
def mover_planta(request, pk):
    planta = get_object_or_404(Planta, pk=pk, area__sala__usuario=request.user)
    if request.method == 'POST':
        form = MoverPlantaForm(request.POST, instance=planta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Planta movida correctamente')
            return redirect('gestion_cultivo:detalle_planta', pk=planta.pk)
    else:
        form = MoverPlantaForm(instance=planta)
    return render(request, 'gestion_cultivo/cultivo/plantas/mover.html', {
        'form': form,
        'planta': planta
    })

@login_required
def mover_area(request, pk):
    area = get_object_or_404(AreaCultivo, pk=pk, sala__usuario=request.user)
    if request.method == 'POST':
        form = MoverAreaForm(request.POST, instance=area)
        if form.is_valid():
            form.save()
            messages.success(request, 'Área movida correctamente')
            return redirect('gestion_cultivo:detalle_area', pk=area.pk)
    else:
        form = MoverAreaForm(instance=area)
    return render(request, 'gestion_cultivo/cultivo/areas/mover.html', {
        'form': form,
        'area': area
    })

# Vistas para el CRUD de Genéticas
@login_required
def lista_geneticas(request):
    geneticas = Genetica.objects.all().order_by('nombre')
    return render(request, 'gestion_cultivo/inventario/productos/geneticas/lista.html', {
        'geneticas': geneticas
    })

@login_required
def crear_genetica(request):
    if request.method == 'POST':
        form = GeneticaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Genética creada exitosamente.')
            return redirect('gestion_cultivo:lista_geneticas')
    else:
        form = GeneticaForm()
    return render(request, 'gestion_cultivo/inventario/productos/geneticas/crear.html', {'form': form})

@login_required
def detalle_genetica(request, pk):
    genetica = get_object_or_404(Genetica, pk=pk)
    return render(request, 'gestion_cultivo/inventario/productos/geneticas/detalle.html', {'genetica': genetica})

@login_required
def editar_genetica(request, pk):
    genetica = get_object_or_404(Genetica, pk=pk)
    if request.method == 'POST':
        form = GeneticaForm(request.POST, instance=genetica)
        if form.is_valid():
            form.save()
            messages.success(request, 'Genética actualizada exitosamente.')
            return redirect('gestion_cultivo:detalle_genetica', pk=genetica.pk)
    else:
        form = GeneticaForm(instance=genetica)
    return render(request, 'gestion_cultivo/inventario/productos/geneticas/editar.html', {'form': form})

@login_required
def eliminar_genetica(request, pk):
    genetica = get_object_or_404(Genetica, pk=pk)
    if request.method == 'POST':
        genetica.delete()
        messages.success(request, 'Genética eliminada exitosamente.')
        return redirect('gestion_cultivo:lista_geneticas')
    return render(request, 'gestion_cultivo/inventario/productos/geneticas/eliminar.html', {'genetica': genetica})

# Vistas para el CRUD de Semillas
@login_required
def lista_semillas(request):
    semillas = Semilla.objects.all().order_by('nombre')
    return render(request, 'gestion_cultivo/inventario/productos/semillas/lista.html', {
        'semillas': semillas
    })

@login_required
def crear_semilla(request):
    if request.method == 'POST':
        form = SemillaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Semilla creada exitosamente.')
            return redirect('gestion_cultivo:lista_semillas')
    else:
        form = SemillaForm()
    return render(request, 'gestion_cultivo/inventario/productos/semillas/crear.html', {
        'form': form
    })

@login_required
def detalle_semilla(request, semilla_id):
    semilla = get_object_or_404(Semilla, id=semilla_id)
    return render(request, 'gestion_cultivo/inventario/productos/semillas/detalle.html', {
        'semilla': semilla
    })

@login_required
def editar_semilla(request, semilla_id):
    semilla = get_object_or_404(Semilla, id=semilla_id)
    if request.method == 'POST':
        form = SemillaForm(request.POST, instance=semilla)
        if form.is_valid():
            form.save()
            messages.success(request, 'Semilla actualizada exitosamente.')
            return redirect('gestion_cultivo:detalle_semilla', semilla_id=semilla.id)
    else:
        form = SemillaForm(instance=semilla)
    return render(request, 'gestion_cultivo/inventario/productos/semillas/editar.html', {
        'form': form,
        'semilla': semilla
    })

@login_required
def eliminar_semilla(request, semilla_id):
    semilla = get_object_or_404(Semilla, id=semilla_id)
    if request.method == 'POST':
        semilla.delete()
        messages.success(request, 'Semilla eliminada exitosamente.')
        return redirect('gestion_cultivo:lista_semillas')
    return render(request, 'gestion_cultivo/inventario/productos/semillas/eliminar.html', {
        'semilla': semilla
    })

def lista_plantas_madre(request):
    plantas_madre = Planta.objects.filter(es_madre=True, activa=True).order_by('nombre_id')
    return render(request, 'gestion_cultivo/cultivo/plantas/lista_madre.html', {
        'plantas_madre': plantas_madre
    })

@login_required
def inventario(request):
    if not request.user.is_authenticated:
        return redirect('gestion_cultivo:login')
    
    # Obtener todos los productos
    semillas = Semilla.objects.filter(usuario=request.user)
    fertilizantes = Fertilizante.objects.filter(usuario=request.user)
    lamparas = Lampara.objects.filter(usuario=request.user)
    macetas = Maceta.objects.filter(usuario=request.user)
    
    # Calcular conteos
    conteos = {
        'semillas': semillas.count(),
        'fertilizantes': fertilizantes.count(),
        'lamparas': lamparas.count(),
        'macetas': macetas.count(),
    }
    
    context = {
        'semillas': semillas,
        'fertilizantes': fertilizantes,
        'lamparas': lamparas,
        'macetas': macetas,
        'conteos': conteos,
    }
    
    return render(request, 'gestion_cultivo/inventario/index.html', context)

@login_required
def agregar_item_inventario(request, tipo):
    if tipo == 'semilla':
        return redirect('gestion_cultivo:agregar_semilla')
    elif tipo == 'fertilizante':
        return redirect('gestion_cultivo:agregar_fertilizante')
    elif tipo == 'lampara':
        return redirect('gestion_cultivo:agregar_lampara')
    elif tipo == 'maceta':
        return redirect('gestion_cultivo:agregar_maceta')
    elif tipo == 'aditivo':
        return redirect('gestion_cultivo:agregar_aditivo')
    elif tipo == 'base':
        return redirect('gestion_cultivo:agregar_base')
    else:
        messages.error(request, 'Tipo de item no válido')
        return redirect('gestion_cultivo:inventario')

@login_required
def agregar_semilla(request):
    if request.method == 'POST':
        form = SemillaForm(request.POST)
        if form.is_valid():
            semilla = form.save()
            messages.success(request, 'Semilla agregada exitosamente.')
            return redirect('gestion_cultivo:detalle_item_inventario', tipo='semilla', pk=semilla.id)
    else:
        form = SemillaForm()
    return render(request, 'gestion_cultivo/inventario/productos/semillas/crear.html', {'form': form})

@login_required
def agregar_banco(request):
    if request.method == 'POST':
        form = BancoForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return render(request, 'gestion_cultivo/inventario/productos/semillas/bancos/crear.html', {'form': BancoForm()})

@login_required
def agregar_terpeno(request):
    if request.method == 'POST':
        form = TerpenoForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return render(request, 'gestion_cultivo/inventario/productos/semillas/terpenos/crear.html', {'form': TerpenoForm()})

@login_required
def agregar_caracteristica(request):
    if request.method == 'POST':
        form = CaracteristicaForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'errors': form.errors})
    return render(request, 'gestion_cultivo/inventario/productos/semillas/caracteristicas/crear.html', {'form': CaracteristicaForm()})

@login_required
def agregar_lampara(request):
    if request.method == 'POST':
        form = LamparaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lámpara creada exitosamente.')
            return redirect('gestion_cultivo:lista_lamparas')
    else:
        form = LamparaForm()
    return render(request, 'gestion_cultivo/inventario/productos/lamparas/crear.html', {'form': form})

@login_required
def agregar_maceta(request):
    if request.method == 'POST':
        form = MacetaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Maceta creada exitosamente.')
            return redirect('gestion_cultivo:lista_macetas')
    else:
        form = MacetaForm()
    return render(request, 'gestion_cultivo/inventario/productos/macetas/crear.html', {'form': form})

@login_required
def agregar_fertilizante(request):
    if request.method == 'POST':
        form = FertilizanteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fertilizante creado exitosamente.')
            return redirect('gestion_cultivo:lista_fertilizantes')
    else:
        form = FertilizanteForm()
    return render(request, 'gestion_cultivo/inventario/productos/fertilizantes/crear.html', {'form': form})

@login_required
def agregar_aditivo(request):
    if request.method == 'POST':
        form = AditivoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aditivo creado exitosamente.')
            return redirect('gestion_cultivo:lista_aditivos')
    else:
        form = AditivoForm()
    return render(request, 'gestion_cultivo/inventario/productos/para_sustrato/crear.html', {'form': form})

@login_required
def agregar_base(request):
    if request.method == 'POST':
        form = BaseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Base creada exitosamente.')
            return redirect('gestion_cultivo:lista_bases')
    else:
        form = BaseForm()
    return render(request, 'gestion_cultivo/inventario/productos/sustratos/crear.html', {'form': form})

@login_required
def detalle_item_inventario(request, tipo, pk):
    # Mapeo de tipos a modelos
    modelos = {
        'semilla': Semilla,
        'fertilizante': Fertilizante,
        'lampara': Lampara,
        'maceta': Maceta,
        'aditivo': Aditivo,
        'base': Base,
    }
    
    if tipo not in modelos:
        messages.error(request, 'Tipo de item no válido')
        return redirect('gestion_cultivo:inventario')
    
    modelo = modelos[tipo]
    item = get_object_or_404(modelo, pk=pk)
    
    return render(request, f'gestion_cultivo/inventario/productos/{tipo}s/detalle.html', {
        'item': item,
        'tipo': tipo
    })

@login_required
def editar_item_inventario(request, tipo, pk):
    # Mapeo de tipos a modelos y formularios
    modelos = {
        'semilla': (Semilla, SemillaForm),
        'fertilizante': (Fertilizante, FertilizanteForm),
        'lampara': (Lampara, LamparaForm),
        'maceta': (Maceta, MacetaForm),
        'aditivo': (Aditivo, AditivoForm),
        'base': (Base, BaseForm),
    }
    
    if tipo not in modelos:
        messages.error(request, 'Tipo de item no válido')
        return redirect('gestion_cultivo:inventario')
    
    modelo, formulario = modelos[tipo]
    item = get_object_or_404(modelo, pk=pk)
    
    if request.method == 'POST':
        form = formulario(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f'{tipo.capitalize()} actualizado exitosamente.')
            return redirect('gestion_cultivo:detalle_item_inventario', tipo=tipo, pk=item.id)
    else:
        form = formulario(instance=item)
    
    return render(request, f'gestion_cultivo/inventario/productos/{tipo}s/editar.html', {
        'form': form,
        'item': item,
        'tipo': tipo
    })

@login_required
def eliminar_item_inventario(request, tipo, pk):
    # Mapeo de tipos a modelos
    modelos = {
        'semilla': Semilla,
        'fertilizante': Fertilizante,
        'lampara': Lampara,
        'maceta': Maceta,
        'aditivo': Aditivo,
        'base': Base,
    }
    
    if tipo not in modelos:
        messages.error(request, 'Tipo de item no válido')
        return redirect('gestion_cultivo:inventario')
    
    modelo = modelos[tipo]
    item = get_object_or_404(modelo, pk=pk)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, f'{tipo.capitalize()} eliminado exitosamente.')
        return redirect('gestion_cultivo:inventario')
    
    return render(request, f'gestion_cultivo/inventario/productos/{tipo}s/eliminar.html', {
        'item': item,
        'tipo': tipo
    })

@login_required
def login_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, '¡Bienvenido!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'gestion_cultivo/login.html')

def logout_usuario(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión')
    return redirect('login_usuario')

@login_required
def dashboard(request):
    # Obtener conteos
    salas_count = Sala.objects.filter(usuario=request.user).count()
    areas_count = AreaCultivo.objects.filter(sala__usuario=request.user).count()
    plantas_count = Planta.objects.filter(area__sala__usuario=request.user).count()
    plantas_madre_count = Planta.objects.filter(area__sala__usuario=request.user, es_madre=True).count()
    
    # Obtener últimas plantas
    ultimas_plantas = Planta.objects.filter(
        area__sala__usuario=request.user
    ).select_related('area').order_by('-fecha_creacion')[:5]
    
    context = {
        'salas_count': salas_count,
        'areas_count': areas_count,
        'plantas_count': plantas_count,
        'plantas_madre_count': plantas_madre_count,
        'ultimas_plantas': ultimas_plantas,
    }
    
    return render(request, 'gestion_cultivo/dashboard.html', context)

@login_required
def cultivo(request):
    return render(request, 'gestion_cultivo/cultivo.html')

@login_required
def configuracion(request):
    return render(request, 'gestion_cultivo/configuracion.html')

@login_required
def lista_plantas(request):
    plantas = Planta.objects.filter(area__sala__usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'gestion_cultivo/cultivo/plantas/lista.html', {'plantas': plantas})

@login_required
def lista_fertilizantes(request):
    fertilizantes = Fertilizante.objects.all()
    return render(request, 'gestion_cultivo/inventario/productos/fertilizantes/lista.html', {'fertilizantes': fertilizantes})

@login_required
def crear_fertilizante(request):
    if request.method == 'POST':
        form = FertilizanteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fertilizante creado exitosamente.')
            return redirect('gestion_cultivo:lista_fertilizantes')
    else:
        form = FertilizanteForm()
    return render(request, 'gestion_cultivo/inventario/productos/fertilizantes/crear.html', {'form': form})

@login_required
def detalle_fertilizante(request, fertilizante_id):
    fertilizante = get_object_or_404(Fertilizante, id=fertilizante_id)
    return render(request, 'gestion_cultivo/inventario/productos/fertilizantes/detalle.html', {'fertilizante': fertilizante})

@login_required
def editar_fertilizante(request, fertilizante_id):
    fertilizante = get_object_or_404(Fertilizante, id=fertilizante_id)
    if request.method == 'POST':
        form = FertilizanteForm(request.POST, instance=fertilizante)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fertilizante actualizado exitosamente')
            return redirect('lista_fertilizantes')
    else:
        form = FertilizanteForm(instance=fertilizante)
    return render(request, 'gestion_cultivo/inventario/productos/fertilizantes/editar.html', {'form': form, 'fertilizante': fertilizante})

@login_required
def eliminar_fertilizante(request, fertilizante_id):
    fertilizante = get_object_or_404(Fertilizante, id=fertilizante_id)
    if request.method == 'POST':
        fertilizante.delete()
        messages.success(request, 'Fertilizante eliminado exitosamente')
        return redirect('lista_fertilizantes')
    return render(request, 'gestion_cultivo/inventario/productos/fertilizantes/eliminar.html', {'fertilizante': fertilizante})

@login_required
def lista_lamparas(request):
    lamparas = Lampara.objects.all()
    return render(request, 'gestion_cultivo/inventario/productos/lamparas/lista.html', {'lamparas': lamparas})

@login_required
def crear_lampara(request):
    if request.method == 'POST':
        form = LamparaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lámpara creada exitosamente.')
            return redirect('gestion_cultivo:lista_lamparas')
    else:
        form = LamparaForm()
    return render(request, 'gestion_cultivo/inventario/productos/lamparas/crear.html', {'form': form})

@login_required
def detalle_lampara(request, lampara_id):
    lampara = get_object_or_404(Lampara, id=lampara_id)
    return render(request, 'gestion_cultivo/inventario/productos/lamparas/detalle.html', {'lampara': lampara})

@login_required
def editar_lampara(request, lampara_id):
    lampara = get_object_or_404(Lampara, id=lampara_id)
    if request.method == 'POST':
        form = LamparaForm(request.POST, instance=lampara)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lámpara actualizada exitosamente')
            return redirect('lista_lamparas')
    else:
        form = LamparaForm(instance=lampara)
    return render(request, 'gestion_cultivo/inventario/productos/lamparas/editar.html', {'form': form, 'lampara': lampara})

@login_required
def eliminar_lampara(request, lampara_id):
    lampara = get_object_or_404(Lampara, id=lampara_id)
    if request.method == 'POST':
        lampara.delete()
        messages.success(request, 'Lámpara eliminada exitosamente')
        return redirect('lista_lamparas')
    return render(request, 'gestion_cultivo/inventario/productos/lamparas/eliminar.html', {'lampara': lampara})

@login_required
def lista_macetas(request):
    macetas = Maceta.objects.all()
    return render(request, 'gestion_cultivo/inventario/productos/macetas/lista.html', {'macetas': macetas})

@login_required
def crear_maceta(request):
    if request.method == 'POST':
        form = MacetaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Maceta creada exitosamente.')
            return redirect('gestion_cultivo:lista_macetas')
    else:
        form = MacetaForm()
    return render(request, 'gestion_cultivo/inventario/productos/macetas/crear.html', {'form': form})

@login_required
def detalle_maceta(request, maceta_id):
    maceta = get_object_or_404(Maceta, id=maceta_id)
    return render(request, 'gestion_cultivo/inventario/productos/macetas/detalle.html', {'maceta': maceta})

@login_required
def editar_maceta(request, maceta_id):
    maceta = get_object_or_404(Maceta, id=maceta_id)
    if request.method == 'POST':
        form = MacetaForm(request.POST, instance=maceta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Maceta actualizada exitosamente')
            return redirect('lista_macetas')
    else:
        form = MacetaForm(instance=maceta)
    return render(request, 'gestion_cultivo/inventario/productos/macetas/editar.html', {'form': form, 'maceta': maceta})

@login_required
def eliminar_maceta(request, maceta_id):
    maceta = get_object_or_404(Maceta, id=maceta_id)
    if request.method == 'POST':
        maceta.delete()
        messages.success(request, 'Maceta eliminada exitosamente')
        return redirect('lista_macetas')
    return render(request, 'gestion_cultivo/inventario/productos/macetas/eliminar.html', {'maceta': maceta})

@login_required
def lista_aditivos(request):
    aditivos = Aditivo.objects.all()
    return render(request, 'gestion_cultivo/inventario/productos/para_sustrato/lista.html', {'aditivos': aditivos})

@login_required
def crear_aditivo(request):
    if request.method == 'POST':
        form = AditivoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aditivo creado exitosamente.')
            return redirect('gestion_cultivo:lista_aditivos')
    else:
        form = AditivoForm()
    return render(request, 'gestion_cultivo/inventario/productos/para_sustrato/crear.html', {'form': form})

@login_required
def detalle_aditivo(request, aditivo_id):
    aditivo = get_object_or_404(Aditivo, id=aditivo_id)
    return render(request, 'gestion_cultivo/inventario/productos/para_sustrato/detalle.html', {'aditivo': aditivo})

@login_required
def editar_aditivo(request, aditivo_id):
    aditivo = get_object_or_404(Aditivo, id=aditivo_id)
    if request.method == 'POST':
        form = AditivoForm(request.POST, instance=aditivo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aditivo actualizado exitosamente')
            return redirect('lista_aditivos')
    else:
        form = AditivoForm(instance=aditivo)
    return render(request, 'gestion_cultivo/inventario/productos/para_sustrato/editar.html', {'form': form, 'aditivo': aditivo})

@login_required
def eliminar_aditivo(request, aditivo_id):
    aditivo = get_object_or_404(Aditivo, id=aditivo_id)
    if request.method == 'POST':
        aditivo.delete()
        messages.success(request, 'Aditivo eliminado exitosamente')
        return redirect('lista_aditivos')
    return render(request, 'gestion_cultivo/inventario/productos/para_sustrato/eliminar.html', {'aditivo': aditivo})

@login_required
def lista_bases(request):
    bases = Base.objects.all()
    return render(request, 'gestion_cultivo/inventario/productos/sustratos/lista.html', {'bases': bases})

@login_required
def crear_base(request):
    if request.method == 'POST':
        form = BaseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Base creada exitosamente.')
            return redirect('gestion_cultivo:lista_bases')
    else:
        form = BaseForm()
    return render(request, 'gestion_cultivo/inventario/productos/sustratos/crear.html', {'form': form})

@login_required
def detalle_base(request, base_id):
    base = get_object_or_404(Base, id=base_id)
    return render(request, 'gestion_cultivo/inventario/productos/sustratos/detalle.html', {'base': base})

@login_required
def editar_base(request, base_id):
    base = get_object_or_404(Base, id=base_id)
    if request.method == 'POST':
        form = BaseForm(request.POST, instance=base)
        if form.is_valid():
            form.save()
            messages.success(request, 'Base actualizada exitosamente')
            return redirect('lista_bases')
    else:
        form = BaseForm(instance=base)
    return render(request, 'gestion_cultivo/inventario/productos/sustratos/editar.html', {'form': form, 'base': base})

@login_required
def eliminar_base(request, base_id):
    base = get_object_or_404(Base, id=base_id)
    if request.method == 'POST':
        base.delete()
        messages.success(request, 'Base eliminada exitosamente')
        return redirect('lista_bases')
    return render(request, 'gestion_cultivo/inventario/productos/sustratos/eliminar.html', {'base': base})

@login_required
def lista_bancos(request):
    bancos = Banco.objects.all()
    return render(request, 'gestion_cultivo/inventario/productos/semillas/bancos/lista.html', {'bancos': bancos})

@login_required
def crear_banco(request):
    if request.method == 'POST':
        form = BancoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Banco creado exitosamente.')
            return redirect('gestion_cultivo:lista_bancos')
    else:
        form = BancoForm()
    return render(request, 'gestion_cultivo/inventario/productos/semillas/bancos/crear.html', {'form': form})

@login_required
def detalle_banco(request, banco_id):
    banco = get_object_or_404(Banco, id=banco_id)
    return render(request, 'gestion_cultivo/inventario/productos/semillas/bancos/detalle.html', {'banco': banco})

@login_required
def editar_banco(request, banco_id):
    banco = get_object_or_404(Banco, id=banco_id)
    if request.method == 'POST':
        form = BancoForm(request.POST, instance=banco)
        if form.is_valid():
            form.save()
            messages.success(request, 'Banco actualizado exitosamente')
            return redirect('lista_bancos')
    else:
        form = BancoForm(instance=banco)
    return render(request, 'gestion_cultivo/inventario/productos/semillas/bancos/editar.html', {'form': form, 'banco': banco})

@login_required
def eliminar_banco(request, banco_id):
    banco = get_object_or_404(Banco, id=banco_id)
    if request.method == 'POST':
        banco.delete()
        messages.success(request, 'Banco eliminado exitosamente')
        return redirect('lista_bancos')
    return render(request, 'gestion_cultivo/inventario/productos/semillas/bancos/eliminar.html', {'banco': banco})

@login_required
def lista_terpenos(request):
    terpenos = Terpeno.objects.all()
    return render(request, 'gestion_cultivo/inventario/productos/semillas/terpenos/lista.html', {'terpenos': terpenos})

@login_required
def crear_terpeno(request):
    if request.method == 'POST':
        form = TerpenoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Terpeno creado exitosamente.')
            return redirect('gestion_cultivo:lista_terpenos')
    else:
        form = TerpenoForm()
    return render(request, 'gestion_cultivo/inventario/productos/semillas/terpenos/crear.html', {'form': form})

@login_required
def detalle_terpeno(request, terpeno_id):
    terpeno = get_object_or_404(Terpeno, id=terpeno_id)
    return render(request, 'gestion_cultivo/inventario/productos/semillas/terpenos/detalle.html', {'terpeno': terpeno})

@login_required
def editar_terpeno(request, terpeno_id):
    terpeno = get_object_or_404(Terpeno, id=terpeno_id)
    if request.method == 'POST':
        form = TerpenoForm(request.POST, instance=terpeno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Terpeno actualizado exitosamente')
            return redirect('lista_terpenos')
    else:
        form = TerpenoForm(instance=terpeno)
    return render(request, 'gestion_cultivo/inventario/productos/semillas/terpenos/editar.html', {'form': form, 'terpeno': terpeno})

@login_required
def eliminar_terpeno(request, terpeno_id):
    terpeno = get_object_or_404(Terpeno, id=terpeno_id)
    if request.method == 'POST':
        terpeno.delete()
        messages.success(request, 'Terpeno eliminado exitosamente')
        return redirect('lista_terpenos')
    return render(request, 'gestion_cultivo/inventario/productos/semillas/terpenos/eliminar.html', {'terpeno': terpeno})

@login_required
def lista_caracteristicas(request):
    caracteristicas = Caracteristica.objects.all()
    return render(request, 'gestion_cultivo/inventario/productos/semillas/caracteristicas/lista.html', {'caracteristicas': caracteristicas})

@login_required
def crear_caracteristica(request):
    if request.method == 'POST':
        form = CaracteristicaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Característica creada exitosamente.')
            return redirect('gestion_cultivo:lista_caracteristicas')
    else:
        form = CaracteristicaForm()
    return render(request, 'gestion_cultivo/inventario/productos/semillas/caracteristicas/crear.html', {'form': form})

@login_required
def detalle_caracteristica(request, caracteristica_id):
    caracteristica = get_object_or_404(Caracteristica, id=caracteristica_id)
    return render(request, 'gestion_cultivo/inventario/productos/semillas/caracteristicas/detalle.html', {'caracteristica': caracteristica})

@login_required
def editar_caracteristica(request, caracteristica_id):
    caracteristica = get_object_or_404(Caracteristica, id=caracteristica_id)
    if request.method == 'POST':
        form = CaracteristicaForm(request.POST, instance=caracteristica)
        if form.is_valid():
            form.save()
            messages.success(request, 'Característica actualizada exitosamente')
            return redirect('lista_caracteristicas')
    else:
        form = CaracteristicaForm(instance=caracteristica)
    return render(request, 'gestion_cultivo/inventario/productos/semillas/caracteristicas/editar.html', {'form': form, 'caracteristica': caracteristica})

@login_required
def eliminar_caracteristica(request, caracteristica_id):
    caracteristica = get_object_or_404(Caracteristica, id=caracteristica_id)
    if request.method == 'POST':
        caracteristica.delete()
        messages.success(request, 'Característica eliminada exitosamente')
        return redirect('lista_caracteristicas')
    return render(request, 'gestion_cultivo/inventario/productos/semillas/caracteristicas/eliminar.html', {'caracteristica': caracteristica})