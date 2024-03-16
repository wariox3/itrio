# Generated by Django 4.2.4 on 2024-03-13 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0018_contacto_asesor_contacto_precio'),
    ]

    operations = [
        migrations.RenameField(
            model_name='empresa',
            old_name='reddoc_id',
            new_name='rededoc_id',
        ),
        migrations.AlterField(
            model_name='asesor',
            name='celular',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='asesor',
            name='correo',
            field=models.EmailField(max_length=255),
        ),
        migrations.AlterField(
            model_name='asesor',
            name='nombre_corto',
            field=models.CharField(max_length=200),
        ),
    ]