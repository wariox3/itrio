# Generated by Django 4.2.4 on 2024-08-01 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0107_rename_estado_genestado'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Identificacion',
            new_name='GenIdentificacion',
        ),
    ]
