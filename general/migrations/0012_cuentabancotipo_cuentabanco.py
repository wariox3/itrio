# Generated by Django 4.2.4 on 2024-03-08 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0011_rename_documentoafectado_documentodetalle_documento_fectado'),
    ]

    operations = [
        migrations.CreateModel(
            name='CuentaBancoTipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'gen_cuenta_banco_tipo',
            },
        ),
        migrations.CreateModel(
            name='CuentaBanco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('numero_cuenta', models.CharField(max_length=50, null=True)),
                ('cuenta_banco_tipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cuentas_bancos', to='general.cuentabancotipo')),
            ],
            options={
                'db_table': 'gen_cuenta_banco',
            },
        ),
    ]