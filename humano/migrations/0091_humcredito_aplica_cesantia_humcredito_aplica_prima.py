# Generated by Django 4.2.4 on 2025-02-03 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0090_humsucursal_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='humcredito',
            name='aplica_cesantia',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='humcredito',
            name='aplica_prima',
            field=models.BooleanField(default=False),
        ),
    ]
