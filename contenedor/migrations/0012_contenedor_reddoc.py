# Generated by Django 4.2.4 on 2024-07-19 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenedor', '0011_contenedormovimiento_contenedor_movimiento_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenedor',
            name='reddoc',
            field=models.BooleanField(default=False),
        ),
    ]
