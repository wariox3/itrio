# Generated by Django 4.2.4 on 2025-02-03 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0169_gendocumentodetalle_novedad'),
    ]

    operations = [
        migrations.AddField(
            model_name='genidentificacion',
            name='tipo_persona',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='general.gentipopersona'),
        ),
    ]
