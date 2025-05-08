# gestion_cultivo/models.py
from django.db import models
from django.contrib.auth.models import User # Importa el modelo User de Django
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Sala(models.Model):
    TIPO_ILUMINACION_CHOICES = [
        ('LED', 'LED'),
        ('HPS', 'HPS'),
        ('CMH', 'CMH'),
        ('LEC', 'LEC'),
        ('FLUORESCENTE', 'Fluorescente'),
        ('NATURAL', 'Natural'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default='')
    temperatura_objetivo = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(50)], null=True, blank=True)
    humedad_objetivo = models.DecimalField(max_digits=4, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    tipo_iluminacion = models.CharField(max_length=20, choices=TIPO_ILUMINACION_CHOICES)
    horas_luz = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)])
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('gestion_cultivo:detalle_sala', args=[str(self.id)])

class AreaCultivo(models.Model):
    TIPO_CULTIVO_CHOICES = [
        ('INDOOR', 'Indoor'),
        ('OUTDOOR', 'Outdoor'),
        ('GREENHOUSE', 'Greenhouse'),
    ]

    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('MANTENIMIENTO', 'En mantenimiento'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default='')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, null=True, blank=True)
    tipo_cultivo = models.CharField(max_length=20, choices=TIPO_CULTIVO_CHOICES, default='INDOOR')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    tiene_riego_automatico = models.BooleanField(default=False)
    sustrato = models.CharField(max_length=100, blank=True, default='')
    composicion_sustrato = models.TextField(blank=True, default='')
    tamano_maceta = models.CharField(max_length=50, blank=True, default='')
    tamano_balde = models.CharField(max_length=50, blank=True, default='')
    altura = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    largo = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    ancho = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre} - {self.sala.nombre}"

    def get_absolute_url(self):
        return reverse('gestion_cultivo:detalle_area', args=[str(self.id)])

    def get_tipo_cultivo_display(self):
        return dict(self.TIPO_CULTIVO_CHOICES).get(self.tipo_cultivo, self.tipo_cultivo)

    def get_sustrato_display(self):
        return self.sustrato if self.sustrato else None

    def get_tamano_maceta_display(self):
        return self.tamano_maceta if self.tamano_maceta else None

    def get_tamano_balde_display(self):
        return self.tamano_balde if self.tamano_balde else None

class Genetica(models.Model):
    TIPO_CHOICES = [
        ('INDICA', 'Indica'),
        ('SATIVA', 'Sativa'),
        ('HIBRIDO', 'Híbrido'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default='')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='HIBRIDO')
    tiempo_floracion = models.IntegerField(validators=[MinValueValidator(0)], default=60)
    rendimiento = models.CharField(max_length=50, default='Medio')
    thc_estimado = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    cbd_estimado = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

class Banco(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default='')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Terpeno(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default='')

    def __str__(self):
        return self.nombre

class Caracteristica(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, default='')

    def __str__(self):
        return self.nombre

class ItemInventario(models.Model):
    TIPO_CHOICES = [
        ('semilla', 'Semilla'),
        ('lampara', 'Lámpara'),
        ('maceta', 'Maceta'),
        ('fertilizante', 'Fertilizante'),
        ('aditivo', 'Aditivo'),
        ('base', 'Base'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='otro')
    cantidad = models.IntegerField(default=0)
    descripcion = models.TextField(blank=True, default='')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fecha_agregado = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True

class Semilla(ItemInventario):
    banco = models.ForeignKey(Banco, on_delete=models.SET_NULL, null=True, blank=True)
    porcentaje_thc = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    porcentaje_cbd = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    dias_flora = models.IntegerField(validators=[MinValueValidator(0)], default=60)
    terpenos = models.ManyToManyField(Terpeno, blank=True)
    caracteristicas = models.ManyToManyField(Caracteristica, blank=True)
    descripcion = models.TextField(blank=True, default='')
    cantidad = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    fecha_compra = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre} - {self.banco.nombre}"

class Lampara(ItemInventario):
    potencia = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    tipo = models.CharField(max_length=100, default='LED')
    marca = models.CharField(max_length=100, default='')
    descripcion = models.TextField(blank=True, default='')
    cantidad = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f"{self.nombre} - {self.marca}"

class Maceta(ItemInventario):
    capacidad = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    material = models.CharField(max_length=100, default='Plástico')
    descripcion = models.TextField(blank=True, default='')
    cantidad = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f"{self.nombre} - {self.capacidad}L"

class Fertilizante(ItemInventario):
    marca = models.CharField(max_length=100, default='')
    tipo = models.CharField(max_length=100, default='')
    npk = models.CharField(max_length=20, default='0-0-0')
    descripcion = models.TextField(blank=True, default='')
    cantidad = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f"{self.nombre} - {self.marca}"

class Aditivo(ItemInventario):
    marca = models.CharField(max_length=100, default='')
    tipo = models.CharField(max_length=100, default='')
    descripcion = models.TextField(blank=True, default='')
    cantidad = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f"{self.nombre} - {self.marca}"

class Base(ItemInventario):
    marca = models.CharField(max_length=100, default='')
    tipo = models.CharField(max_length=100, default='')
    descripcion = models.TextField(blank=True, default='')
    cantidad = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f"{self.nombre} - {self.marca}"

class Planta(models.Model):
    TIPO_PLANTA_CHOICES = [
        ('REGULAR', 'Regular'),
        ('FEMINIZADA', 'Feminizada'),
        ('AUTOFLORECIENTE', 'Autofloreciente'),
    ]

    ETAPA_CHOICES = [
        ('GERMINACION', 'Germinación'),
        ('PLANTULA', 'Plántula'),
        ('VEGETATIVO', 'Vegetativo'),
        ('FLORACION', 'Floración'),
        ('SECADO', 'Secado'),
        ('CURADO', 'Curado'),
    ]

    nombre_id = models.CharField(max_length=100)
    tipo_planta = models.CharField(max_length=20, choices=TIPO_PLANTA_CHOICES, default='FEMINIZADA')
    semilla = models.ForeignKey(Semilla, on_delete=models.SET_NULL, null=True, blank=True)
    planta_madre = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    es_madre = models.BooleanField(default=False)
    thc_estimado = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    cbd_estimado = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(100)], default=0)
    fecha_germinacion = models.DateField(default=timezone.now)
    etapa_actual = models.CharField(max_length=20, choices=ETAPA_CHOICES, default='GERMINACION')
    area = models.ForeignKey(AreaCultivo, on_delete=models.CASCADE, null=True, blank=True)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre_id} - {self.etapa_actual}"

    def get_absolute_url(self):
        return reverse('gestion_cultivo:detalle_planta', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.tipo_planta == 'semilla' and self.semilla:
            # Reducir la cantidad de semillas disponibles
            self.semilla.cantidad_disponible -= 1
            self.semilla.save()
        super().save(*args, **kwargs)