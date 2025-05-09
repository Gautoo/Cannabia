# Generated by Django 5.2 on 2025-05-08 06:17

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_cultivo', '0007_rename_fecha_creacion_semilla_fecha_agregado_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, default='')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Caracteristica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Terpeno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.RemoveField(
            model_name='sustrato',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='fertilizante',
            name='fecha_caducidad',
        ),
        migrations.RemoveField(
            model_name='fertilizante',
            name='fecha_compra',
        ),
        migrations.RemoveField(
            model_name='fertilizante',
            name='instrucciones',
        ),
        migrations.RemoveField(
            model_name='fertilizante',
            name='notas',
        ),
        migrations.RemoveField(
            model_name='fertilizante',
            name='precio',
        ),
        migrations.RemoveField(
            model_name='fertilizante',
            name='volumen',
        ),
        migrations.RemoveField(
            model_name='semilla',
            name='altura',
        ),
        migrations.RemoveField(
            model_name='semilla',
            name='ambiente',
        ),
        migrations.RemoveField(
            model_name='semilla',
            name='cbd',
        ),
        migrations.RemoveField(
            model_name='semilla',
            name='fecha_caducidad',
        ),
        migrations.RemoveField(
            model_name='semilla',
            name='genetica',
        ),
        migrations.RemoveField(
            model_name='semilla',
            name='notas',
        ),
        migrations.RemoveField(
            model_name='semilla',
            name='precio',
        ),
        migrations.RemoveField(
            model_name='semilla',
            name='rendimiento',
        ),
        migrations.RemoveField(
            model_name='semilla',
            name='thc',
        ),
        migrations.RemoveField(
            model_name='semilla',
            name='tiempo_floracion',
        ),
        migrations.AddField(
            model_name='fertilizante',
            name='descripcion',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='semilla',
            name='dias_flora',
            field=models.IntegerField(default=60, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='semilla',
            name='porcentaje_cbd',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AddField(
            model_name='semilla',
            name='porcentaje_thc',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='areacultivo',
            name='altura',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='areacultivo',
            name='ancho',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='areacultivo',
            name='composicion_sustrato',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='areacultivo',
            name='descripcion',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='areacultivo',
            name='estado',
            field=models.CharField(choices=[('ACTIVO', 'Activo'), ('INACTIVO', 'Inactivo'), ('MANTENIMIENTO', 'En mantenimiento')], default='ACTIVO', max_length=20),
        ),
        migrations.AlterField(
            model_name='areacultivo',
            name='largo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='areacultivo',
            name='sala',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion_cultivo.sala'),
        ),
        migrations.AlterField(
            model_name='areacultivo',
            name='sustrato',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='areacultivo',
            name='tamano_balde',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='areacultivo',
            name='tamano_maceta',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='areacultivo',
            name='tipo_cultivo',
            field=models.CharField(choices=[('INDOOR', 'Indoor'), ('OUTDOOR', 'Outdoor'), ('GREENHOUSE', 'Greenhouse')], default='INDOOR', max_length=20),
        ),
        migrations.AlterField(
            model_name='fertilizante',
            name='cantidad',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='fertilizante',
            name='marca',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='fertilizante',
            name='nombre',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='fertilizante',
            name='npk',
            field=models.CharField(default='0-0-0', max_length=20),
        ),
        migrations.AlterField(
            model_name='fertilizante',
            name='tipo',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='genetica',
            name='cbd_estimado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='genetica',
            name='descripcion',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='genetica',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='genetica',
            name='rendimiento',
            field=models.CharField(default='Medio', max_length=50),
        ),
        migrations.AlterField(
            model_name='genetica',
            name='thc_estimado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='genetica',
            name='tiempo_floracion',
            field=models.IntegerField(default=60, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='genetica',
            name='tipo',
            field=models.CharField(choices=[('INDICA', 'Indica'), ('SATIVA', 'Sativa'), ('HIBRIDO', 'Híbrido')], default='HIBRIDO', max_length=20),
        ),
        migrations.AlterField(
            model_name='planta',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion_cultivo.areacultivo'),
        ),
        migrations.AlterField(
            model_name='planta',
            name='cbd_estimado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='planta',
            name='etapa_actual',
            field=models.CharField(choices=[('GERMINACION', 'Germinación'), ('PLANTULA', 'Plántula'), ('VEGETATIVO', 'Vegetativo'), ('FLORACION', 'Floración'), ('SECADO', 'Secado'), ('CURADO', 'Curado')], default='GERMINACION', max_length=20),
        ),
        migrations.AlterField(
            model_name='planta',
            name='fecha_germinacion',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='planta',
            name='planta_madre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion_cultivo.planta'),
        ),
        migrations.AlterField(
            model_name='planta',
            name='thc_estimado',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='planta',
            name='tipo_planta',
            field=models.CharField(choices=[('REGULAR', 'Regular'), ('FEMINIZADA', 'Feminizada'), ('AUTOFLORECIENTE', 'Autofloreciente')], default='FEMINIZADA', max_length=20),
        ),
        migrations.AlterField(
            model_name='sala',
            name='descripcion',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='sala',
            name='horas_luz',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)]),
        ),
        migrations.AlterField(
            model_name='sala',
            name='humedad_objetivo',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='sala',
            name='temperatura_objetivo',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50)]),
        ),
        migrations.AlterField(
            model_name='sala',
            name='tipo_iluminacion',
            field=models.CharField(choices=[('LED', 'LED'), ('HPS', 'HPS'), ('CMH', 'CMH'), ('LEC', 'LEC'), ('FLUORESCENTE', 'Fluorescente'), ('NATURAL', 'Natural')], max_length=20),
        ),
        migrations.AlterField(
            model_name='semilla',
            name='cantidad',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='semilla',
            name='descripcion',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='semilla',
            name='fecha_compra',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='semilla',
            name='nombre',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='semilla',
            name='tipo',
            field=models.CharField(choices=[('semilla', 'Semilla'), ('lampara', 'Lámpara'), ('maceta', 'Maceta'), ('fertilizante', 'Fertilizante'), ('aditivo', 'Aditivo'), ('base', 'Base'), ('otro', 'Otro')], default='otro', max_length=20),
        ),
        migrations.CreateModel(
            name='Aditivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('fecha_agregado', models.DateTimeField(default=django.utils.timezone.now)),
                ('marca', models.CharField(default='', max_length=100)),
                ('tipo', models.CharField(default='', max_length=100)),
                ('descripcion', models.TextField(blank=True, default='')),
                ('cantidad', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='semilla',
            name='banco',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion_cultivo.banco'),
        ),
        migrations.CreateModel(
            name='Base',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('fecha_agregado', models.DateTimeField(default=django.utils.timezone.now)),
                ('marca', models.CharField(default='', max_length=100)),
                ('tipo', models.CharField(default='', max_length=100)),
                ('descripcion', models.TextField(blank=True, default='')),
                ('cantidad', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='semilla',
            name='caracteristicas',
            field=models.ManyToManyField(blank=True, to='gestion_cultivo.caracteristica'),
        ),
        migrations.CreateModel(
            name='Lampara',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('fecha_agregado', models.DateTimeField(default=django.utils.timezone.now)),
                ('potencia', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('tipo', models.CharField(default='LED', max_length=100)),
                ('marca', models.CharField(default='', max_length=100)),
                ('descripcion', models.TextField(blank=True, default='')),
                ('cantidad', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Maceta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('tipo', models.CharField(choices=[('semilla', 'Semilla'), ('lampara', 'Lámpara'), ('maceta', 'Maceta'), ('fertilizante', 'Fertilizante'), ('aditivo', 'Aditivo'), ('base', 'Base'), ('otro', 'Otro')], default='otro', max_length=20)),
                ('fecha_agregado', models.DateTimeField(default=django.utils.timezone.now)),
                ('capacidad', models.DecimalField(decimal_places=2, default=0, max_digits=6, validators=[django.core.validators.MinValueValidator(0)])),
                ('material', models.CharField(default='Plástico', max_length=100)),
                ('descripcion', models.TextField(blank=True, default='')),
                ('cantidad', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='semilla',
            name='terpenos',
            field=models.ManyToManyField(blank=True, to='gestion_cultivo.terpeno'),
        ),
        migrations.DeleteModel(
            name='Equipo',
        ),
        migrations.DeleteModel(
            name='Sustrato',
        ),
    ]
