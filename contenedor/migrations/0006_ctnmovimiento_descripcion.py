# Generated by Django 4.2.4 on 2025-07-04 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenedor', '0005_alter_ctnmovimiento_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctnmovimiento',
            name='descripcion',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
