# Generated by Django 4.2.4 on 2024-08-01 23:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contabilidad', '0006_concomprobante'),
        ('general', '0100_rename_documentoclase_gendocumentoclase'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DocumentoDetalle',
            new_name='GenDocumentoDetalle',
        ),
    ]
