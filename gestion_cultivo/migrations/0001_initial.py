# Generated by Django 5.2 on 2025-05-05 22:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaCultivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Planta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_id', models.CharField(help_text='Identificador único para esta planta (ej: SKUNK-01)', max_length=100)),
                ('genetica', models.CharField(blank=True, max_length=100)),
                ('thc_estimado', models.FloatField(blank=True, null=True, verbose_name='THC Estimado (%)')),
                ('cbd_estimado', models.FloatField(blank=True, null=True, verbose_name='CBD Estimado (%)')),
                ('fecha_germinacion', models.DateField(blank=True, null=True)),
                ('etapa_actual', models.CharField(choices=[('SEM', 'Semilla'), ('PLN', 'Plántula'), ('VEG', 'Vegetativo'), ('PRE', 'Pre-floración'), ('FLO', 'Floración'), ('MAD', 'Maduración'), ('COS', 'Cosecha'), ('SEC', 'Secado'), ('CUR', 'Curado')], default='SEM', max_length=3, verbose_name='Etapa Actual')),
                ('activa', models.BooleanField(default=True)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plantas', to='gestion_cultivo.areacultivo')),
            ],
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='salas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='areacultivo',
            name='sala',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='areas', to='gestion_cultivo.sala'),
        ),
    ]
