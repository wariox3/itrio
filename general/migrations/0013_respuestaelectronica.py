# Generated by Django 4.2.4 on 2024-03-11 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0012_cuentabancotipo_cuentabanco'),
    ]

    operations = [
        migrations.CreateModel(
            name='RespuestaElectronica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_estatus', models.CharField(max_length=10, null=True)),
                ('proceso_dian', models.CharField(max_length=1, null=True)),
                ('mensaje_error', models.TextField(null=True)),
                ('razon_error', models.TextField(null=True)),
                ('codigo_modelo', models.IntegerField()),
                ('fecha', models.DateField()),
            ],
            options={
                'db_table': 'gen_respuesta_electronica',
            },
        ),
    ]