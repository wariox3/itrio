# Generated by Django 4.2.4 on 2024-06-21 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0076_impuesto_porcentaje_base'),
    ]

    operations = [
        migrations.AlterField(
            model_name='impuesto',
            name='porcentaje_base',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=10),
        ),
    ]