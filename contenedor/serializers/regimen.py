from contenedor.models import CtnRegimen
from rest_framework import serializers

class ContenedorRegimenSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CtnRegimen
        fields = [
            'id', 
            'nombre'
            ]  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
        }        

class ContenedorRegimenListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = CtnRegimen

    def to_representation(self, instance):
        return {
            'regimen_id': instance.id,            
            'regimen_nombre': instance.nombre,
        }     