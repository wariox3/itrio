# Generated by Django 4.2.4 on 2025-01-29 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0167_genconfiguracion_hum_entidad_riesgo'),
    ]

    operations = [
        migrations.AddField(
            model_name='genidentificacion',
            name='aporte',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
