# Generated by Django 4.2.4 on 2024-03-22 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0031_documento_comentario_documento_cue_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='base_impuesto',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='documento',
            name='cobrar',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='documento',
            name='cobrar_afectado',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='documento',
            name='cobrar_pendiente',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='documento',
            name='descuento',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='documento',
            name='impuesto',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='documento',
            name='subtotal',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='documento',
            name='total',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='documento',
            name='total_bruto',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='documentodetalle',
            name='descuento',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='documentodetalle',
            name='porcentaje_descuento',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='documentodetalle',
            name='precio',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='documentodetalle',
            name='subtotal',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='documentodetalle',
            name='total',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='documentodetalle',
            name='total_bruto',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=12),
        ),
    ]
