# Generated by Django 4.2.4 on 2025-02-25 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0031_conmovimiento_cierre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conmovimiento',
            name='base',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
    ]
