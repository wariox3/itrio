# Generated by Django 4.2.4 on 2024-04-05 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0044_remove_resolucion_ambiente'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='electronico_id',
            field=models.IntegerField(null=True),
        ),
    ]
