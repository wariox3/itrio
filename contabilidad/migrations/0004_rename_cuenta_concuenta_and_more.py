# Generated by Django 4.2.4 on 2024-07-30 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0091_configuracion_informacion_factura_superior'),
        ('contabilidad', '0003_cuentaclase_remove_cuenta_movimiento_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cuenta',
            new_name='ConCuenta',
        ),
        migrations.RenameModel(
            old_name='CuentaClase',
            new_name='ConCuentaClase',
        ),
        migrations.RenameModel(
            old_name='Movimiento',
            new_name='ConMovimiento',
        ),
    ]