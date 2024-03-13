# Generated by Django 4.2.4 on 2024-03-13 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0017_asesor'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacto',
            name='asesor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='general.asesor'),
        ),
        migrations.AddField(
            model_name='contacto',
            name='precio',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='general.precio'),
        ),
    ]
