# Generated by Django 4.2.4 on 2024-05-30 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0065_documentodetalle_cuenta_alter_documentodetalle_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentodetalle',
            name='naturaleza',
            field=models.CharField(max_length=1, null=True),
        ),
    ]
