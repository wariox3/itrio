# Generated by Django 4.2.4 on 2024-07-16 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruteo', '0016_alter_rutdespacho_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='rutdespacho',
            name='visitas',
            field=models.FloatField(default=0),
        ),
    ]
