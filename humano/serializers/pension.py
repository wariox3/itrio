from rest_framework import serializers
from humano.models.pension import HumPension
from humano.models.concepto import HumConcepto

class HumPensionSeleccionarSerializador(serializers.ModelSerializer):
    class Meta:
        model = HumPension
        fields = ['id', 'nombre']

class HumPensionSerializador(serializers.HyperlinkedModelSerializer):    
    concepto = serializers.PrimaryKeyRelatedField(queryset=HumConcepto.objects.all(), default=None, allow_null=True)

    class Meta:
        model = HumPension
        fields = ['id', 'nombre', 'concepto']

    def to_representation(self, instance):
        concepto_nombre = ''
        if instance.concepto:
            concepto_nombre = instance.concepto.nombre
        return {
            'pension_id': instance.id,
            'pension_nombre': instance.nombre,
            'pension_concepto_id': instance.concepto_id,
            'pension_concepto_nombre': concepto_nombre
        } 
    

class HumPensionListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = HumPension

    def to_representation(self, instance):
        return {
            'pension_id': instance.id,
            'pension_nombre': instance.nombre
        }         
        