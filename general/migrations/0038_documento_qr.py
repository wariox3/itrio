# Generated by Django 4.2.4 on 2024-03-22 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0037_alter_documento_base_impuesto_alter_documento_cobrar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='qr',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
