# Generated by Django 4.2.4 on 2024-11-27 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruteo', '0036_alter_rutvisita_latitud_alter_rutvisita_longitud'),
    ]

    operations = [
        migrations.AddField(
            model_name='rutvisita',
            name='resultados',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
