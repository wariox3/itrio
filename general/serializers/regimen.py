from general.models.regimen import GenRegimen
from rest_framework import serializers

class GenRegimenSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenRegimen
        fields = [
            'id', 
            'nombre'
            ]  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
        }        

class GenRegimenListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = GenRegimen

    def to_representation(self, instance):
        return {
            'regimen_id': instance.id,            
            'regimen_nombre': instance.nombre,
        }       