# Generated by Django 4.2.4 on 2024-06-13 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenedor', '0006_contenedormovimiento_fecha_vence'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventoPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('evento', models.CharField(max_length=50, null=True)),
                ('entorno', models.CharField(max_length=10, null=True)),
                ('fecha', models.DateField()),
            ],
            options={
                'db_table': 'cnt_evento_pago',
            },
        ),
    ]
