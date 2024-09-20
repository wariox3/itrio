# Generated by Django 4.2.4 on 2024-09-20 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0063_humentidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='humcontrato',
            name='entidad_caja',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contratos_entidad_caja_rel', to='humano.humentidad'),
        ),
        migrations.AddField(
            model_name='humcontrato',
            name='entidad_cesantias',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contratos_entidad_cesantias_rel', to='humano.humentidad'),
        ),
        migrations.AddField(
            model_name='humcontrato',
            name='entidad_pension',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contratos_entidad_pension_rel', to='humano.humentidad'),
        ),
        migrations.AddField(
            model_name='humcontrato',
            name='entidad_salud',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contratos_entidad_salud_rel', to='humano.humentidad'),
        ),
    ]
