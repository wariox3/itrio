# Generated by Django 4.2.4 on 2024-11-14 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0149_genparametros'),
    ]

    operations = [
        migrations.AddField(
            model_name='gendocumento',
            name='evento_aceptacion',
            field=models.CharField(default='PE', max_length=2),
        ),
        migrations.AddField(
            model_name='gendocumento',
            name='evento_documento',
            field=models.CharField(default='PE', max_length=2),
        ),
        migrations.AddField(
            model_name='gendocumento',
            name='evento_recepcion',
            field=models.CharField(default='PE', max_length=2),
        ),
    ]
