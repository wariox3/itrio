# Generated by Django 4.2.4 on 2024-11-26 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenedor', '0039_ctndireccion_resultado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ctndireccion',
            old_name='resultado',
            new_name='cantidad_resultados',
        ),
    ]
