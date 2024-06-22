# Generated by Django 4.2.4 on 2024-06-22 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0080_documentoimpuesto_porcentaje_base'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentoimpuesto',
            name='base',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='documentoimpuesto',
            name='porcentaje',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='documentoimpuesto',
            name='porcentaje_base',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=15),
        ),
        migrations.AlterField(
            model_name='documentoimpuesto',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]
