# Generated by Django 4.2.4 on 2025-03-10 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruteo', '0040_rutdespacho_estado_terminado_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rutvisita',
            name='franja',
        ),
        migrations.AddField(
            model_name='rutvisita',
            name='franja_codigo',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
