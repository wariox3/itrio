# Generated by Django 4.2.4 on 2023-09-21 14:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inquilino', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarioinquilino',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='movimiento',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inquilino',
            name='plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inquilino.plan'),
        ),
        migrations.AddField(
            model_name='dominio',
            name='tenant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='inquilino.inquilino'),
        ),
        migrations.AddField(
            model_name='consumo',
            name='plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inquilino.plan'),
        ),
        migrations.AddField(
            model_name='consumo',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='usuarioinquilino',
            unique_together={('usuario', 'inquilino')},
        ),
    ]
