# Generated by Django 4.2.4 on 2025-01-29 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0080_humaporte_presentacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='humaporte',
            name='entidad_riesgo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='humano.humentidad'),
        ),
    ]
