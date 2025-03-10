# Generated by Django 4.2.4 on 2025-03-07 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0032_alter_conmovimiento_base'),
        ('humano', '0109_remove_humpagotipo_cuenta'),
    ]

    operations = [
        migrations.CreateModel(
            name='HumConfiguracionProvision',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=20, null=True)),
                ('orden', models.IntegerField(default=0)),
                ('cuenta_credito', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='configuraciones_provisiones_cuenta_credito_rel', to='contabilidad.concuenta')),
                ('cuenta_debito', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='configuraciones_provisiones_cuenta_debito_rel', to='contabilidad.concuenta')),
                ('tipo_costo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='configuraciones_provisiones_tipo_costo_rel', to='humano.humtipocosto')),
            ],
            options={
                'db_table': 'hum_configuracion_provision',
            },
        ),
    ]
