# Generated by Django 4.2.4 on 2024-03-19 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0023_ciudad_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacto',
            name='celular',
            field=models.CharField(max_length=50, null=True, verbose_name='Celular'),
        ),
    ]
