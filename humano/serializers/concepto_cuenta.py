from rest_framework import serializers
from humano.models.concepto_cuenta import HumConceptoCuenta
from humano.models.concepto import HumConcepto
from humano.models.tipo_costo import HumTipoCosto
from contabilidad.models.cuenta import ConCuenta

class HumConceptoCuentaSerializador(serializers.HyperlinkedModelSerializer):
    concepto = serializers.PrimaryKeyRelatedField(queryset=HumConcepto.objects.all())
    tipo_costo = serializers.PrimaryKeyRelatedField(queryset=HumTipoCosto.objects.all())
    cuenta = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all())
    
    class Meta:
        model = HumConceptoCuenta
        fields = ['concepto', 'tipo_costo', 'cuenta']

    def to_representation(self, instance):       
        tipo_costo_nombre = ""
        if instance.tipo_costo:
            tipo_costo_nombre = instance.tipo_costo.nombre
        cuenta_nombre = ""
        if instance.cuenta:
            cuenta_nombre = instance.cuenta.nombre
        return {
            'id': instance.id,         
            'concepto_id': instance.concepto_id,
            'tipo_costo_id': instance.tipo_costo_id,
            'tipo_costo_nombre': tipo_costo_nombre,
            'cuenta_id': instance.cuenta_id,
            'cuenta_nombre': cuenta_nombre
        } 
       
        