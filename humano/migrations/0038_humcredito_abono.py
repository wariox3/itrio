# Generated by Django 4.2.4 on 2024-08-19 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0037_humcredito_concepto'),
    ]

    operations = [
        migrations.AddField(
            model_name='humcredito',
            name='abono',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
    ]