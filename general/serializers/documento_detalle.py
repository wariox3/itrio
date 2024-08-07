from general.models.documento_detalle import GenDocumentoDetalle
from general.models.documento import GenDocumento
from general.models.item import GenItem
from general.models.contacto import GenContacto
from contabilidad.models.cuenta import ConCuenta
from rest_framework import serializers

class GenDocumentoDetalleSerializador(serializers.HyperlinkedModelSerializer):
    documento = serializers.PrimaryKeyRelatedField(queryset=GenDocumento.objects.all())
    item = serializers.PrimaryKeyRelatedField(queryset=GenItem.objects.all(), default=None, allow_null=True)
    documento_afectado = serializers.PrimaryKeyRelatedField(queryset=GenDocumento.objects.all(), default=None, allow_null=True)
    cuenta = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all(), default=None, allow_null=True)
    contacto = serializers.PrimaryKeyRelatedField(queryset=GenContacto.objects.all(), default=None, allow_null=True)
    class Meta:
        model = GenDocumentoDetalle
        fields = ['documento', 'documento_afectado', 'item', 'cuenta', 'contacto', 'cantidad', 'precio', 'pago', 'porcentaje_descuento', 'descuento', 'subtotal', 'total_bruto', 'total', 'base_impuesto', 'naturaleza', 'impuesto', 'detalle', 'numero']

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
        return {
            'id': instance.id,            
            'documento_id': instance.documento_id,        
            'item': instance.item_id,
            'item_nombre': item_nombre,
            'cuenta': instance.cuenta_id,
            'cuenta_codigo': cuenta_codigo,           
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
            'documento_afectado_numero': documento_afectado_numero,
            'documento_afectado_contacto_nombre_corto':documento_afectado_contacto_nombre_corto,
            'contacto_id': instance.contacto_id,
            'contacto_nombre_corto': contacto_nombre_corto,
            'naturaleza':instance.naturaleza,
            'detalle': instance.detalle,
            'numero': instance.numero
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