# Generated by Django 4.2.4 on 2025-07-03 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenedor', '0003_alter_ctnplan_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctnsocio',
            name='porcentaje_comision',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=16),
        ),
    ]
