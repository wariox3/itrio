# Generated by Django 4.2.4 on 2024-07-27 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenedor', '0028_rename_contenedoridentificacion_ctnidentificacion'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ContenedorTipoPersona',
            new_name='CtnTipoPersona',
        ),
    ]
