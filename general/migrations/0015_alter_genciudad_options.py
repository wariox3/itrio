# Generated by Django 4.2.4 on 2025-06-25 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0014_alter_genitemimpuesto_item'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genciudad',
            options={'ordering': ['nombre']},
        ),
    ]
