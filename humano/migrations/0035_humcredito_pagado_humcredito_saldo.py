# Generated by Django 4.2.4 on 2024-08-19 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0034_humcredito_inactivo_humcredito_inactivo_periodo'),
    ]

    operations = [
        migrations.AddField(
            model_name='humcredito',
            name='pagado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='humcredito',
            name='saldo',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=20),
        ),
    ]
