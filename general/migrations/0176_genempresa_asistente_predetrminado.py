# Generated by Django 4.2.4 on 2025-02-08 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0175_genimpuesto_cuenta'),
    ]

    operations = [
        migrations.AddField(
            model_name='genempresa',
            name='asistente_predetrminado',
            field=models.BooleanField(default=False),
        ),
    ]
