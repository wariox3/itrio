# Generated by Django 4.2.4 on 2024-04-02 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0038_documento_qr'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RespuestaElectronica',
        ),
        migrations.AddField(
            model_name='documento',
            name='estado_electronico_enviado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='documento',
            name='estado_electronico_notificado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='documentotipo',
            name='consecutivo',
            field=models.IntegerField(null=True),
        ),
    ]
