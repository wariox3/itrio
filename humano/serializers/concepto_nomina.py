from rest_framework import serializers
from humano.models.concepto_nomina import HumConceptoNomina
from humano.models.concepto import HumConcepto

class HumConceptoNominaSerializador(serializers.HyperlinkedModelSerializer):
    concepto = serializers.PrimaryKeyRelatedField(queryset=HumConcepto.objects.all(), default=None, allow_null=True)
    class Meta:
        model = HumConceptoNomina
        fields = ['id', 'nombre', 'concepto']

    def to_representation(self, instance):      
        concepto_nombre = ''
        if instance.concepto:
            concepto_nombre = instance.concepto.nombre
        return {
            'id': instance.id,
            'nombre': instance.nombre,
            'concepto_id': instance.concepto_id,
            'concepto_nombre': concepto_nombre            
        } 

        