# Generated by Django 4.2.4 on 2024-08-15 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0013_humriesgo_humcontrato_sucursal_humcontrato_riesgo'),
    ]

    operations = [
        migrations.CreateModel(
            name='HumCargo',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'hum_cargo',
            },
        ),
        migrations.CreateModel(
            name='HumSubtipoCotizante',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'hum_subtipo_cotizante',
            },
        ),
        migrations.CreateModel(
            name='HumTipoCotizante',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'hum_tipo_cotizante',
            },
        ),
        migrations.AddField(
            model_name='humcontrato',
            name='cargo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='contratos_cargo_rel', to='humano.humcargo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='humcontrato',
            name='subtipo_cotizante',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='contratos_subtipo_cotizante_rel', to='humano.humsubtipocotizante'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='humcontrato',
            name='tipo_cotizante',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='contratos_tipo_cotizante_rel', to='humano.humtipocotizante'),
            preserve_default=False,
        ),
    ]
