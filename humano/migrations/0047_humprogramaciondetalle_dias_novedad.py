# Generated by Django 4.2.4 on 2024-08-25 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0046_humconcepto_adicional'),
    ]

    operations = [
        migrations.AddField(
            model_name='humprogramaciondetalle',
            name='dias_novedad',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=10),
        ),
    ]
