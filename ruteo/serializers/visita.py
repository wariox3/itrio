from rest_framework import serializers
from ruteo.models.visita import RutVisita


class RutVisitaSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = RutVisita
        fields = ['id', 'guia', 'fecha', 'documento', 'destinatario', 'destinatario_direccion', 'ciudad', 'estado', 'pais', 'destinatario_telefono', 'destinatario_correo', 'peso', 'volumen', 'latitud', 'longitud', 'decodificado', 'orden', 'distancia_proxima']

    def to_representation(self, instance):        
        return {
            'id': instance.id,  
            'guia': instance.guia,
            'fecha': instance.fecha,
            'documento': instance.documento,
            'destinatario': instance.destinatario,
            'destinatario_direccion': instance.destinatario_direccion,
            'ciudad': instance.ciudad,
            'estado': instance.estado,
            'pais': instance.pais,
            'destinatario_telefono': instance.destinatario_telefono,
            'destinatario_correo': instance.destinatario_correo,
            'peso': instance.peso,
            'volumen': instance.volumen,
            'decodificado': instance.decodificado,
            'decodificado_error': instance.decodificado_error,
            'latitud': instance.latitud,
            'longitud': instance.longitud,
            'orden': instance.orden,
            'distancia_proxima': instance.distancia_proxima
        }
    
