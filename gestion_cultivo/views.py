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
from django.db.models import Q, Sum
from django.contrib.auth.forms import UserCreationForm

from .forms import (
    SalaForm, UsuarioForm, AreaCultivoForm, PlantaForm, 
    SemillaForm, FertilizanteForm, ContenedorForm, MaquinariaForm, StockForm,
    GeneticaForm, BancoForm, TerpenoForm, CaracteristicaForm,
    MoverPlantaForm, MoverAreaForm
)
from .models import (
    Sala, AreaCultivo, Planta, Genetica, Semilla, Fertilizante,
    Banco, Terpeno, Caracteristica, Contenedor, Maquinaria, Stock, PresentacionFertilizante
)

@login_required
def pagina_inicio_cultivo(request):
    salas = Sala.objects.filter(usuario=request.user)
    return render(request, 'gestion_cultivo/inicio_cultivo.html', {'salas': salas})

@login_required
def lista_salas(request):
    salas = Sala.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'gestion_cultivo/cultivo/salas/lista.html', {
        'salas': salas
    })

def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a Mi Cultivo App.')
            return redirect('gestion_cultivo:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registro.html', {'form': form})

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

@login_required
def dashboard(request):
    # Contadores para el cultivo
    salas_count = Sala.objects.filter(usuario=request.user).count()
    areas_count = AreaCultivo.objects.filter(sala__usuario=request.user).count()
    plantas_count = Planta.objects.filter(area__sala__usuario=request.user).count()
    
    # Contadores para el inventario
    semillas_count = Semilla.objects.count()  # No tiene campo usuario
    fertilizantes_count = Fertilizante.objects.count()  # No tiene campo usuario
    contenedores_count = Contenedor.objects.filter(usuario=request.user).count()
    maquinaria_count = Maquinaria.objects.filter(usuario=request.user).count()
    
    # Obtener plantas activas
    plantas_activas = Planta.objects.filter(
        area__sala__usuario=request.user,
        activa=True
    ).select_related('area', 'area__sala')

    # Obtener áreas de cultivo
    areas = AreaCultivo.objects.filter(
        sala__usuario=request.user
    ).select_related('sala')

    # Obtener salas
    salas = Sala.objects.filter(usuario=request.user)
    
    context = {
        'salas_count': salas_count,
        'areas_count': areas_count,
        'plantas_count': plantas_count,
        'semillas_count': semillas_count,
        'fertilizantes_count': fertilizantes_count,
        'contenedores_count': contenedores_count,
        'maquinaria_count': maquinaria_count,
        'plantas_activas': plantas_activas,
        'areas': areas,
        'salas': salas,
    }
    return render(request, 'gestion_cultivo/dashboard.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('gestion_cultivo:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'gestion_cultivo/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('gestion_cultivo:login')

def registro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('gestion_cultivo:dashboard')
    else:
        form = UsuarioForm()
    return render(request, 'gestion_cultivo/registro.html', {'form': form})

@login_required
def configuracion(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Configuración actualizada correctamente')
            return redirect('gestion_cultivo:configuracion')
    else:
        form = UsuarioForm(instance=request.user)
    return render(request, 'gestion_cultivo/configuracion.html', {'form': form})

# Vistas de Inventario
@login_required
def inventario(request):
    semillas = Semilla.objects.all()  # No tiene campo usuario
    fertilizantes = Fertilizante.objects.all()  # No tiene campo usuario
    contenedores = Contenedor.objects.filter(usuario=request.user)
    maquinaria = Maquinaria.objects.filter(usuario=request.user)
    
    context = {
        'semillas': semillas,
        'fertilizantes': fertilizantes,
        'contenedores': contenedores,
        'maquinaria': maquinaria,
    }
    return render(request, 'gestion_cultivo/inventario/index.html', context)

@login_required
def agregar_stock(request):
    if request.method == 'POST':
        form = StockForm(request.user, request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.usuario = request.user
            stock.save()
            messages.success(request, 'Stock agregado correctamente')
            return redirect('gestion_cultivo:inventario')
    else:
        form = StockForm(request.user)
    return render(request, 'gestion_cultivo/inventario/agregar_stock.html', {'form': form})

@login_required
def editar_stock(request, pk):
    stock = get_object_or_404(Stock, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = StockForm(request.user, request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock actualizado correctamente')
            return redirect('gestion_cultivo:inventario')
    else:
        form = StockForm(request.user, instance=stock)
    return render(request, 'gestion_cultivo/inventario/editar_stock.html', {'form': form})

@login_required
def nuevo_producto(request):
    return render(request, 'gestion_cultivo/inventario/nuevo_producto.html')

# Vistas de Semillas
@login_required
def lista_semillas(request):
    semillas = Semilla.objects.all()  # No tiene campo usuario
    return render(request, 'gestion_cultivo/inventario/semillas/lista.html', {'semillas': semillas})

@login_required
def crear_semilla(request):
    if request.method == 'POST':
        form = SemillaForm(request.POST)
        if form.is_valid():
            semilla = form.save()
            messages.success(request, 'Semilla creada exitosamente')
            return redirect('gestion_cultivo:lista_semillas')
    else:
        form = SemillaForm()
    return render(request, 'gestion_cultivo/inventario/semillas/crear.html', {'form': form})

@login_required
def detalle_semilla(request, pk):
    semilla = get_object_or_404(Semilla, pk=pk)  # No tiene campo usuario
    return render(request, 'gestion_cultivo/inventario/semillas/detalle.html', {'semilla': semilla})

@login_required
def editar_semilla(request, pk):
    semilla = get_object_or_404(Semilla, pk=pk)  # No tiene campo usuario
    if request.method == 'POST':
        form = SemillaForm(request.POST, instance=semilla)
        if form.is_valid():
            form.save()
            messages.success(request, 'Semilla actualizada exitosamente')
            return redirect('gestion_cultivo:lista_semillas')
    else:
        form = SemillaForm(instance=semilla)
    return render(request, 'gestion_cultivo/inventario/semillas/editar.html', {'form': form, 'semilla': semilla})

@login_required
def eliminar_semilla(request, pk):
    semilla = get_object_or_404(Semilla, pk=pk)  # No tiene campo usuario
    if request.method == 'POST':
        semilla.delete()
        messages.success(request, 'Semilla eliminada exitosamente')
        return redirect('gestion_cultivo:lista_semillas')
    return render(request, 'gestion_cultivo/inventario/semillas/eliminar.html', {'semilla': semilla})

# Vistas de Fertilizantes
@login_required
def lista_fertilizantes(request):
    fertilizantes = Fertilizante.objects.all()  # No tiene campo usuario
    return render(request, 'gestion_cultivo/inventario/fertilizantes/lista.html', {'fertilizantes': fertilizantes})

@login_required
def crear_fertilizante(request):
    if request.method == 'POST':
        form = FertilizanteForm(request.POST)
        if form.is_valid():
            fertilizante = form.save()
            messages.success(request, 'Fertilizante creado exitosamente')
            return redirect('gestion_cultivo:lista_fertilizantes')
    else:
        form = FertilizanteForm()
    return render(request, 'gestion_cultivo/inventario/fertilizantes/crear.html', {'form': form})

@login_required
def detalle_fertilizante(request, pk):
    fertilizante = get_object_or_404(Fertilizante, pk=pk)  # No tiene campo usuario
    return render(request, 'gestion_cultivo/inventario/fertilizantes/detalle.html', {'fertilizante': fertilizante})

@login_required
def editar_fertilizante(request, pk):
    fertilizante = get_object_or_404(Fertilizante, pk=pk)  # No tiene campo usuario
    if request.method == 'POST':
        form = FertilizanteForm(request.POST, instance=fertilizante)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fertilizante actualizado exitosamente')
            return redirect('gestion_cultivo:lista_fertilizantes')
    else:
        form = FertilizanteForm(instance=fertilizante)
    return render(request, 'gestion_cultivo/inventario/fertilizantes/editar.html', {'form': form, 'fertilizante': fertilizante})

@login_required
def eliminar_fertilizante(request, pk):
    fertilizante = get_object_or_404(Fertilizante, pk=pk)  # No tiene campo usuario
    if request.method == 'POST':
        fertilizante.delete()
        messages.success(request, 'Fertilizante eliminado exitosamente')
        return redirect('gestion_cultivo:lista_fertilizantes')
    return render(request, 'gestion_cultivo/inventario/fertilizantes/eliminar.html', {'fertilizante': fertilizante})

# Vistas de Contenedores
@login_required
def lista_contenedores(request):
    contenedores = Contenedor.objects.filter(usuario=request.user)
    return render(request, 'gestion_cultivo/inventario/contenedores/lista.html', {'contenedores': contenedores})

@login_required
def crear_contenedor(request):
    if request.method == 'POST':
        form = ContenedorForm(request.POST)
        if form.is_valid():
            contenedor = form.save(commit=False)
            contenedor.usuario = request.user
            contenedor.save()
            messages.success(request, 'Contenedor creado exitosamente')
            return redirect('gestion_cultivo:lista_contenedores')
    else:
        form = ContenedorForm()
    return render(request, 'gestion_cultivo/inventario/contenedores/crear.html', {'form': form})

@login_required
def detalle_contenedor(request, pk):
    contenedor = get_object_or_404(Contenedor, pk=pk, usuario=request.user)
    return render(request, 'gestion_cultivo/inventario/contenedores/detalle.html', {'contenedor': contenedor})

@login_required
def editar_contenedor(request, pk):
    contenedor = get_object_or_404(Contenedor, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = ContenedorForm(request.POST, instance=contenedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contenedor actualizado exitosamente')
            return redirect('gestion_cultivo:lista_contenedores')
    else:
        form = ContenedorForm(instance=contenedor)
    return render(request, 'gestion_cultivo/inventario/contenedores/editar.html', {'form': form, 'contenedor': contenedor})

@login_required
def eliminar_contenedor(request, pk):
    contenedor = get_object_or_404(Contenedor, pk=pk, usuario=request.user)
    if request.method == 'POST':
        contenedor.delete()
        messages.success(request, 'Contenedor eliminado exitosamente')
        return redirect('gestion_cultivo:lista_contenedores')
    return render(request, 'gestion_cultivo/inventario/contenedores/eliminar.html', {'contenedor': contenedor})

# Vistas de Maquinaria
@login_required
def lista_maquinaria(request):
    maquinaria = Maquinaria.objects.filter(usuario=request.user)
    return render(request, 'gestion_cultivo/inventario/maquinaria/lista.html', {'maquinaria': maquinaria})

@login_required
def crear_maquinaria(request):
    if request.method == 'POST':
        form = MaquinariaForm(request.POST)
        if form.is_valid():
            maquinaria = form.save(commit=False)
            maquinaria.usuario = request.user
            maquinaria.save()
            messages.success(request, 'Maquinaria creada exitosamente')
            return redirect('gestion_cultivo:lista_maquinaria')
    else:
        form = MaquinariaForm()
    return render(request, 'gestion_cultivo/inventario/maquinaria/crear.html', {'form': form})

@login_required
def detalle_maquinaria(request, pk):
    maquinaria = get_object_or_404(Maquinaria, pk=pk, usuario=request.user)
    return render(request, 'gestion_cultivo/inventario/maquinaria/detalle.html', {'maquinaria': maquinaria})

@login_required
def editar_maquinaria(request, pk):
    maquinaria = get_object_or_404(Maquinaria, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = MaquinariaForm(request.POST, instance=maquinaria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Maquinaria actualizada exitosamente')
            return redirect('gestion_cultivo:lista_maquinaria')
    else:
        form = MaquinariaForm(instance=maquinaria)
    return render(request, 'gestion_cultivo/inventario/maquinaria/editar.html', {'form': form, 'maquinaria': maquinaria})

@login_required
def eliminar_maquinaria(request, pk):
    maquinaria = get_object_or_404(Maquinaria, pk=pk, usuario=request.user)
    if request.method == 'POST':
        maquinaria.delete()
        messages.success(request, 'Maquinaria eliminada exitosamente')
        return redirect('gestion_cultivo:lista_maquinaria')
    return render(request, 'gestion_cultivo/inventario/maquinaria/eliminar.html', {'maquinaria': maquinaria})