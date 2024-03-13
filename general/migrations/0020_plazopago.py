# Generated by Django 4.2.4 on 2024-03-13 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0019_rename_reddoc_id_empresa_rededoc_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlazoPago',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('dias', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'gen_plazo_pago',
            },
        ),
    ]
