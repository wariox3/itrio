# Generated by Django 4.2.4 on 2025-07-02 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('humano', '0009_alter_humpension_options_alter_humsalud_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='humtipocosto',
            options={'ordering': ['id']},
        ),
    ]
