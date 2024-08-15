# Generated by Django 4.2.4 on 2024-08-15 18:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0021_humprogramaciondetalle_ingreso'),
    ]

    operations = [
        migrations.CreateModel(
            name='HumPension',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'hum_pension',
            },
        ),
        migrations.CreateModel(
            name='HumSalud',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'hum_salud',
            },
        ),
        migrations.AddField(
            model_name='humcontrato',
            name='pension',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contratos_pension_rel', to='humano.humpension'),
        ),
        migrations.AddField(
            model_name='humcontrato',
            name='salud',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contratos_salud_rel', to='humano.humsalud'),
        ),
    ]