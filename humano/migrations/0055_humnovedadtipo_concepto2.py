# Generated by Django 4.2.4 on 2024-08-26 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0054_humnovedad_pago_dia_dinero'),
    ]

    operations = [
        migrations.AddField(
            model_name='humnovedadtipo',
            name='concepto2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='novedades_tipos_concepto2_rel', to='humano.humconcepto'),
        ),
    ]
