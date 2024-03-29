# Generated by Django 4.2.4 on 2024-03-14 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuenta',
            name='movimiento',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cuenta',
            name='requiere_centro_costo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cuenta',
            name='requiere_tercero',
            field=models.BooleanField(default=False),
        ),
    ]
