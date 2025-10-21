from rest_framework import serializers
from contabilidad.models.conciliacion_detalle import ConConciliacionDetalle

class ConConciliacionDetalleSerializador(serializers.ModelSerializer):     
    class Meta:
        model = ConConciliacionDetalle
        fields = ['id', 'fecha', 'debito', 'credito', 'detalle', 'estado_conciliado', 
                  'conciliacion', 
                  'cuenta', 
                  'contacto', 
                  'documento']  
        select_related_fields = ['conciliacion', 'cuenta', 'contacto', 'documento']              
        