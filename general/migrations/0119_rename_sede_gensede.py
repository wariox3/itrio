# Generated by Django 4.2.4 on 2024-08-01 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0118_rename_resolucion_genresolucion'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Sede',
            new_name='GenSede',
        ),
    ]
