# Generated by Django 4.2.4 on 2024-08-01 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0095_rename_configuracionusuario_genconfiguracionusuario'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Configuracion',
            new_name='GenConfiguracion',
        ),
    ]
