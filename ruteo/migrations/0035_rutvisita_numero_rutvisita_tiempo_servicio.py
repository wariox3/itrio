# Generated by Django 4.2.4 on 2024-11-20 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruteo', '0034_rutvisita_estado_decodificado_alerta'),
    ]

    operations = [
        migrations.AddField(
            model_name='rutvisita',
            name='numero',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='rutvisita',
            name='tiempo_servicio',
            field=models.IntegerField(default=0),
        ),
    ]
