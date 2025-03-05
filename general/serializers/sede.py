from general.models.sede import GenSede
from rest_framework import serializers
from contabilidad.models.grupo import ConGrupo

class GenSedeSerializador(serializers.HyperlinkedModelSerializer):
    grupo = serializers.PrimaryKeyRelatedField(queryset=ConGrupo.objects.all(), default=None, allow_null=True)
    class Meta:
        model = GenSede
        fields = ['id', 'nombre', 'grupo']  
        
    def to_representation(self, instance):
        grupo_nombre = ""
        if instance.grupo:
            grupo_nombre = instance.grupo.nombre

        return {
            'id': instance.id,
            'nombre': instance.nombre,
            'grupo_id': instance.grupo_id,
            'grupo_nombre': grupo_nombre    
        }     

class GenSedeListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenSede
        
    def to_representation(self, instance):
        return {
            'sede_id': instance.id,            
            'sede_nombre': instance.nombre
        }       