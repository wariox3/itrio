# Generated by Django 4.2.4 on 2024-07-10 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ruteo', '0007_rutfranja'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RutGuia',
            new_name='RutVisita',
        ),
        migrations.AlterModelTable(
            name='rutvisita',
            table='rut_visita',
        ),
    ]
