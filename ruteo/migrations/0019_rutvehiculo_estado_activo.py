# Generated by Django 4.2.4 on 2024-07-18 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruteo', '0018_rutvehiculo_estado_asignado'),
    ]

    operations = [
        migrations.AddField(
            model_name='rutvehiculo',
            name='estado_activo',
            field=models.BooleanField(default=False),
        ),
    ]