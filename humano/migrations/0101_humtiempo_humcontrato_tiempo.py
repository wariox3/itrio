# Generated by Django 4.2.4 on 2025-02-12 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0100_humaporteentidad'),
    ]

    operations = [
        migrations.CreateModel(
            name='HumTiempo',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=200)),
                ('factor', models.DecimalField(decimal_places=3, default=0, max_digits=6)),
            ],
            options={
                'db_table': 'hum_tiempo',
            },
        ),
        migrations.AddField(
            model_name='humcontrato',
            name='tiempo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='contratos_tiempo_rel', to='humano.humtiempo'),
        ),
    ]
