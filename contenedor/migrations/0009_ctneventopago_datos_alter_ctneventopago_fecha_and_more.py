# Generated by Django 4.2.4 on 2025-07-23 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenedor', '0008_alter_ctndireccion_direccion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctneventopago',
            name='datos',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ctneventopago',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='ctneventopago',
            name='referencia',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
