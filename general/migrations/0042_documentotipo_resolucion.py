# Generated by Django 4.2.4 on 2024-04-02 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0041_alter_documentotipo_consecutivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentotipo',
            name='resolucion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documentos_tipos', to='general.resolucion'),
        ),
    ]
