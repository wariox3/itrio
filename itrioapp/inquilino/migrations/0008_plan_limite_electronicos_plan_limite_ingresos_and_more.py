# Generated by Django 4.2 on 2023-07-11 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquilino', '0007_alter_dominio_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='limite_electronicos',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='plan',
            name='limite_ingresos',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='plan',
            name='limite_usuarios',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='plan',
            name='precio',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='plan',
            name='precio_usuario_adicional',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='plan',
            name='usuarios_base',
            field=models.IntegerField(default=0),
        ),
    ]
