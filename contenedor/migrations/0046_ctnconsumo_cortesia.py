# Generated by Django 4.2.4 on 2025-03-13 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenedor', '0045_contenedor_cortesia'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctnconsumo',
            name='cortesia',
            field=models.BooleanField(default=False),
        ),
    ]
