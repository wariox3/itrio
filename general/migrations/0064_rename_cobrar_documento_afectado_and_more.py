# Generated by Django 4.2.4 on 2024-05-23 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0063_documentoclase_grupo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documento',
            old_name='cobrar',
            new_name='afectado',
        ),
        migrations.RenameField(
            model_name='documento',
            old_name='cobrar_afectado',
            new_name='pendiente',
        ),
        migrations.RemoveField(
            model_name='documento',
            name='cobrar_pendiente',
        ),
    ]
