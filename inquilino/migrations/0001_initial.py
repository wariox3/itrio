# Generated by Django 4.2 on 2023-08-08 19:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, null=True)),
                ('limite_usuarios', models.IntegerField(default=0)),
                ('usuarios_base', models.IntegerField(default=0)),
                ('limite_ingresos', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('precio', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('precio_usuario_adicional', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('limite_electronicos', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
            ],
            options={
                'db_table': 'inq_plan',
            },
        ),
        migrations.CreateModel(
            name='Verificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario_id', models.IntegerField(null=True)),
                ('empresa_id', models.IntegerField(null=True)),
                ('token', models.CharField(max_length=50)),
                ('estado_usado', models.BooleanField(default=False)),
                ('vence', models.DateField(null=True)),
                ('accion', models.CharField(default='registro', max_length=10)),
                ('usuario_invitado_username', models.EmailField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'inq_verificacion',
            },
        ),
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=20, null=True)),
                ('fecha', models.DateField(null=True)),
                ('vr_total', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('vr_afectado', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('vr_saldo', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'inq_movimiento',
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema_name', models.CharField(max_length=100)),
                ('nombre', models.CharField(max_length=200, null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('imagen', models.TextField(null=True)),
                ('usuario_id', models.IntegerField(null=True)),
                ('usuarios', models.IntegerField(default=1)),
                ('plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inquilino.plan')),
            ],
            options={
                'db_table': 'inq_empresa',
            },
        ),
        migrations.CreateModel(
            name='Dominio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=253, unique=True)),
                ('is_primary', models.BooleanField(db_index=True, default=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='inquilino.empresa')),
            ],
            options={
                'db_table': 'inq_dominio',
            },
        ),
        migrations.CreateModel(
            name='Consumo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(null=True)),
                ('empresa_id', models.IntegerField(null=True)),
                ('empresa', models.CharField(max_length=200, null=True)),
                ('usuarios', models.IntegerField(default=0)),
                ('vr_plan', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('vr_usuario_adicional', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('vr_total', models.DecimalField(decimal_places=2, default=0, max_digits=16)),
                ('plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inquilino.plan')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'inq_consumo',
            },
        ),
        migrations.CreateModel(
            name='UsuarioEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(max_length=20, null=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inquilino.empresa')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'inq_usuario_empresa',
                'unique_together': {('usuario', 'empresa')},
            },
        ),
    ]
