# Generated by Django 4.2.4 on 2024-08-25 19:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0047_humprogramaciondetalle_dias_novedad'),
    ]

    operations = [
        migrations.AddField(
            model_name='humnovedadtipo',
            name='concepto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='novedades_tipos_concepto_rel', to='humano.humconcepto'),
        ),
    ]
