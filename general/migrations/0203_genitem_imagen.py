# Generated by Django 4.2.4 on 2025-03-19 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0202_genarchivo_archivo_tipo_id_genarchivo_codigo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='genitem',
            name='imagen',
            field=models.TextField(null=True),
        ),
    ]
