# Generated by Django 4.2.4 on 2024-08-12 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transporte', '0002_rename_guia_tteguia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tteguia',
            name='fechaDespacho',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='tteguia',
            name='fechaEntrega',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='tteguia',
            name='fechaIngreso',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='tteguia',
            name='fechaRecogida',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='tteguia',
            name='fechaSoporte',
            field=models.DateTimeField(null=True),
        ),
    ]
