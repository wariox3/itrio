from general.models.asesor import Asesor
from rest_framework import serializers

class AsesorSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Asesor
        fields = [
            'id',
            'nombre_corto', 
            'celular',
            'correo',
            ]  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'nombre_corto': instance.nombre_corto,
            'celular': instance.celular,
            'correo': instance.correo,    
        }     

class AsesorListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Asesor 
        
    def to_representation(self, instance):
        return {
            'asesor_id': instance.id,            
            'asesor_nombre': instance.nombre_corto
        }       