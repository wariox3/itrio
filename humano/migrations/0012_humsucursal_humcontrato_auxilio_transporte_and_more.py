# Generated by Django 4.2.4 on 2024-08-15 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0011_humcredito'),
    ]

    operations = [
        migrations.CreateModel(
            name='HumSucursal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'hum_sucursal',
            },
        ),
        migrations.AddField(
            model_name='humcontrato',
            name='auxilio_transporte',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='humcontrato',
            name='comentario',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='humcontrato',
            name='salario',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
        migrations.AddField(
            model_name='humcontrato',
            name='salario_integral',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='humprogramacion',
            name='comentario',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
