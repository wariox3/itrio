# Generated by Django 4.2.4 on 2024-06-04 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0067_documentotipo_cuenta_cobrar'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacto',
            name='cliente',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contacto',
            name='plazo_pago_proveedor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contactos_plazo_pago_proveedor', to='general.plazopago'),
        ),
        migrations.AddField(
            model_name='contacto',
            name='proveedor',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='contacto',
            name='plazo_pago',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contactos_plazo_pago', to='general.plazopago'),
        ),
    ]
