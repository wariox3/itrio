# Generated by Django 4.2.4 on 2025-03-13 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0034_conactivo_metodo_depreciacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='conactivo',
            name='depreciacion_periodo',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
    ]
