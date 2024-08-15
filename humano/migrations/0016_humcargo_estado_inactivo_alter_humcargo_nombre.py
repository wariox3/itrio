# Generated by Django 4.2.4 on 2024-08-15 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0015_humcargo_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='humcargo',
            name='estado_inactivo',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='humcargo',
            name='nombre',
            field=models.CharField(max_length=200),
        ),
    ]