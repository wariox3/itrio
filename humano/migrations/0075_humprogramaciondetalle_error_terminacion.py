# Generated by Django 4.2.4 on 2025-01-20 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0074_humcredito_comentario'),
    ]

    operations = [
        migrations.AddField(
            model_name='humprogramaciondetalle',
            name='error_terminacion',
            field=models.BooleanField(default=False),
        ),
    ]
