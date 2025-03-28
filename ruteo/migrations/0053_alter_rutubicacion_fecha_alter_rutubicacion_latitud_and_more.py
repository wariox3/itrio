# Generated by Django 4.2.4 on 2025-03-28 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruteo', '0052_rutdespacho_fecha_ubicacion_rutdespacho_latitud_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rutubicacion',
            name='fecha',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='rutubicacion',
            name='latitud',
            field=models.DecimalField(decimal_places=15, max_digits=25),
        ),
        migrations.AlterField(
            model_name='rutubicacion',
            name='longitud',
            field=models.DecimalField(decimal_places=15, max_digits=25),
        ),
    ]
