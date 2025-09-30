from general.models.documento_detalle import GenDocumentoDetalle
from general.models.documento import GenDocumento
from general.models.item import GenItem
from general.models.contacto import GenContacto
from contabilidad.models.cuenta import ConCuenta
from contabilidad.models.grupo import ConGrupo
from contabilidad.models.activo import ConActivo
from humano.models.concepto import HumConcepto
from humano.models.credito import HumCredito
from humano.models.novedad import HumNovedad
from humano.models.contrato import HumContrato
from inventario.models.almacen import InvAlmacen

from rest_framework import serializers

class GenDocumentoDetalleAgregarDocumentoSerializador(serializers.ModelSerializer):
    item__nombre = serializers.CharField(source='item.nombre', read_only=True)
    grupo__nombre = serializers.CharField(source='grupo.nombre', read_only=True)
    almacen__nombre = serializers.CharField(source='almacen.nombre', read_only=True)
    documento__numero = serializers.IntegerField(source='documento.numero', read_only=True)
    documento__contacto__nombre_corto = serializers.CharField(source='documento.contacto.nombre_corto', read_only=True)
    documento__contacto__numero_identificacion = serializers.CharField(source='documento.contacto.numero_identificacion', read_only=True)
    documento__documento__tipo__nombre = serializers.CharField(source='documento.documento_tipo.nombre', read_only=True)
    class Meta:
        model = GenDocumentoDetalle
        fields = ['id', 'item', 'item__nombre', 'grupo',  'grupo__nombre', 'almacen', 'almacen__nombre',
                  'cantidad', 'precio', 'documento__numero' ,'documento__documento__tipo__nombre', 'documento__contacto__nombre_corto',
                  'documento__contacto__numero_identificacion']   
        select_related_fields = ['item','grupo', 'almacen', 'documento', 'documento_tipo', 'contacto']     

class GenDocumentoDetalleNominaSerializador(serializers.ModelSerializer):
    documento__contacto__nombre_corto = serializers.CharField(source='documento.contacto.nombre_corto', read_only=True)
    documento__contacto__numero_identificacion = serializers.CharField(source='documento.contacto.numero_identificacion', read_only=True)
    documento__documento_tipo__nombre = serializers.CharField(source='documento.documento_tipo.nombre', read_only=True)
    documento__fecha = serializers.DateField(source='documento.fecha', read_only=True)
    documento__fecha_desde = serializers.DateField(source='documento.fecha_desde', read_only=True)
    documento__fecha_hasta = serializers.DateField(source='documento.fecha_hasta', read_only=True)
    documento__numero = serializers.IntegerField(source='documento.numero', read_only=True)
    documento__contacto = serializers.IntegerField(source='documento.contacto_id', read_only=True)
    documento__contrato = serializers.IntegerField(source='documento.contrato_id', read_only=True)
    concepto__nombre = serializers.CharField(source='concepto.nombre', read_only=True)
    class Meta:
        model = GenDocumentoDetalle
        fields = [
            'id', 
            'documento', 
            'documento__documento_tipo__nombre', 
            'documento__fecha', 
            'documento__fecha_desde',
            'documento__fecha_hasta',
            'documento__numero', 
            'documento__contacto',
            'documento__contacto__numero_identificacion', 
            'documento__contacto__nombre_corto', 
            'documento__contrato',
            'concepto', 
            'concepto__nombre', 
            'detalle', 
            'porcentaje', 
            'cantidad', 
            'dias', 
            'hora', 
            'operacion', 
            'pago_operado', 
            'devengado',
            'deduccion', 
            'total',
            'base_cotizacion', 
            'base_prestacion', 
            'base_impuesto'
        ]
        select_related_fields = ['documento__contacto', 'documento' , 'concepto', 'documento__documento_tipo']  

class GenDocumentoDetalleNominaExcelSerializador(serializers.ModelSerializer):
        documento__contacto__nombre_corto = serializers.CharField(source='documento.contacto.nombre_corto', read_only=True)
        documento__contacto__numero_identificacion = serializers.CharField(source='documento.contacto.numero_identificacion', read_only=True)
        documento__documento_tipo__nombre = serializers.CharField(source='documento.documento_tipo.nombre', read_only=True)
        documento__fecha = serializers.DateField(source='documento.fecha', read_only=True)
        documento__fecha_hasta = serializers.DateField(source='documento.fecha_hasta', read_only=True)
        documento__contacto = serializers.IntegerField(source='documento.contacto_id', read_only=True)
        documento__contrato = serializers.IntegerField(source='documento.contrato_id', read_only=True)
        concepto__nombre = serializers.CharField(source='concepto.nombre', read_only=True)
        class Meta:
            model = GenDocumentoDetalle
            fields = [
                'id', 
                'documento', 
                'documento__documento_tipo__nombre', 
                'documento__fecha', 
                'documento__fecha_hasta',
                'documento__contacto',
                'documento__contacto__numero_identificacion', 
                'documento__contacto__nombre_corto', 
                'documento__contrato',
                'concepto', 
                'concepto__nombre', 
                'detalle', 
                'porcentaje', 
                'cantidad', 
                'dias', 
                'hora', 
                'operacion', 
                'pago_operado', 
                'devengado',
                'deduccion', 
                'base_cotizacion', 
                'base_prestacion', 
                'base_impuesto'
            ]
            select_related_fields = ['documento__contacto', 'documento' , 'concepto', 'documento__documento_tipo']          

class GenDocumentoDetalleListaDetalleCuentaSerializador(serializers.ModelSerializer):
    contacto__numero_identificacion = serializers.CharField(source='contacto.numero_identificacion', read_only=True, allow_null=True, default=None)
    contacto__nombre_corto = serializers.CharField(source='contacto.nombre_corto', read_only=True, allow_null=True, default=None)
    cuenta__codigo = serializers.CharField(source='cuenta.codigo', read_only=True, allow_null=True, default=None)
    grupo__nombre = serializers.CharField(source='grupo.nombre', read_only=True, allow_null=True, default=None)
    class Meta:
        model = GenDocumentoDetalle
        fields = [
                    'id', 
                    'naturaleza', 
                    'precio', 
                    'base', 
                    'total', 
                    'detalle',
                    'contacto__numero_identificacion',
                    'contacto__nombre_corto',
                    'cuenta__codigo',
                    'grupo__nombre'
                ]   
        select_related_fields = ['contacto','cuenta', 'grupo']

class GenDocumentoDetalleInformeVentaSerializador(serializers.ModelSerializer):          
    documento__numero = serializers.CharField(source='documento.numero', read_only=True)
    documento__fecha = serializers.CharField(source='documento.fecha', read_only=True)
    documento__documento_tipo__nombre = serializers.CharField(source='documento.documento_tipo.nombre', read_only=True)
    documento__contacto__nombre_corto = serializers.CharField(source='documento.contacto.nombre_corto', read_only=True)
    item__nombre = serializers.CharField(source='item.nombre', read_only=True)
    class Meta:
        model = GenDocumentoDetalle
        fields = ['id', 
                  'documento__documento_tipo__nombre',
                  'documento__numero',
                  'documento__fecha',
                  'documento__contacto__nombre_corto',
                  'item_id',
                  'item__nombre',
                  'cantidad',
                  'precio',
                  'subtotal',
                  'impuesto',
                  'total']
        select_related_fields = ['documento', 'item', 'documento__documento_tipo', 'documento__contacto']  

class GenDocumentoDetalleInformeInventarioSerializador(serializers.ModelSerializer):          
    documento__numero = serializers.CharField(source='documento.numero', read_only=True)
    documento__fecha = serializers.CharField(source='documento.fecha', read_only=True)
    documento__documento_tipo__nombre = serializers.CharField(source='documento.documento_tipo.nombre', read_only=True)
    documento__contacto__nombre_corto = serializers.CharField(source='documento.contacto.nombre_corto', read_only=True)
    item__nombre = serializers.CharField(source='item.nombre', read_only=True)
    class Meta:
        model = GenDocumentoDetalle
        fields = ['id', 'cantidad', 'cantidad_operada', 'costo', 'precio', 'subtotal', 'impuesto', 'total',
                    'documento',
                    'documento__numero',
                    'documento__fecha',                   
                    'documento__documento_tipo__nombre',
                    'documento__contacto__nombre_corto',
                    'item_id',
                    'item__nombre'
                ]
        select_related_fields = ['documento', 'item', 'documento__documento_tipo', 'documento__contacto']

class GenDocumentoDetalleCreditoPagoSerializador(serializers.ModelSerializer):  
    class Meta:
        model = GenDocumentoDetalle
        fields = ['id', 'pago']

#deprecated
class GenDocumentoDetalleSerializador(serializers.HyperlinkedModelSerializer):
    documento = serializers.PrimaryKeyRelatedField(queryset=GenDocumento.objects.all())
    item = serializers.PrimaryKeyRelatedField(queryset=GenItem.objects.all(), default=None, allow_null=True)
    documento_afectado = serializers.PrimaryKeyRelatedField(queryset=GenDocumento.objects.all(), default=None, allow_null=True)
    cuenta = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all(), default=None, allow_null=True)
    activo = serializers.PrimaryKeyRelatedField(queryset=ConActivo.objects.all(), default=None, allow_null=True)
    grupo = serializers.PrimaryKeyRelatedField(queryset=ConGrupo.objects.all(), default=None, allow_null=True)
    contacto = serializers.PrimaryKeyRelatedField(queryset=GenContacto.objects.all(), default=None, allow_null=True)
    concepto = serializers.PrimaryKeyRelatedField(queryset=HumConcepto.objects.all(), default=None, allow_null=True)
    credito = serializers.PrimaryKeyRelatedField(queryset=HumCredito.objects.all(), default=None, allow_null=True)
    novedad = serializers.PrimaryKeyRelatedField(queryset=HumNovedad.objects.all(), default=None, allow_null=True)
    contrato = serializers.PrimaryKeyRelatedField(queryset=HumContrato.objects.all(), default=None, allow_null=True)
    almacen = serializers.PrimaryKeyRelatedField(queryset=InvAlmacen.objects.all(), default=None, allow_null=True)

    class Meta:
        model = GenDocumentoDetalle
        fields = ['tipo_registro', 'cantidad', 'cantidad_operada', 'documento', 'documento_afectado', 'item', 'cuenta', 'activo', 'grupo', 'contacto', 'precio', 'pago', 'porcentaje_descuento', 
                  'porcentaje', 'descuento', 'subtotal', 'total_bruto', 'total', 'base', 'base_impuesto', 'hora', 'naturaleza', 
                  'impuesto', 'impuesto_retencion', 'impuesto_operado', 
                  'detalle', 'numero', 'concepto', 'credito', 'novedad', 'base_cotizacion', 'base_prestacion', 'base_prestacion_vacacion', 'operacion', 'operacion_inventario', 'pago_operado', 
                  'devengado', 'deduccion', 'dias', 'almacen', 'contrato']        

    def to_representation(self, instance):
        item = instance.item
        item_nombre = ""
        if item is not None:
            item_nombre = item.nombre
        documento_afectado_numero = ""
        documento_afectado_contacto_nombre_corto = ""
        documento_afectado_documento_tipo_nombre = ""        
        if instance.documento_afectado is not None:
            documento_afectado_numero = instance.documento_afectado.numero    
            if instance.documento_afectado.contacto is not None:
                documento_afectado_contacto_nombre_corto = instance.documento_afectado.contacto.nombre_corto
            if instance.documento_afectado.documento_tipo:
                documento_afectado_documento_tipo_nombre = instance.documento_afectado.documento_tipo.nombre
        cuenta_codigo = ""
        cuenta_nombre = ''
        if instance.cuenta:
            cuenta_codigo = instance.cuenta.codigo
            cuenta_nombre = instance.cuenta.nombre
        activo_codigo = ""
        activo_nombre = ''
        if instance.activo:
            activo_codigo = instance.activo.codigo
            activo_nombre = instance.activo.nombre
        grupo_nombre = ""
        if instance.grupo:
            grupo_nombre = instance.grupo.nombre
        contacto_nombre_corto = ''
        if instance.contacto:
            contacto_nombre_corto = instance.contacto.nombre_corto
        concepto_nombre = ''
        if instance.concepto:
            concepto_nombre = instance.concepto.nombre
        almacen_nombre = ""
        if instance.almacen:
            almacen_nombre = instance.almacen.nombre,
        documento_numero = ""
        documento_fecha = None
        if instance.documento:
            documento_numero = instance.documento.numero
            documento_fecha = instance.documento.fecha
        return {
            'id': instance.id,                                
            'tipo_registro': instance.tipo_registro,
            'item': instance.item_id,
            'item_nombre': item_nombre,
            'cuenta': instance.cuenta_id,
            'cuenta_codigo': cuenta_codigo,           
            'cuenta_nombre': cuenta_nombre,
            'cantidad': instance.cantidad,
            'cantidad_operada': instance.cantidad_operada,
            'precio': instance.precio,
            'pago': instance.pago,
            'pago_operado': instance.pago_operado,
            'porcentaje': instance.porcentaje,
            'porcentaje_descuento': instance.porcentaje_descuento,
            'descuento' :  instance.descuento,
            'subtotal' : instance.subtotal,
            'total_bruto' : instance.total_bruto,
            'base' : instance.base,
            'base_impuesto' : instance.base_impuesto,
            'impuesto' : instance.impuesto,
            'impuesto_retencion' : instance.impuesto_retencion,
            'impuesto_operado' : instance.impuesto_operado,
            'total' : instance.total,
            'pago': instance.pago,
            'hora' : instance.hora,
            'dias' : instance.dias,
            'devengado': instance.devengado,
            'deduccion': instance.deduccion,
            'operacion': instance.operacion,
            'operacion_inventario': instance.operacion_inventario,
            'base_cotizacion': instance.base_cotizacion,
            'base_prestacion': instance.base_prestacion,
            'base_prestacion_vacacion': instance.base_prestacion_vacacion,
            'documento_afectado_id': instance.documento_afectado_id,
            'documento_afectado_documento_tipo_nombre': documento_afectado_documento_tipo_nombre,
            'documento_afectado_numero': documento_afectado_numero,
            'documento_afectado_contacto_nombre_corto':documento_afectado_contacto_nombre_corto,
            'contacto_id': instance.contacto_id,
            'contacto_nombre_corto': contacto_nombre_corto,
            'naturaleza':instance.naturaleza,
            'detalle': instance.detalle,
            'numero': instance.numero,
            'concepto_id': instance.concepto_id,
            'concepto_nombre': concepto_nombre,
            'credito_id': instance.credito_id,
            'grupo_id': instance.grupo_id,
            'grupo_nombre': grupo_nombre,
            'almacen_id': instance.almacen_id,
            'almacen_nombre': almacen_nombre,
            'documento_id': instance.documento_id,
            'documento_numero': documento_numero,
            'documento_fecha': documento_fecha,
            'activo_id': instance.activo_id,
            'activo_codigo': activo_codigo,           
            'activo_nombre': activo_nombre
        }  
            
      
    
  

        