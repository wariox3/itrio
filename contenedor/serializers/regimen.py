from contenedor.models import ContenedorRegimen
from rest_framework import serializers

class ContenedorRegimenSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ContenedorRegimen
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
        model = ContenedorRegimen

    def to_representation(self, instance):
        return {
            'regimen_id': instance.id,            
            'regimen_nombre': instance.nombre,
        }     