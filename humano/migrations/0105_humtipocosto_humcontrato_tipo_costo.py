# Generated by Django 4.2.4 on 2025-03-06 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0104_humprogramaciondetalle_base_cotizacion_acumulado_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HumTipoCosto',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'hum_tipo_costo',
            },
        ),
        migrations.AddField(
            model_name='humcontrato',
            name='tipo_costo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contratos_tipo_costo_rel', to='humano.humtipocosto'),
        ),
    ]
