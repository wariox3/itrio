# Generated by Django 4.2.4 on 2024-09-18 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0059_humnovedad_fecha_desde_empresa_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HumPeriodo',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'hum_periodo',
            },
        ),
    ]
