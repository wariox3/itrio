from rest_framework import serializers
from contabilidad.models.cuenta_clase import ConCuentaClase

class ConCuentaClaseSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConCuentaClase
        fields = ['id', 'nombre']

class ConCuentaClaseListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConCuentaClase

    def to_representation(self, instance):
        return {
            'cuenta_clase_id': instance.id,
            'cuenta_clase_nombre': instance.nombre
        }        
        