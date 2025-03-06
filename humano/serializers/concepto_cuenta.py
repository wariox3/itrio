from rest_framework import serializers
from humano.models.concepto_cuenta import HumConceptoCuenta
from humano.models.concepto import HumConcepto
from contabilidad.models.cuenta import ConCuenta

class HumConceptoCuentaSerializador(serializers.HyperlinkedModelSerializer):
    concepto = serializers.PrimaryKeyRelatedField(queryset=HumConcepto.objects.all())
    cuenta = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all())
    
    class Meta:
        model = HumConceptoCuenta
        fields = ['concepto', 'cuenta']

    def to_representation(self, instance):       
        return {
            'id': instance.id,         
            'concepto_id': instance.concepto_id,
            'cuenta_id': instance.cuenta_id
        } 
       
        