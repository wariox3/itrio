# Generated by Django 4.2.4 on 2024-08-19 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0033_humsalud_porcentaje_empleado'),
    ]

    operations = [
        migrations.AddField(
            model_name='humcredito',
            name='inactivo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='humcredito',
            name='inactivo_periodo',
            field=models.BooleanField(default=False),
        ),
    ]
