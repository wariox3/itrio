# Generated by Django 4.2.4 on 2024-10-15 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0066_alter_humcargo_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='HumAporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_desde', models.DateField()),
                ('fecha_hasta', models.DateField()),
                ('fecha_hasta_periodo', models.DateField()),
                ('anio', models.BigIntegerField(default=0)),
                ('anio_salud', models.BigIntegerField(default=0)),
                ('mes', models.BigIntegerField(default=0)),
                ('mes_salud', models.BigIntegerField(default=0)),
                ('contratos', models.IntegerField(default=0)),
                ('empleados', models.IntegerField(default=0)),
                ('lineas', models.IntegerField(default=0)),
                ('pension', models.DecimalField(decimal_places=6, default=0, max_digits=20)),
                ('fondo_solidaridad', models.DecimalField(decimal_places=6, default=0, max_digits=20)),
                ('fondo_subsistencia', models.DecimalField(decimal_places=6, default=0, max_digits=20)),
                ('salud', models.DecimalField(decimal_places=6, default=0, max_digits=20)),
                ('riesgo', models.DecimalField(decimal_places=6, default=0, max_digits=20)),
                ('caja', models.DecimalField(decimal_places=6, default=0, max_digits=20)),
                ('sena', models.DecimalField(decimal_places=6, default=0, max_digits=20)),
                ('icbf', models.DecimalField(decimal_places=6, default=0, max_digits=20)),
                ('total', models.DecimalField(decimal_places=6, default=0, max_digits=20)),
                ('estado_aprobado', models.BooleanField(default=False)),
                ('estado_generado', models.BooleanField(default=False)),
                ('comentario', models.CharField(max_length=300, null=True)),
                ('sucursal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='aportes_sucursal_rel', to='humano.humsucursal')),
            ],
            options={
                'db_table': 'hum_aporte',
            },
        ),
    ]
