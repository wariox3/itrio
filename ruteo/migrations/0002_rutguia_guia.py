# Generated by Django 4.2.4 on 2024-07-08 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruteo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rutguia',
            name='guia',
            field=models.IntegerField(null=True),
        ),
    ]