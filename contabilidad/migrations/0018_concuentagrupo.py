# Generated by Django 4.2.4 on 2024-09-23 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0017_alter_concuenta_codigo_alter_concuenta_nombre'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConCuentaGrupo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'con_cuenta_grupo',
            },
        ),
    ]