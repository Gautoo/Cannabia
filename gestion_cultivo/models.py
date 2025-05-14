# gestion_cultivo/models.py
from django.db import models
from django.contrib.auth.models import User # Importa el modelo User de Django
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

class Semilla(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, default='')
    banco = models.ForeignKey('Banco', on_delete=models.SET_NULL, null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(default=timezone.now)
    fecha_compra = models.DateField(default=timezone.now)
    cbd = models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True)
    thc = models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True)
    tiempo_floracion = models.IntegerField(blank=True, default=0, help_text='Días', null=True)
    rendimiento = models.CharField(blank=True, default='', max_length=50)
    variedad = models.CharField(blank=True, default='', max_length=100)
    caracteristicas = models.ManyToManyField('Caracteristica', blank=True)
    terpenos = models.CharField(blank=True, max_length=200, null=True)
    ciclo = models.CharField(blank=True, max_length=100, null=True)
    observaciones = models.TextField(blank=True, null=True)
    padres = models.CharField(blank=True, max_length=200, null=True)
    precio = models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)
    tamano_blister = models.CharField(blank=True, max_length=50, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Semilla'
        verbose_name_plural = 'Semillas'

class Fertilizante(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100, blank=True, default='')
    descripcion = models.TextField(blank=True, default='')
    tipo = models.CharField(choices=[('base', 'Base'), ('estimulador', 'Estimulador'), ('microbios', 'Microbios'), ('otro', 'Otro')], max_length=20, blank=True, default='')
    etapa_uso = models.CharField(choices=[('crecimiento', 'Crecimiento'), ('floracion', 'Floración'), ('ambas', 'Ambas')], max_length=20, blank=True, default='')
    medio_compatible = models.CharField(choices=[('suelo', 'Suelo'), ('hidroponico', 'Hidropónico'), ('ambos', 'Ambos')], max_length=20, blank=True, default='')
    npk = models.CharField(max_length=20, blank=True, default='')
    precio = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    instrucciones = models.TextField(blank=True, default='')
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Fertilizante'
        verbose_name_plural = 'Fertilizantes'

class Contenedor(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default='')
    dimensiones = models.CharField(max_length=50, blank=True, default='')
    caracteristicas = models.TextField(blank=True, default='')
    tipo = models.CharField(choices=[('maceta', 'Maceta'), ('bandeja', 'Bandeja de esquejes'), ('aeroclonador', 'Aeroclonador'), ('balde', 'Balde hidroponía')], max_length=20)
    capacidad = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    color = models.CharField(max_length=50, blank=True, default='')
    material = models.CharField(max_length=50, blank=True, default='')
    precio = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Contenedor'
        verbose_name_plural = 'Contenedores'

class Maquinaria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default='')
    tipo = models.CharField(choices=[('iluminacion', 'Iluminación'), ('ventilacion', 'Ventilación'), ('controlador', 'Controlador'), ('bomba', 'Bomba'), ('medidor', 'Medidor')], max_length=20)
    marca = models.CharField(max_length=100, blank=True, default='')
    modelo = models.CharField(max_length=100, blank=True, default='')
    potencia = models.CharField(max_length=50, blank=True, default='')
    voltaje = models.CharField(max_length=50, blank=True, default='')
    compatibilidad = models.CharField(max_length=200, blank=True, default='')
    dimensiones = models.CharField(max_length=100, blank=True, default='')
    accesorios = models.TextField(blank=True, default='')
    precio = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fecha_actualizacion = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Maquinaria'
        verbose_name_plural = 'Maquinarias'

class Stock(models.Model):
    tipo_producto = models.CharField(choices=[('semilla', 'Semilla'), ('fertilizante', 'Fertilizante'), ('contenedor', 'Contenedor'), ('maquinaria', 'Maquinaria')], max_length=20)
    cantidad = models.IntegerField(default=0)
    fecha_compra = models.DateField(blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    lote = models.CharField(blank=True, max_length=50, null=True)
    ubicacion = models.CharField(blank=True, max_length=100, null=True)
    notas = models.TextField(blank=True, default='')
    precio_compra = models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)
    proveedor = models.CharField(blank=True, default='', max_length=100)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    semilla = models.ForeignKey(Semilla, on_delete=models.CASCADE, blank=True, null=True)
    fertilizante = models.ForeignKey(Fertilizante, on_delete=models.CASCADE, blank=True, null=True)
    contenedor = models.ForeignKey(Contenedor, on_delete=models.CASCADE, blank=True, null=True)
    maquinaria = models.ForeignKey(Maquinaria, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        if self.semilla:
            return f"{self.semilla.nombre} - {self.cantidad}"
        elif self.fertilizante:
            return f"{self.fertilizante.nombre} - {self.cantidad}"
        elif self.contenedor:
            return f"{self.contenedor.nombre} - {self.cantidad}"
        elif self.maquinaria:
            return f"{self.maquinaria.nombre} - {self.cantidad}"
        return f"Stock {self.id}"

    class Meta:
        verbose_name = 'Stock'
        verbose_name_plural = 'Stocks'

class Sala(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default='')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    humedad_objetivo = models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    temperatura_objetivo = models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, validators=[MinValueValidator(0), MaxValueValidator(50)])
    tipo_iluminacion = models.CharField(choices=[('LED', 'LED'), ('HPS', 'HPS'), ('CMH', 'CMH'), ('LEC', 'LEC'), ('FLUORESCENTE', 'Fluorescente'), ('NATURAL', 'Natural')], max_length=20)
    horas_luz = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)])

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'

class AreaCultivo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default='')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    tipo_cultivo = models.CharField(choices=[('suelo', 'Suelo'), ('hidroponico', 'Hidropónico'), ('living_soil', 'Living Soil')], default='suelo', max_length=20)
    estado = models.CharField(max_length=50, blank=True, default='')
    tiene_riego_automatico = models.BooleanField(default=False)
    sustrato = models.CharField(blank=True, choices=[('tierra_100', '100% Tierra'), ('coco_100', '100% Coco'), ('tierra_coco_50_50', '50% Tierra - 50% Coco'), ('tierra_hummus_50_50', '50% Tierra - 50% Hummus'), ('tierra_perlita_70_30', '70% Tierra - 30% Perlita'), ('coco_perlita_70_30', '70% Coco - 30% Perlita'), ('personalizado', 'Personalizado')], max_length=20, null=True)
    composicion_sustrato = models.TextField(blank=True, help_text='Describe la composición personalizada del sustrato', null=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Área de Cultivo'
        verbose_name_plural = 'Áreas de Cultivo'

class Planta(models.Model):
    nombre_id = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default='')
    area = models.ForeignKey(AreaCultivo, on_delete=models.CASCADE, null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    tipo_planta = models.CharField(choices=[('REGULAR', 'Regular'), ('FEMINIZADA', 'Feminizada'), ('AUTOFLORECIENTE', 'Autofloreciente')], default='FEMINIZADA', max_length=20)
    etapa_actual = models.CharField(choices=[('GERMINACION', 'Germinación'), ('PLANTULA', 'Plántula'), ('VEGETATIVO', 'Vegetativo'), ('FLORACION', 'Floración'), ('SECADO', 'Secado'), ('CURADO', 'Curado')], default='GERMINACION', max_length=20)
    activa = models.BooleanField(default=True)
    es_madre = models.BooleanField(default=False)
    planta_madre = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='esquejes')
    semilla = models.ForeignKey(Semilla, on_delete=models.SET_NULL, null=True, blank=True)
    thc_estimado = models.DecimalField(decimal_places=2, default=0, max_digits=4, validators=[MinValueValidator(0), MaxValueValidator(100)])
    cbd_estimado = models.DecimalField(decimal_places=2, default=0, max_digits=4, validators=[MinValueValidator(0), MaxValueValidator(100)])
    fecha_germinacion = models.DateField(default=timezone.now)

    def __str__(self):
        return self.nombre_id

    class Meta:
        verbose_name = 'Planta'
        verbose_name_plural = 'Plantas'

class Genetica(models.Model):
    nombre = models.CharField(max_length=100, blank=True, default='')
    descripcion = models.TextField(blank=True, default='')
    tipo = models.CharField(choices=[('INDICA', 'Indica'), ('SATIVA', 'Sativa'), ('HIBRIDO', 'Híbrido')], default='HIBRIDO', max_length=20)
    tiempo_floracion = models.IntegerField(blank=True, default=0, null=True)
    rendimiento = models.CharField(blank=True, default='', max_length=50)
    thc_estimado = models.DecimalField(decimal_places=2, default=0, max_digits=4, validators=[MinValueValidator(0), MaxValueValidator(100)])
    cbd_estimado = models.DecimalField(decimal_places=2, default=0, max_digits=4, validators=[MinValueValidator(0), MaxValueValidator(100)])
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre or 'Sin nombre'

class Caracteristica(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default='')
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Característica'
        verbose_name_plural = 'Características'

class PresentacionFertilizante(models.Model):
    tamano = models.CharField(max_length=50, blank=True, default='')
    precio = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    fertilizante = models.ForeignKey(Fertilizante, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.tamano} - ${self.precio}"

    class Meta:
        verbose_name = 'Presentación de Fertilizante'
        verbose_name_plural = 'Presentaciones de Fertilizantes'

class Banco(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default='')
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'

class Terpeno(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default='')
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Terpeno'
        verbose_name_plural = 'Terpenos'