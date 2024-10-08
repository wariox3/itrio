# Generated by Django 4.2.4 on 2024-08-15 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0121_gendocumentodetalle_contacto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='genconfiguracion',
            name='gen_uvt',
            field=models.DecimalField(decimal_places=6, default=47065, max_digits=20),
        ),
        migrations.AddField(
            model_name='genconfiguracion',
            name='hum_auxilio_transporte',
            field=models.DecimalField(decimal_places=6, default=162000, max_digits=20),
        ),
        migrations.AddField(
            model_name='genconfiguracion',
            name='hum_factor',
            field=models.DecimalField(decimal_places=3, default=7.667, max_digits=6),
        ),
        migrations.AddField(
            model_name='genconfiguracion',
            name='hum_salario_minimo',
            field=models.DecimalField(decimal_places=6, default=1300000, max_digits=20),
        ),
    ]
