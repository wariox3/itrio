# Generated by Django 4.2.4 on 2024-07-19 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguridad', '0003_alter_user_fecha_creacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cortesia',
            field=models.BooleanField(default=False),
        ),
    ]
