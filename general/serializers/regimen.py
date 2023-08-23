from general.models.regimen import Regimen
from rest_framework import serializers

class RegimenSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Regimen
        fields = [
            'id', 
            'nombre'
            ]  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
        }        