# Generated by Django 4.2.4 on 2024-07-18 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruteo', '0017_rutdespacho_visitas'),
    ]

    operations = [
        migrations.AddField(
            model_name='rutvehiculo',
            name='estado_asignado',
            field=models.BooleanField(default=False),
        ),
    ]
