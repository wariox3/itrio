from rest_framework import serializers
from general.models.documento_tipo import GenDocumentoTipo
from general.models.resolucion import GenResolucion
from contabilidad.models.cuenta import ConCuenta

class GenDocumentoTipoAutocompletarSerializador(serializers.ModelSerializer):          
    class Meta:
        model = GenDocumentoTipo
        fields = ['id', 
                  'nombre']

#deprecated
class GenDocumentoTipoSerializador(serializers.HyperlinkedModelSerializer):
    resolucion = serializers.PrimaryKeyRelatedField(queryset=GenResolucion.objects.all(), allow_null=True)
    cuenta_cobrar = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all(), default=None, allow_null=True)
    cuenta_pagar = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all(), default=None, allow_null=True)

    class Meta:
        model = GenDocumentoTipo
        fields = ['consecutivo', 'resolucion', 'cuenta_pagar', 'cuenta_cobrar']

    def to_representation(self, instance):  
        cuenta_cobrar_codigo = ""
        cuenta_cobrar_nombre = ""
        if instance.cuenta_cobrar:
            cuenta_cobrar_codigo = instance.cuenta_cobrar.codigo
            cuenta_cobrar_nombre = instance.cuenta_cobrar.nombre
        cuenta_pagar_codigo = ""
        cuenta_pagar_nombre = ""
        if instance.cuenta_pagar:
            cuenta_pagar_codigo = instance.cuenta_pagar.codigo
            cuenta_pagar_nombre = instance.cuenta_pagar.nombre            
        resolucion_numero = ""
        resolucion_prefijo = ""
        if instance.resolucion:
            resolucion_numero = instance.resolucion.numero
            resolucion_prefijo = instance.resolucion.prefijo
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'consecutivo' : instance.consecutivo,
            'resolucion_id' : instance.resolucion_id,
            'resolucion_numero' : resolucion_numero,
            'resolucion_prefijo' : resolucion_prefijo,
            'venta' : instance.venta,
            'compra' : instance.compra,
            'operacion': instance.operacion,
            'cuenta_cobrar_id': instance.cuenta_cobrar_id,
            'cuenta_cobrar_codigo': cuenta_cobrar_codigo,
            'cuenta_cobrar_nombre' : cuenta_cobrar_nombre,
            'cuenta_pagar_id': instance.cuenta_pagar_id,
            'cuenta_pagar_codigo': cuenta_pagar_codigo,
            'cuenta_pagar_nombre' : cuenta_pagar_nombre
            
        } 

class GenDocumentoTipoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenDocumentoTipo 
        
    def to_representation(self, instance):
        return {
            'documento_tipo_id': instance.id,            
            'documento_tipo_nombre': instance.nombre
        }            
