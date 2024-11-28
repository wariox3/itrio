from rest_framework import serializers
from ruteo.models.despacho import RutDespacho


class RutDespachoSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = RutDespacho
        fields = ['id', 'peso', 'volumen', 'visitas', 'vehiculo', 'estado_aprobado']

    def to_representation(self, instance):      
        vehiculo_placa = ""
        if instance.vehiculo:
            vehiculo_placa = instance.vehiculo.placa
        return {
            'id': instance.id,  
            'fecha': instance.fecha,
            'peso': instance.peso,
            'volumen': instance.volumen,
            'visitas': instance.visitas,
            'vehiculo_id': instance.vehiculo_id,
            'vehiculo_placa': vehiculo_placa,
            'estado_aprobado': instance.estado_aprobado
        }
    
