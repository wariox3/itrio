# Generated by Django 4.2.4 on 2025-02-28 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0190_remove_genconfiguracion_venta_asesor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gendocumentodetalle',
            name='base',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
    ]
