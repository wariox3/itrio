from general.models.gen_asesor import GenAsesor
from rest_framework import serializers

class GenAsesorSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenAsesor
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

class GenAsesorListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenAsesor 
        
    def to_representation(self, instance):
        return {
            'asesor_id': instance.id,            
            'asesor_nombre_corto': instance.nombre_corto
        }       