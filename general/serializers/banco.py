from general.models.banco import GenBanco
from rest_framework import serializers

class GenBancoSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenBanco
        fields = ['id', 'nombre', 'codigo']
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'codigo': instance.codigo
        }
     
class GenBancoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenBanco
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'codigo': instance.codigo
        }

class GenBancoListaBuscarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenBanco    
    def to_representation(self, instance):
        return {
            'id': instance.id,                        
            'nombre': instance.nombre
        }    