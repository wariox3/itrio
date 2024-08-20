# Generated by Django 4.2.4 on 2024-08-19 23:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0036_humconceptotipo_humconcepto_concepto_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='humcredito',
            name='concepto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='creditos_concepto_rel', to='humano.humconcepto'),
        ),
    ]
