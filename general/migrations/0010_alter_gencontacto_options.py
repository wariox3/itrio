# Generated by Django 4.2.4 on 2025-06-11 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0009_alter_gendocumentodetalle_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gencontacto',
            options={'ordering': ['-id']},
        ),
    ]
