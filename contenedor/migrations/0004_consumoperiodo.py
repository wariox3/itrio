# Generated by Django 4.2.4 on 2024-06-12 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenedor', '0003_contenedorregimen_contenedortipopersona'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumoPeriodo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
            ],
            options={
                'db_table': 'cnt_consumo_periodo',
            },
        ),
    ]
