# Generated by Django 4.2.4 on 2024-07-27 17:58

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenedor', '0022_rename_eventopago_ctneventopago'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ContenedorMovimiento',
            new_name='CtnMovimiento',
        ),
    ]
