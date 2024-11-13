# Generated by Django 4.2.4 on 2024-11-13 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ruteo', '0029_alter_rutvisita_ciudad_alter_rutvisita_destinatario_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RutFlota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='flotas_vehiculo_rel', to='ruteo.rutvehiculo')),
            ],
            options={
                'db_table': 'rut_flota',
            },
        ),
    ]
