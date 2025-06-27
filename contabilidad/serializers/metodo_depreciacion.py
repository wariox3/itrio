from rest_framework import serializers
from contabilidad.models.metodo_depreciacion import ConMetodoDepreciacion

class ConMetodoDepreciacionSeleccionarSerializador(serializers.ModelSerializer):
    class Meta:
        model = ConMetodoDepreciacion
        fields = ['id', 'nombre']
class ConMetodoDepreciacionSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConMetodoDepreciacion
        fields = '__all__'

class ConMetodoDepreciacionListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConMetodoDepreciacion

    def to_representation(self, instance):
        return {
            'metodo_depreciacion_id': instance.id,
            'metodo_depreciacion_nombre': instance.nombre
        }        
        