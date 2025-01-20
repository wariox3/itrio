from rest_framework import serializers
from general.models.documento_tipo import GenDocumentoTipo
from general.models.resolucion import GenResolucion

class GenDocumentoTipoSerializador(serializers.HyperlinkedModelSerializer):
    resolucion = serializers.PrimaryKeyRelatedField(queryset=GenResolucion.objects.all(), allow_null=True)
    class Meta:
        model = GenDocumentoTipo
        fields = ['consecutivo', 'resolucion']

    def to_representation(self, instance):  
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
            'operacion': instance.operacion            
        }        
        