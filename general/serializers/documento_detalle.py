from general.models.documento_detalle import GenDocumentoDetalle
from general.models.documento import GenDocumento
from general.models.item import GenItem
from general.models.contacto import GenContacto
from contabilidad.models.cuenta import ConCuenta
from humano.models.concepto import HumConcepto
from humano.models.credito import HumCredito
from rest_framework import serializers

class GenDocumentoDetalleSerializador(serializers.HyperlinkedModelSerializer):
    documento = serializers.PrimaryKeyRelatedField(queryset=GenDocumento.objects.all())
    item = serializers.PrimaryKeyRelatedField(queryset=GenItem.objects.all(), default=None, allow_null=True)
    documento_afectado = serializers.PrimaryKeyRelatedField(queryset=GenDocumento.objects.all(), default=None, allow_null=True)
    cuenta = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all(), default=None, allow_null=True)
    contacto = serializers.PrimaryKeyRelatedField(queryset=GenContacto.objects.all(), default=None, allow_null=True)
    concepto = serializers.PrimaryKeyRelatedField(queryset=HumConcepto.objects.all(), default=None, allow_null=True)
    credito = serializers.PrimaryKeyRelatedField(queryset=HumCredito.objects.all(), default=None, allow_null=True)

    class Meta:
        model = GenDocumentoDetalle
        fields = ['tipo_registro', 'documento', 'documento_afectado', 'item', 'cuenta', 'contacto', 'cantidad', 'precio', 'pago', 'porcentaje_descuento', 
                  'porcentaje', 'descuento', 'subtotal', 'total_bruto', 'total', 'base_impuesto', 'hora', 'naturaleza', 
                  'impuesto', 'impuesto_retencion', 'impuesto_operado', 
                  'detalle', 'numero', 'concepto', 'credito', 'base_cotizacion', 'base_prestacion', 'operacion', 'pago_operado', 
                  'devengado', 'deduccion', 'dias']

    def to_representation(self, instance):
        item = instance.item
        item_nombre = ""
        if item is not None:
            item_nombre = item.nombre
        documento_afectado_numero = ""
        documento_afectado_contacto_nombre_corto = ""
        documento_afectado = instance.documento_afectado    
        if documento_afectado is not None:
            documento_afectado_numero = documento_afectado.numero    
            contacto = documento_afectado.contacto
            if contacto is not None:
                documento_afectado_contacto_nombre_corto = contacto.nombre_corto
        cuenta_codigo = ""
        cuenta = instance.cuenta
        if cuenta:
            cuenta_codigo = cuenta.codigo
        contacto_nombre_corto = ''
        if instance.contacto:
            contacto_nombre_corto = instance.contacto.nombre_corto
        concepto_nombre = ''
        if instance.concepto:
            concepto_nombre = instance.concepto.nombre
        return {
            'id': instance.id,            
            'documento_id': instance.documento_id,        
            'tipo_registro': instance.tipo_registro,
            'item': instance.item_id,
            'item_nombre': item_nombre,
            'cuenta': instance.cuenta_id,
            'cuenta_codigo': cuenta_codigo,           
            'cantidad': instance.cantidad,
            'precio': instance.precio,
            'pago': instance.pago,
            'pago_operado': instance.pago_operado,
            'porcentaje': instance.porcentaje,
            'porcentaje_descuento': instance.porcentaje_descuento,
            'descuento' :  instance.descuento,
            'subtotal' : instance.subtotal,
            'total_bruto' : instance.total_bruto,
            'base_impuesto' : instance.base_impuesto,
            'impuesto' : instance.impuesto,
            'impuesto_retencion' : instance.impuesto_retencion,
            'impuesto_operado' : instance.impuesto_operado,
            'total' : instance.total,
            'hora' : instance.hora,
            'dias' : instance.dias,
            'devengado': instance.devengado,
            'deduccion': instance.deduccion,
            'operacion': instance.operacion,
            'base_cotizacion': instance.base_cotizacion,
            'base_prestacion': instance.base_prestacion,
            'documento_afectado_id': instance.documento_afectado_id,
            'documento_afectado_numero': documento_afectado_numero,
            'documento_afectado_contacto_nombre_corto':documento_afectado_contacto_nombre_corto,
            'contacto_id': instance.contacto_id,
            'contacto_nombre_corto': contacto_nombre_corto,
            'naturaleza':instance.naturaleza,
            'detalle': instance.detalle,
            'numero': instance.numero,
            'concepto_id': instance.concepto_id,
            'concepto_nombre': concepto_nombre,
            'credito_id': instance.credito_id
        }  

class GenDocumentoDetalleInformeSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenDocumentoDetalle        

    def to_representation(self, instance):
        item = instance.item
        item_nombre = ""
        if item is not None:
            item_nombre = item.nombre
        documento = instance.documento
        documento_tipo_nombre = ""
        documento_contacto_nombre = ""
        if documento is not None:
            documento_tipo = documento.documento_tipo
            if documento_tipo is not None:
                documento_tipo_nombre = documento_tipo.nombre
            contacto = documento.contacto
            if contacto is not None:
                documento_contacto_nombre = contacto.nombre_corto
        return {
            'id': instance.id,            
            'documento_id': instance.documento_id,
            'documento_tipo_nombre': documento_tipo_nombre,        
            'documento_fecha': documento.fecha,
            'documento_numero': documento.numero,    
            'documento_contacto_nombre': documento_contacto_nombre,
            'item_id': instance.item_id,
            'item_nombre': item_nombre,
            'cuenta_id': instance.cuenta_id,
            'cantidad': instance.cantidad,
            'precio': instance.precio,
            'pago': instance.pago,
            'porcentaje_descuento': instance.porcentaje_descuento,
            'descuento' :  instance.descuento,
            'subtotal' : instance.subtotal,
            'total_bruto' : instance.total_bruto,
            'base_impuesto' : instance.base_impuesto,
            'impuesto' : instance.impuesto,
            'total' : instance.total,
            'documento_afectado_id': instance.documento_afectado_id
        }           
    
class GenDocumentoDetalleExcelSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenDocumentoDetalle        

    def to_representation(self, instance):
        item = instance.item
        item_nombre = ""
        if item is not None:
            item_nombre = item.nombre
        documento = instance.documento
        documento_tipo_nombre = ""
        documento_contacto_nombre = ""
        documento_contacto_numero_identificacion = ""
        if documento is not None:
            documento_tipo = documento.documento_tipo
            if documento_tipo is not None:
                documento_tipo_nombre = documento_tipo.nombre
            contacto = documento.contacto
            if contacto is not None:
                documento_contacto_nombre = contacto.nombre_corto 
                documento_contacto_numero_identificacion = contacto.numero_identificacion 
        documento_afectado_numero = ""
        documento_afectado = instance.documento_afectado
        if documento_afectado is not None:
            documento_afectado_numero = documento_afectado.numero
        return {
            'id': instance.id,            
            'documento_id': instance.documento_id,
            'documento_tipo_nombre': documento_tipo_nombre,        
            'documento_fecha': documento.fecha,
            'documento_numero': documento.numero, 
            'documento_contacto_numero_identificacion': documento_contacto_numero_identificacion,  
            'documento_contacto_nombre': documento_contacto_nombre,  
            'item_id': instance.item_id,
            'item_nombre': item_nombre,
            'cuenta_id': instance.cuenta_id,
            'cantidad': instance.cantidad,
            'precio': instance.precio,
            'pago': instance.pago,
            'porcentaje_descuento': instance.porcentaje_descuento,
            'descuento' :  instance.descuento,
            'subtotal' : instance.subtotal,
            'total_bruto' : instance.total_bruto,
            'base_impuesto' : instance.base_impuesto,
            'impuesto' : instance.impuesto,
            'total' : instance.total,
            'documento_afectado_id': instance.documento_afectado_id,
            'documento_afectado_numero': documento_afectado_numero
        }      
    
class GenDocumentoDetalleNominaSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenDocumentoDetalle        

    def to_representation(self, instance):
        documento_contacto_nombre = ""
        documento_contacto_numero_identificacion = ""
        if instance.documento.contacto:
            documento_contacto_nombre = instance.documento.contacto.nombre_corto
            documento_contacto_numero_identificacion = instance.documento.contacto.numero_identificacion
        concepto_nombre = ""
        if instance.concepto:
            concepto_nombre = instance.concepto.nombre
            
        return {
            'id': instance.id,            
            'documento_id': instance.documento_id,
            'documento_tipo_nombre': instance.documento.documento_tipo.nombre,        
            'documento_fecha': instance.documento.fecha,
            'documento_numero': instance.documento.numero,    
            'documento_contacto_id': instance.documento.contacto_id,
            'documento_contacto_numero_identificacion': documento_contacto_numero_identificacion,
            'documento_contacto_nombre': documento_contacto_nombre,
            'documento_contrato_id': instance.documento.contrato_id,
            'documento_fecha_hasta': instance.documento.fecha_hasta,
            'concepto_id': instance.concepto_id,
            'concepto_nombre': concepto_nombre,
            'detalle':instance.detalle,
            'porcentaje': instance.porcentaje,
            'cantidad': instance.cantidad,
            'dias': instance.dias,
            'hora': instance.hora,
            'operacion': instance.operacion,
            'pago': instance.pago,
            'pago_operado': instance.pago_operado,
            'devengado': instance.devengado,
            'deduccion': instance.deduccion,
            'base_cotizacion': instance.base_cotizacion,
            'base_prestacion': instance.base_prestacion,
            'base_impuesto': instance.base_impuesto
        } 

class GenDocumentoDetalleNominaExcelSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenDocumentoDetalle        

    def to_representation(self, instance):
        documento_contacto_nombre = ""
        documento_contacto_numero_identificacion = ""
        if instance.documento.contacto:
            documento_contacto_nombre = instance.documento.contacto.nombre_corto
            documento_contacto_numero_identificacion = instance.documento.contacto.numero_identificacion
        concepto_nombre = ""
        if instance.concepto:
            concepto_nombre = instance.concepto.nombre
            
        return {
            'ID': instance.id,            
            'DOC_ID': instance.documento_id,
            'DOCUMENTO': instance.documento.documento_tipo.nombre,    
            'NUMERO': instance.documento.numero,            
            'DESDE': instance.documento.fecha,            
            'HASTA': instance.documento.fecha_hasta,
            'EMP_ID': instance.documento.contacto_id,
            'IDENTIFICACION': documento_contacto_numero_identificacion,
            'EMPLEADO': documento_contacto_nombre,
            'CONT': instance.documento.contrato_id,        
            'CON_ID': instance.concepto_id,
            'CONCEPTO': concepto_nombre,
            'DETALLE':instance.detalle,
            'POR': instance.porcentaje,            
            'DIAS': instance.dias,
            'HORAS': instance.cantidad,
            'HORA': instance.hora,
            'OP': instance.operacion,
            'PAGO': instance.pago,
            'PAGO_OPE': instance.pago_operado,
            'DEVENGADO': instance.devengado,
            'DEDUCCION': instance.deduccion,
            'IBC': instance.base_cotizacion,
            'IBP': instance.base_prestacion,
            'BASE': instance.base_impuesto
        }     