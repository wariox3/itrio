# Generated by Django 4.2.4 on 2025-03-10 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruteo', '0041_remove_rutvisita_franja_rutvisita_franja_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='rutvisita',
            name='franja_id',
            field=models.IntegerField(null=True),
        ),
    ]
