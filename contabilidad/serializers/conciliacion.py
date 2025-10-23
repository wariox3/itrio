from rest_framework import serializers
from contabilidad.models.conciliacion import ConConciliacion

class ConConciliacionSerializador(serializers.ModelSerializer): 
    cuenta_banco__nombre = serializers.CharField(source='cuenta_banco.nombre', read_only=True)   
    cuenta_banco__cuenta__codigo = serializers.CharField(source='cuenta_banco.cuenta.codigo', read_only=True)   
    cuenta_banco__cuenta__nombre = serializers.CharField(source='cuenta_banco.cuenta.nombre', read_only=True)   
    class Meta:
        model = ConConciliacion
        fields = ['id', 'fecha_desde', 'fecha_hasta', 
                  'cuenta_banco',
                  'cuenta_banco__nombre',
                  'cuenta_banco__cuenta__codigo',
                  'cuenta_banco__cuenta__nombre']  
        select_related_fields = ['cuenta_banco']              
        