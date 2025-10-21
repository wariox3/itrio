from rest_framework import serializers
from contabilidad.models.conciliacion import ConConciliacion

class ConConciliacionSerializador(serializers.ModelSerializer): 
    cuenta_banco__nombre = serializers.CharField(source='cuenta_banco.nombre', read_only=True)   
    class Meta:
        model = ConConciliacion
        fields = ['id', 'fecha_desde', 'fecha_hasta', 
                  'cuenta_banco',
                  'cuenta_banco__nombre']  
        select_related_fields = ['cuenta_banco']              
        