# Generated by Django 4.2.4 on 2024-08-22 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0134_gencomplemento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gencomplemento',
            name='datos_json',
            field=models.JSONField(null=True),
        ),
    ]
