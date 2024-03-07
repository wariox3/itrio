# Generated by Django 4.2.4 on 2024-03-07 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenedor', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContenedorRegimen',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'cnt_regimen',
            },
        ),
        migrations.CreateModel(
            name='ContenedorTipoPersona',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'cnt_tipo_persona',
            },
        ),
    ]
