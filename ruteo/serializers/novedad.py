from rest_framework import serializers
from ruteo.models.visita import RutVisita
from ruteo.models.novedad_tipo import RutNovedadTipo
from ruteo.models.novedad import RutNovedad

class RutNovedadSerializador(serializers.HyperlinkedModelSerializer):            
    visita = serializers.PrimaryKeyRelatedField(queryset=RutVisita.objects.all())    
    novedad_tipo = serializers.PrimaryKeyRelatedField(queryset=RutNovedadTipo.objects.all())
    
    class Meta:
        model = RutNovedad
        fields = ['id', 'fecha', 'fecha_solucion', 'descripcion', 'solucion', 'estado_solucion', 'visita', 'novedad_tipo']

    def to_representation(self, instance):      
        novedad_tipo_nombre = ''
        if instance.novedad_tipo:
            novedad_tipo_nombre = instance.novedad_tipo.nombre   
        return {
            'id': instance.id,  
            'fecha': instance.fecha,
            'fecha_solucion': instance.fecha_solucion,
            'descripcion': instance.descripcion,
            'solucion': instance.solucion,
            'estado_solucion': instance.estado_solucion,
            'nuevo_complemento': instance.nuevo_complemento,
            'novedad_tipo_nombre': novedad_tipo_nombre            
        }  
    
