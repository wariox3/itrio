# Generated by Django 4.2.4 on 2024-07-26 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenedor', '0017_alter_contenedormovimiento_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventopago',
            name='fecha',
            field=models.DateTimeField(),
        ),
    ]
