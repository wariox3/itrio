# Generated by Django 4.2.4 on 2024-08-01 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0111_rename_item_genitem'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MetodoPago',
            new_name='GenMetodoPago',
        ),
    ]
