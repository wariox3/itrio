# Generated by Django 4.2.4 on 2025-03-08 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0117_humaportecontrato_cotizacion_caja_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='humaportecontrato',
            name='cotizacion_pension_total',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
    ]
