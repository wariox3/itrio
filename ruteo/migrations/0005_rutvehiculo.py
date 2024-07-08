# Generated by Django 4.2.4 on 2024-07-08 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruteo', '0004_rename_destinatariocorreo_rutguia_destinatario_correo_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RutVehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=10, null=True)),
                ('capacidad', models.FloatField(default=0)),
            ],
            options={
                'db_table': 'rut_vehiculo',
            },
        ),
    ]
