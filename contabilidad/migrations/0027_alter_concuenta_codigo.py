# Generated by Django 4.2.4 on 2024-11-29 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0026_alter_congrupo_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concuenta',
            name='codigo',
            field=models.CharField(default='0', max_length=20, unique=True),
        ),
    ]
