# Generated by Django 4.2.4 on 2024-07-10 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruteo', '0008_rename_rutguia_rutvisita_alter_rutvisita_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='rutvisita',
            name='ciudad',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='rutvisita',
            name='estado',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='rutvisita',
            name='pais',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
