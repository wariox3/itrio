# Generated by Django 4.2.4 on 2024-04-11 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0046_documento_fecha_validacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='subdominio',
            field=models.CharField(default='demo', max_length=100),
        ),
    ]
