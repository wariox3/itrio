from general.models.respuesta_electronica import RespuestaElectronica
from rest_framework import serializers

class RespuestaElectronicaSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RespuestaElectronica
        fields = [
            'codigo_estatus',
            'proceso_dian',
            'mensaje_error',
            'razon_error',
            'codigo_modelo',
            'fecha'
            ]  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'codigo_estatus': instance.codigo_status,
            'proceso_dian': instance.proceso_dian,
            'mensaje_error': instance.mensaje_error,
            'razon_error': instance.razon_error,
            'codigo_modelo': instance.codigo_modelo,
            'fecha': instance.fecha,
        }        

   