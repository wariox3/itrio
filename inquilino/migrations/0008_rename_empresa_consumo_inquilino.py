# Generated by Django 4.2.4 on 2023-09-22 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inquilino', '0007_rename_empresa_id_consumo_inquilino_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consumo',
            old_name='empresa',
            new_name='inquilino',
        ),
    ]
