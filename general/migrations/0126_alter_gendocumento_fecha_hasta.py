# Generated by Django 4.2.4 on 2024-08-15 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0125_gendocumento_contrato_gendocumento_deduccion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gendocumento',
            name='fecha_hasta',
            field=models.DateField(null=True),
        ),
    ]
