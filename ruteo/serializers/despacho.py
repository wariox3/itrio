from rest_framework import serializers
from ruteo.models.despacho import RutDespacho


class RutDespachoSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = RutDespacho
        fields = ['id', 'peso', 'volumen', 'tiempo', 'visitas', 'visitas_entregadas', 'vehiculo', 'estado_aprobado', 'estado_terminado']

    def to_representation(self, instance):      
        vehiculo_placa = ""
        if instance.vehiculo:
            vehiculo_placa = instance.vehiculo.placa
        return {
            'id': instance.id,  
            'fecha': instance.fecha,
            'peso': instance.peso,
            'volumen': instance.volumen,
            'tiempo': instance.tiempo,
            'visitas': instance.visitas,
            'visitas_entregadas': instance.visitas_entregadas,
            'vehiculo_id': instance.vehiculo_id,
            'vehiculo_placa': vehiculo_placa,
            'estado_aprobado': instance.estado_aprobado,
            'estado_terminado': instance.estado_terminado
        }
    
