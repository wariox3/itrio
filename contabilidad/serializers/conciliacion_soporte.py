from rest_framework import serializers
from contabilidad.models.conciliacion_soporte import ConConciliacionSoporte

class ConConciliacionSoporteSerializador(serializers.ModelSerializer):     
    class Meta:
        model = ConConciliacionSoporte
        fields = ['id', 'fecha', 'debito', 'credito', 'detalle', 'estado_conciliado',
                  'conciliacion']  
        select_related_fields = ['conciliacion']              
        