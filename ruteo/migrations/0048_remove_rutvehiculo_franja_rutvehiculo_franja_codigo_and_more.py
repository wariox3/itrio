# Generated by Django 4.2.4 on 2025-03-10 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruteo', '0047_rutdespacho_tiempo_servicio_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rutvehiculo',
            name='franja',
        ),
        migrations.AddField(
            model_name='rutvehiculo',
            name='franja_codigo',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='rutvehiculo',
            name='franja_id',
            field=models.IntegerField(null=True),
        ),
    ]
