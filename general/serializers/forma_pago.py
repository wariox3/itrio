from general.models.forma_pago import GenFormaPago
from contabilidad.models.cuenta import ConCuenta
from rest_framework import serializers

class GenFormaPagoListaSerializador(serializers.ModelSerializer):          
    class Meta:
        model = GenFormaPago
        fields = ['id', 
                  'nombre']

class GenFormaPagoSerializador(serializers.HyperlinkedModelSerializer):
    cuenta = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all(), default=None, allow_null=True)
    class Meta:
        model = GenFormaPago
        fields = ['id', 'nombre', 'cuenta']  
        
    def to_representation(self, instance):
        cuenta_codigo = ""
        cuenta_nombre = ""
        if instance.cuenta:
            cuenta_codigo = instance.cuenta.codigo
            cuenta_nombre = instance.cuenta.nombre
        return {
            'id': instance.id,            
            'nombre': instance.nombre,
            'cuenta_id': instance.cuenta_id,
            'cuenta_codigo': cuenta_codigo,
            'cuenta_nombre': cuenta_nombre
        }        
    
class GenFormaPagoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenFormaPago 
        
    def to_representation(self, instance):
        return {
            'forma_pago_id': instance.id,            
            'forma_pago_nombre': instance.nombre
        }     