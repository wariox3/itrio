# Generated by Django 4.2.4 on 2025-01-27 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0077_humaportecontrato_error_terminacion_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HumAporteDetalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aporte_contrato', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='aportes_detalles_aporte_contrato_rel', to='humano.humaportecontrato')),
            ],
            options={
                'db_table': 'hum_aporte_detalle',
            },
        ),
    ]
