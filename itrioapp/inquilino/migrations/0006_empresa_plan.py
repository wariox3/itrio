# Generated by Django 4.2 on 2023-07-11 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inquilino', '0005_alter_plan_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inquilino.plan'),
        ),
    ]
