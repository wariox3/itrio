# Generated by Django 4.2.4 on 2025-02-07 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenedor', '0043_alter_contenedor_fecha_ultima_conexion'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctnplan',
            name='plan_tipo_id',
            field=models.CharField(max_length=1, null=True),
        ),
    ]
