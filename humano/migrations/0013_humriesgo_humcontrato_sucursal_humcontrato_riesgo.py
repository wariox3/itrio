# Generated by Django 4.2.4 on 2024-08-15 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0012_humsucursal_humcontrato_auxilio_transporte_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HumRiesgo',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=100)),
                ('porcentaje', models.DecimalField(decimal_places=3, default=0, max_digits=6)),
            ],
            options={
                'db_table': 'hum_riesgo',
            },
        ),
        migrations.AddField(
            model_name='humcontrato',
            name='sucursal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contratos_sucursal_rel', to='humano.humsucursal'),
        ),
        migrations.AddField(
            model_name='humcontrato',
            name='riesgo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='contratos_riesgo_rel', to='humano.humriesgo'),
            preserve_default=False,
        ),
    ]