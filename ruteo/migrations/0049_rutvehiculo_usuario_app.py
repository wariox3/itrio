# Generated by Django 4.2.4 on 2025-03-19 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruteo', '0048_remove_rutvehiculo_franja_rutvehiculo_franja_codigo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rutvehiculo',
            name='usuario_app',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
