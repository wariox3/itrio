# Generated by Django 4.2.4 on 2024-03-08 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0010_documento_cobrar_documento_cobrar_afectado_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documentodetalle',
            old_name='documentoAfectado',
            new_name='documento_fectado',
        ),
    ]
