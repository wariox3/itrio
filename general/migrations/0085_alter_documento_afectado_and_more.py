# Generated by Django 4.2.4 on 2024-06-22 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0084_alter_documentodetalle_base_impuesto_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='afectado',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='documento',
            name='base_impuesto',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='documento',
            name='descuento',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='documento',
            name='impuesto',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='documento',
            name='pendiente',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='documento',
            name='subtotal',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='documento',
            name='total',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='documento',
            name='total_bruto',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
    ]
