# Generated by Django 4.2.4 on 2025-01-09 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0072_remove_humaportecontrato_cantidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='humprogramaciondetalle',
            name='salario_promedio',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
    ]
