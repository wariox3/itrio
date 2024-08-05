# Generated by Django 4.2.4 on 2024-08-05 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0007_alter_concuenta_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='concuenta',
            name='exige_base',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='concuenta',
            name='exige_tercero',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='concuenta',
            name='permite_movimiento',
            field=models.BooleanField(default=False),
        ),
    ]
