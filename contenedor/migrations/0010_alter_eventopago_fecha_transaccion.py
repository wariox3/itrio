# Generated by Django 4.2.4 on 2024-06-13 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenedor', '0009_eventopago_correo_eventopago_estado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventopago',
            name='fecha_transaccion',
            field=models.DateTimeField(null=True),
        ),
    ]
