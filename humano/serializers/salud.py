from rest_framework import serializers
from humano.models.salud import HumSalud
from humano.models.concepto import HumConcepto

class HumSaludSeleccionarSerializador(serializers.ModelSerializer):
    class Meta:
        model = HumSalud
        fields = ['id', 'nombre']
class HumSaludSerializador(serializers.HyperlinkedModelSerializer):
    concepto = serializers.PrimaryKeyRelatedField(queryset=HumConcepto.objects.all(), default=None, allow_null=True)
    class Meta:
        model = HumSalud
        fields = ['id', 'nombre', 'concepto']

    def to_representation(self, instance):
        concepto_nombre = ''
        if instance.concepto:
            concepto_nombre = instance.concepto.nombre
        return {
            'salud_id': instance.id,
            'salud_nombre': instance.nombre,
            'salud_concepto_id': instance.concepto_id,
            'salud_concepto_nombre': concepto_nombre
        } 
    

class HumSaludListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumSalud

    def to_representation(self, instance):
        return {
            'salud_id': instance.id,
            'salud_nombre': instance.nombre,
        }         
        