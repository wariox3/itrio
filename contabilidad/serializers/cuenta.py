from rest_framework import serializers
from contabilidad.models.cuenta import ConCuenta
from contabilidad.models.cuenta_clase import ConCuentaClase

class ConCuentaSerializador(serializers.HyperlinkedModelSerializer):
    cuenta_clase = serializers.PrimaryKeyRelatedField(queryset=ConCuentaClase.objects.all(), allow_null=True)
    class Meta:
        model = ConCuenta
        fields = ['id', 'codigo', 'nombre', 'exige_base', 'exige_tercero', 'exige_grupo', 'permite_movimiento', 'cuenta_clase']

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'codigo': instance.codigo,
            'nombre': instance.nombre,
            'exige_base': instance.exige_base,
            'exige_tercero': instance.exige_tercero,
            'exige_grupo': instance.exige_grupo,
            'permite_movimiento': instance.permite_movimiento            
        } 


class ConCuentaListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConCuenta

    def to_representation(self, instance):
        return {
            'cuenta_id': instance.id,
            'cuenta_nombre': instance.nombre,
            'cuenta_codigo': instance.codigo
        }         
        