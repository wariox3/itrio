# Generated by Django 4.2.4 on 2023-11-10 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0003_rename_fechadesde_resolucion_fecha_desde_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resolucion',
            name='ambiente',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='resolucion',
            name='clave_tecnica',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='resolucion',
            name='set_prueba',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='resolucion',
            name='numero',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='resolucion',
            name='prefijo',
            field=models.CharField(max_length=50, null=True),
        ),
    ]