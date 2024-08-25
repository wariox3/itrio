# Generated by Django 4.2.4 on 2024-08-24 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruteo', '0026_rutvisita_estado_franja'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rutvisita',
            name='decodificado',
        ),
        migrations.RemoveField(
            model_name='rutvisita',
            name='decodificado_error',
        ),
        migrations.AddField(
            model_name='rutvisita',
            name='estado_decodificado',
            field=models.BooleanField(default=None, null=True),
        ),
    ]
