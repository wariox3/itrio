# Generated by Django 4.2.4 on 2024-09-23 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0018_concuentagrupo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConCuentaSubcuenta',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'con_cuenta_subcuenta',
            },
        ),
    ]