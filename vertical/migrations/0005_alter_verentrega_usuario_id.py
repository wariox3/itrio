# Generated by Django 4.2.4 on 2025-03-20 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vertical', '0004_verentrega_schema_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verentrega',
            name='usuario_id',
            field=models.IntegerField(null=True),
        ),
    ]
