# Generated by Django 4.2.4 on 2024-07-27 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenedor', '0030_rename_contenedorregimen_ctnregimen'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ContenedorCiudad',
            new_name='CtnCiudad',
        ),
    ]