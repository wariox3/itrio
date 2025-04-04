# Generated by Django 4.2.4 on 2025-03-07 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0032_alter_conmovimiento_base'),
        ('humano', '0110_humconfiguracionprovision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='humconfiguracionprovision',
            name='cuenta_credito',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='configuraciones_provisiones_cuenta_credito_rel', to='contabilidad.concuenta'),
        ),
        migrations.AlterField(
            model_name='humconfiguracionprovision',
            name='cuenta_debito',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='configuraciones_provisiones_cuenta_debito_rel', to='contabilidad.concuenta'),
        ),
    ]
