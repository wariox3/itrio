from django.db import models
from general.models.contacto import GenContacto
from general.models.ciudad import GenCiudad
from transporte.models.operacion import TteOperacion
from transporte.models.despacho import TteDespacho
from transporte.models.servicio import TteServicio
from transporte.models.producto import TteProducto
from transporte.models.empaque import TteEmpaque
from transporte.models.ruta import TteRuta
from transporte.models.zona import TteZona

class TteGuia(models.Model):
    fecha = models.DateField()
    fecha_registro = models.DateTimeField(auto_now_add=True, null=True)
    fecha_recogida = models.DateTimeField(null=True)
    fecha_ingreso = models.DateTimeField(null=True)
    fecha_despacho = models.DateTimeField(null=True)
    fecha_entrega = models.DateTimeField(null=True)
    fecha_soporte = models.DateTimeField(null=True)
    documento = models.CharField(max_length=30, null=True)
    numero_rndc = models.IntegerField(null=True)
    remitente_nombre = models.CharField(max_length=150)
    destinatario_nombre = models.CharField(max_length=150)
    destinatario_direccion = models.CharField(max_length=150)
    destinatario_telefono = models.CharField(max_length=50, null=True)
    destinatario_correo = models.CharField(max_length=255, null=True)
    unidades = models.FloatField(default=0)
    peso = models.FloatField(default=0)
    volumen = models.FloatField(default=0)
    peso_facturado = models.FloatField(default=0)
    declara = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    flete = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    manejo = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    recaudo = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    cobro_entrega = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    estado_recogido = models.BooleanField(default = False)
    estado_ingreso = models.BooleanField(default = False)
    estado_embarcado = models.BooleanField(default = False)
    estado_despachado = models.BooleanField(default = False)
    estado_entregado = models.BooleanField(default = False)
    estado_soporte = models.BooleanField(default = False)
    estado_novedad = models.BooleanField(default = False)
    estado_novedad_solucionada = models.BooleanField(default = False)
    estado_rndc = models.BooleanField(default = False)
    contenido_verificado = models.BooleanField(default = False)
    mercancia_peligrosa = models.BooleanField(default = False)
    requiere_cita = models.BooleanField(default = False)
    liquidacion = models.CharField(max_length=1)
    comentario = models.CharField(max_length=500, null=True)
    contacto = models.ForeignKey(GenContacto, on_delete=models.PROTECT, related_name='guias_contacto_rel')
    cliente = models.ForeignKey(GenContacto, on_delete=models.PROTECT, related_name='guias_cliente_rel')
    destinatario = models.ForeignKey(GenContacto, on_delete=models.PROTECT, related_name='guias_destinatario_rel')
    operacion_ingeso = models.ForeignKey(TteOperacion, on_delete=models.PROTECT, related_name='guias_operacion_ingreso_rel')
    operacion_cargo = models.ForeignKey(TteOperacion, on_delete=models.PROTECT, related_name='guias_operacion_cargo_rel')
    ciudad_origen = models.ForeignKey(GenCiudad, on_delete=models.PROTECT, related_name='guias_ciudad_origen_rel')
    ciudad_destino = models.ForeignKey(GenCiudad, on_delete=models.PROTECT, related_name='guias_ciudad_destino_rel')
    despacho = models.ForeignKey(TteDespacho, null=True, on_delete=models.PROTECT, related_name='guias_despacho_rel')
    servicio = models.ForeignKey(TteServicio, on_delete=models.PROTECT, related_name='guias_servicio_rel')
    producto = models.ForeignKey(TteProducto, on_delete=models.PROTECT, related_name='guias_producto_rel')
    empaque = models.ForeignKey(TteEmpaque, on_delete=models.PROTECT, related_name='guias_empaque_rel')
    ruta = models.ForeignKey(TteRuta, null=True, on_delete=models.PROTECT, related_name='guias_ruta_rel')
    zona = models.ForeignKey(TteZona, null=True, on_delete=models.PROTECT, related_name='guias_zona_rel')

    class Meta:
        db_table = "tte_guia"