# Generated by Django 4.2.4 on 2025-02-25 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0186_gendocumentodetalle_almacen'),
        ('inventario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvExistencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('existencia', models.FloatField(default=0)),
                ('remision', models.FloatField(default=0)),
                ('disponible', models.FloatField(default=0)),
                ('almacen', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='existencias_almacen_rel', to='inventario.invalmacen')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='existencias_item_rel', to='general.genitem')),
            ],
            options={
                'db_table': 'inv_existencia',
            },
        ),
    ]
