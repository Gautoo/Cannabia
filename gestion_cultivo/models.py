# gestion_cultivo/models.py
from django.db import models
from django.contrib.auth.models import User # Importa el modelo User de Django

class Sala(models.Model):
    # Cada sala pertenece a un usuario específico. Si el usuario se borra, sus salas también (CASCADE).
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='salas')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True) # blank=True (no requerido en forms), null=True (puede ser NULL en DB)

    def __str__(self):
        # Texto que representa al objeto (útil en el admin)
        return self.nombre

class AreaCultivo(models.Model):
    # Cada área pertenece a una Sala. Si la Sala se borra, sus Áreas también.
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='areas')
    nombre = models.CharField(max_length=100)
    # Puedes añadir más campos después (ej: tipo_cultivo = models.CharField(...))

    def __str__(self):
        # Muestra el nombre de la sala y el área para claridad
        return f"{self.sala.nombre} - {self.nombre}"

class Planta(models.Model):
    # Cada planta pertenece a un Área de Cultivo. Si el Área se borra, sus Plantas también.
    area = models.ForeignKey(AreaCultivo, on_delete=models.CASCADE, related_name='plantas')
    # Usamos un nombre/ID para identificarla, debe ser único para evitar confusiones
    nombre_id = models.CharField(max_length=100, help_text="Identificador único para esta planta (ej: SKUNK-01)")
    genetica = models.CharField(max_length=100, blank=True)
    thc_estimado = models.FloatField(verbose_name="THC Estimado (%)", blank=True, null=True)
    cbd_estimado = models.FloatField(verbose_name="CBD Estimado (%)", blank=True, null=True)
    fecha_germinacion = models.DateField(blank=True, null=True)

    # Definimos las etapas posibles como opciones
    ETAPAS = [
        ('SEM', 'Semilla'),
        ('PLN', 'Plántula'),
        ('VEG', 'Vegetativo'),
        ('PRE', 'Pre-floración'),
        ('FLO', 'Floración'),
        ('MAD', 'Maduración'),
        ('COS', 'Cosecha'),
        ('SEC', 'Secado'),
        ('CUR', 'Curado'),
    ]
    # Campo para guardar la etapa actual, usando las opciones definidas
    etapa_actual = models.CharField(
        max_length=3,
        choices=ETAPAS,
        default='SEM', # Valor por defecto al crear una planta
        verbose_name="Etapa Actual"
    )
    # Campo para saber si la planta está activa o ya fue cosechada/descartada
    activa = models.BooleanField(default=True)

    class Meta:
        # Asegura que no haya dos plantas con el mismo nombre_id DENTRO de la misma área.
        # unique_together = [['area', 'nombre_id']] # Comentado por ahora para simplificar, puedes añadirlo luego si quieres IDs únicos *por área* en vez de globales.
         pass # Puedes descomentar unique_together luego si lo necesitas

    def __str__(self):
        return f"{self.nombre_id} ({self.genetica})" if self.genetica else self.nombre_id