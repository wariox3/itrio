# Generated by Django 4.2.4 on 2024-07-27 18:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenedor', '0032_rename_contenedorestado_ctnestado'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ContenedorPais',
            new_name='CtnPais',
        ),
    ]
