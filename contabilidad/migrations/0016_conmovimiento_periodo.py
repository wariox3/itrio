# Generated by Django 4.2.4 on 2024-08-11 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0015_conperiodo'),
    ]

    operations = [
        migrations.AddField(
            model_name='conmovimiento',
            name='periodo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='movimientos_periodo_rel', to='contabilidad.conperiodo'),
            preserve_default=False,
        ),
    ]
