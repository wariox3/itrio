from rest_framework import serializers
from ruteo.models.rut_visita import RutVisita


class RutVisitaSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = RutVisita
        fields = ['id', 'guia', 'fecha', 'documento', 'destinatario', 'destinatario_direccion', 'destinatario_telefono', 'destinatario_correo', 'peso', 'volumen', 'latitud', 'longitud', 'decodificado']

    def to_representation(self, instance):        
        return {
            'id': instance.id,  
            'guia': instance.guia,
            'fecha': instance.fecha,
            'documento': instance.documento,
            'destinatario': instance.destinatario,
            'destinatario_direccion': instance.destinatario_direccion,
            'destinatario_telefono': instance.destinatario_telefono,
            'destinatario_correo': instance.destinatario_correo,
            'peso': instance.peso,
            'volumen': instance.volumen,
            'decodificado': instance.decodificado,
            'decodificado_error': instance.decodificado_error,
            'latitud': instance.latitud,
            'longitud': instance.longitud
        }
    
