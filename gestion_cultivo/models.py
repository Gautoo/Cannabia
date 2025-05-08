# gestion_cultivo/models.py
from django.db import models
from django.contrib.auth.models import User # Importa el modelo User de Django
from django.urls import reverse
from django.utils import timezone

class Sala(models.Model):
    TIPOS_SALA = [
        ('vegetacion', 'Vegetación'),
        ('floracion', 'Floración'),
        ('mixta', 'Mixta'),
        ('ciclo_completo', 'Ciclo Completo'),
        ('otro', 'Otro'),
    ]
    
    # Cada sala pertenece a un usuario específico. Si el usuario se borra, sus salas también (CASCADE).
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='salas')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True) # blank=True (no requerido en forms), null=True (puede ser NULL en DB)
    tipo = models.CharField(max_length=20, choices=TIPOS_SALA, default='mixta')
    altura = models.DecimalField(max_digits=5, decimal_places=2, help_text='Altura en metros', default=0.00)
    largo = models.DecimalField(max_digits=5, decimal_places=2, help_text='Largo en metros', default=0.00)
    ancho = models.DecimalField(max_digits=5, decimal_places=2, help_text='Ancho en metros', default=0.00)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        # Texto que representa al objeto (útil en el admin)
        return self.nombre

    def get_absolute_url(self):
        return reverse('gestion_cultivo:detalle_sala', args=[str(self.id)])

class AreaCultivo(models.Model):
    TIPOS_CULTIVO = [
        ('suelo', 'Suelo'),
        ('hidroponico', 'Hidropónico'),
        ('living_soil', 'Living Soil'),
    ]

    TIPOS_SUSTRATO = [
        ('tierra_100', '100% Tierra'),
        ('coco_100', '100% Coco'),
        ('tierra_coco_50_50', '50% Tierra - 50% Coco'),
        ('tierra_hummus_50_50', '50% Tierra - 50% Hummus'),
        ('tierra_perlita_70_30', '70% Tierra - 30% Perlita'),
        ('coco_perlita_70_30', '70% Coco - 30% Perlita'),
        ('personalizado', 'Personalizado'),
    ]

    TAMANOS_MACETA = [
        ('1l', '1 Litro'),
        ('3l', '3 Litros'),
        ('5l', '5 Litros'),
        ('7l', '7 Litros'),
        ('10l', '10 Litros'),
        ('15l', '15 Litros'),
        ('20l', '20 Litros'),
        ('otro', 'Otro'),
    ]

    TAMANOS_BALDE = [
        ('5l', '5 Litros'),
        ('10l', '10 Litros'),
        ('15l', '15 Litros'),
        ('20l', '20 Litros'),
        ('otro', 'Otro'),
    ]

    nombre = models.CharField(max_length=100)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='areas')
    tipo_cultivo = models.CharField(max_length=20, choices=TIPOS_CULTIVO, default='suelo')
    tiene_riego_automatico = models.BooleanField(default=False)
    sustrato = models.CharField(max_length=20, choices=TIPOS_SUSTRATO, null=True, blank=True)
    composicion_sustrato = models.TextField(blank=True, null=True, help_text='Describe la composición personalizada del sustrato')
    tamano_maceta = models.CharField(max_length=10, choices=TAMANOS_MACETA, null=True, blank=True)
    tamano_balde = models.CharField(max_length=10, choices=TAMANOS_BALDE, null=True, blank=True)
    altura = models.DecimalField(max_digits=5, decimal_places=2, help_text='Altura en metros', default=0.00)
    largo = models.DecimalField(max_digits=5, decimal_places=2, help_text='Largo en metros', default=0.00)
    ancho = models.DecimalField(max_digits=5, decimal_places=2, help_text='Ancho en metros', default=0.00)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('gestion_cultivo:detalle_area', args=[str(self.id)])

    def get_tipo_cultivo_display(self):
        return dict(self.TIPOS_CULTIVO).get(self.tipo_cultivo, self.tipo_cultivo)

    def get_sustrato_display(self):
        return dict(self.TIPOS_SUSTRATO).get(self.sustrato, self.sustrato) if self.sustrato else None

    def get_tamano_maceta_display(self):
        return dict(self.TAMANOS_MACETA).get(self.tamano_maceta, self.tamano_maceta) if self.tamano_maceta else None

    def get_tamano_balde_display(self):
        return dict(self.TAMANOS_BALDE).get(self.tamano_balde, self.tamano_balde) if self.tamano_balde else None

class Genetica(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    thc_estimado = models.FloatField(verbose_name="THC Estimado (%)", blank=True, null=True)
    cbd_estimado = models.FloatField(verbose_name="CBD Estimado (%)", blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

class Semilla(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    cantidad_disponible = models.PositiveIntegerField(default=0)
    fecha_compra = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre} ({self.cantidad_disponible} disponibles)"

    def get_absolute_url(self):
        return reverse('gestion_cultivo:detalle_semilla', args=[str(self.id)])

class Planta(models.Model):
    TIPOS_PLANTA = [
        ('semilla', 'Semilla'),
        ('esqueje', 'Esqueje'),
    ]

    ETAPAS = [
        ('germinacion', 'Germinación'),
        ('planta_bebe', 'Planta Bebé'),
        ('vegetacion', 'Vegetación'),
        ('pre_floracion', 'Pre-Floración'),
        ('floracion', 'Floración'),
        ('cosecha', 'Cosecha'),
        ('secado', 'Secado'),
        ('curado', 'Curado'),
    ]

    nombre_id = models.CharField(max_length=100)
    tipo_planta = models.CharField(max_length=20, choices=TIPOS_PLANTA, default='semilla')
    semilla = models.ForeignKey(Semilla, on_delete=models.SET_NULL, null=True, blank=True)
    planta_madre = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='esquejes')
    es_madre = models.BooleanField(default=False)
    thc_estimado = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Porcentaje estimado de THC')
    cbd_estimado = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text='Porcentaje estimado de CBD')
    fecha_germinacion = models.DateField(null=True, blank=True)
    etapa_actual = models.CharField(max_length=20, choices=ETAPAS, default='germinacion')
    area = models.ForeignKey(AreaCultivo, on_delete=models.CASCADE)
    activa = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre_id

    def get_absolute_url(self):
        return reverse('gestion_cultivo:detalle_planta', args=[str(self.id)])

    def save(self, *args, **kwargs):
        if self.tipo_planta == 'semilla' and self.semilla:
            # Reducir la cantidad de semillas disponibles
            self.semilla.cantidad_disponible -= 1
            self.semilla.save()
        super().save(*args, **kwargs)