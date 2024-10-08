# Generated by Django 4.2.4 on 2024-08-15 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0022_humpension_humsalud_humcontrato_pension_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='humpension',
            name='porcentaje_empleado',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='humpension',
            name='porcentaje_empleador',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=6),
        ),
    ]
