# Generated by Django 4.2.4 on 2025-02-26 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0188_gendocumentodetalle_operacion_inventario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gendocumentodetalle',
            name='cantidad_operada',
            field=models.FloatField(default=0),
        ),
    ]
