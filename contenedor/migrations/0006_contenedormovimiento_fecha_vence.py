# Generated by Django 4.2.4 on 2024-06-12 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenedor', '0005_consumo_subdominio'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenedormovimiento',
            name='fecha_vence',
            field=models.DateField(null=True),
        ),
    ]