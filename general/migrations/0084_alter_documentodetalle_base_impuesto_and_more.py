# Generated by Django 4.2.4 on 2024-06-22 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0083_alter_documentoimpuesto_base_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentodetalle',
            name='base_impuesto',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='documentodetalle',
            name='descuento',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='documentodetalle',
            name='impuesto',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='documentodetalle',
            name='pago',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='documentodetalle',
            name='porcentaje_descuento',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='documentodetalle',
            name='precio',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='documentodetalle',
            name='subtotal',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='documentodetalle',
            name='total',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='documentodetalle',
            name='total_bruto',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
    ]
