# Generated by Django 4.2.4 on 2025-01-27 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguridad', '0006_user_numero_identificacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cargo',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
