# Generated by Django 4.2.4 on 2024-08-16 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0025_alter_humconceptonomina_options'),
        ('general', '0127_gendocumentodetalle_hora_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gendocumentodetalle',
            name='concepto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='documentos_detalles_concepto_rel', to='humano.humconcepto'),
        ),
    ]
