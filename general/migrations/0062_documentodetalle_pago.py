# Generated by Django 4.2.4 on 2024-05-16 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0061_configuracion_informacion_factura'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentodetalle',
            name='pago',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]
