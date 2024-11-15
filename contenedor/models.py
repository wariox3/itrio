from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from seguridad.models import User

class CtnPais(models.Model):
    id = models.CharField(primary_key=True, max_length=2)
    nombre = models.CharField(max_length=50, null=True)
    codigo = models.CharField(max_length=10, null=True)
    
    class Meta:
        db_table = "cnt_pais"

class CtnEstado(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=10, null=True)
    pais = models.ForeignKey(CtnPais, on_delete=models.CASCADE)

    class Meta:
        db_table = "cnt_estado"

class CtnCiudad(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50) 
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    codigo_postal = models.CharField(max_length=10, null=True)
    porcentaje_impuesto = models.DecimalField(max_digits=5, decimal_places=2, default=0)  
    estado = models.ForeignKey(CtnEstado, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "cnt_ciudad"      
        
class CtnRegimen(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50) 
    
    class Meta:
        db_table = "cnt_regimen"  

class CtnTipoPersona(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50) 
    
    class Meta:
        db_table = "cnt_tipo_persona"  

class CtnIdentificacion(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)    
    orden = models.BigIntegerField(default=0)
    codigo = models.CharField(max_length=10, null=True)
    pais = models.ForeignKey(CtnPais, on_delete=models.CASCADE, null=True)
    
    class Meta:
        db_table = "cnt_identificacion"

class CtnSocio(models.Model):
    nombre = models.CharField(max_length=100)    
    
    class Meta:
        db_table = "cnt_socio"

class CtnPlan(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50, null=True)
    limite_usuarios = models.IntegerField(default=0)
    usuarios_base = models.IntegerField(default=0)
    limite_ingresos = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    precio = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    precio_usuario_adicional = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    limite_electronicos = models.DecimalField(max_digits=16, decimal_places=2, default=0)

    class Meta:
        db_table = "cnt_plan"

class Contenedor(TenantMixin):
    schema_name = models.CharField(max_length=100)
    nombre = models.CharField(max_length=200, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    imagen = models.TextField(null=True)
    #usuario_id = models.IntegerField(null=True)
    usuarios = models.IntegerField(default=1) 
    reddoc = models.BooleanField(default = False)
    ruteo = models.BooleanField(default = False)
    plan = models.ForeignKey(CtnPlan, on_delete=models.CASCADE, null=True)         
    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True
    auto_drop_schema = True
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.schema_name
    
    class Meta:
        db_table = "cnt_contenedor"

class Dominio(DomainMixin):
    pass

    class Meta:
        db_table = "cnt_dominio"

class CtnConsumoPeriodo(models.Model):
    fecha = models.DateField()
    class Meta:
        db_table = "cnt_consumo_periodo"

class CtnConsumo(models.Model):
    fecha = models.DateField(null=True)
    contenedor_id = models.IntegerField(null=True)
    contenedor = models.CharField(max_length=200, null=True) 
    subdominio = models.CharField(max_length=100, null=True)   
    usuarios = models.IntegerField(default=0) 
    vr_plan = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    vr_usuario_adicional = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    vr_total = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    plan = models.ForeignKey(CtnPlan, on_delete=models.CASCADE, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "cnt_consumo"

class CtnVerificacion(models.Model):
    usuario_id = models.IntegerField(null=True)
    contenedor_id = models.IntegerField(null=True)
    token = models.CharField(max_length=50)
    estado_usado = models.BooleanField(default = False)
    vence = models.DateField(null=True)
    accion = models.CharField(max_length=10, default='registro')
    usuario_invitado_username = models.EmailField(max_length = 255, null=True)

    class Meta:
        db_table = "cnt_verificacion" 

class UsuarioContenedor(models.Model):
    rol = models.CharField(max_length=20, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenedor = models.ForeignKey(Contenedor, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('usuario', 'contenedor')
        db_table = "cnt_usuario_contenedor"        

class CtnMovimiento(models.Model):
    tipo = models.CharField(max_length=20, null=True)
    fecha = models.DateTimeField(null=True)
    fecha_vence = models.DateField(null=True)    
    vr_total = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    vr_afectado = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    vr_saldo = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    contenedor_movimiento_id = models.IntegerField(null=True) 
    documento_fisico = models.BooleanField(default = False) 
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    socio = models.ForeignKey(CtnSocio, on_delete=models.CASCADE, null=True)
    class Meta:
        db_table = "cnt_movimiento"   

class CtnEventoPago(models.Model):
    fecha = models.DateTimeField()    
    evento = models.CharField(max_length=50, null=True)
    entorno = models.CharField(max_length=10, null=True)
    transaccion = models.CharField(max_length=50, null=True)    
    metodo_pago = models.CharField(max_length=50, null=True)
    referencia = models.CharField(max_length=50, null=True)    
    correo = models.CharField(max_length=250, null=True)
    estado = models.CharField(max_length=50, null=True)
    fecha_transaccion = models.DateTimeField(null=True)
    estado_aplicado = models.BooleanField(default = False)
    vr_original = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    vr_aplicar = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    class Meta:
        db_table = "cnt_evento_pago"              

class CtnInformacionFacturacion(models.Model):
    numero_identificacion = models.CharField(max_length=20, null=True)
    digito_verificacion = models.CharField(max_length=1, null=True)
    nombre_corto = models.CharField(max_length=200)
    direccion = models.CharField(max_length=50, null=True)
    telefono = models.CharField(max_length=50, null=True)
    correo = models.EmailField(max_length = 255)
    identificacion = models.ForeignKey(CtnIdentificacion, on_delete=models.PROTECT)
    ciudad = models.ForeignKey(CtnCiudad, on_delete=models.PROTECT)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    class Meta:
        db_table = "cnt_informacion_facturacion"

class CtnDireccion(models.Model):
    fecha = models.DateTimeField()
    direccion = models.CharField(max_length=150)
    direccion_formato = models.CharField(max_length=150)
    latitud = models.DecimalField(max_digits=20, decimal_places=12, null=True)
    longitud = models.DecimalField(max_digits=20, decimal_places=12, null=True)
    ciudad = models.ForeignKey(CtnCiudad, on_delete=models.PROTECT, null=True)
    class Meta:
        db_table = "cnt_direccion"        