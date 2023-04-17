from django.db import models

class Contacto(models.Model):
    codigo_identificacion_fkm = models.IntegerField(null=True)
    numero_identificacion = models.CharField(max_length=3)
    digito_verificacion = models.CharField(max_length=1)
    nombre_corto = models.CharField(max_length=200)
    nombre1 = models.CharField(max_length=50)
    nombre2 = models.CharField(max_length=50)
    apellido1 = models.CharField(max_length=50)
    apellido2 = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    codigo_ciudad_fkm = models.IntegerField()
    codigo_postal = models.CharField(max_length=20)
    telefono = models.CharField(max_length=50)
    celular = models.CharField(max_length=50)
    correo = models.CharField(max_length=200)
    codigo_tipo_persona_fkm = models.IntegerField(null=True)
    codigo_regimen_fkm = models.IntegerField(null=True)
    codigo_cuenta_cobrar_fk = models.IntegerField(null=True)
    codigo_cuenta_pagar_fk = models.IntegerField(null=True)
    
    class Meta:
        db_table = "gen_contacto"

class Item(models.Model):
    nombre = models.CharField(max_length=200)
    codigo_general = models.CharField(max_length=100, null=True)
    referencia = models.CharField(max_length=50, null=True)
    costo_predeterminado = models.FloatField(default=0)
    precio_predeterminado = models.FloatField(default=0)
    codigo_impuesto_compra_fkm = models.IntegerField(null=True)
    codigo_impuesto_venta_fkm = models.IntegerField(null=True)
    codigo_cuenta_venta_fk = models.IntegerField(null=True)
    codigo_cuenta_costo_venta_fk = models.IntegerField(null=True)
    codigo_cuenta_inventario_fk = models.IntegerField(null=True)
    codigo_marca_fk = models.IntegerField(null=True)
    codigo_medida_fkm = models.IntegerField(null=True)

    class Meta:
        db_table = "gen_item"  