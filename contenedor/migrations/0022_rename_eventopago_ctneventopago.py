# Generated by Django 4.2.4 on 2024-07-27 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenedor', '0021_rename_informacionfacturacion_ctninformacionfacturacion'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EventoPago',
            new_name='CtnEventoPago',
        ),
    ]
