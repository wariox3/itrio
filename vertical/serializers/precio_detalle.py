from rest_framework import serializers
from vertical.models.precio_detalle import VerPrecioDetalle

class VerPrecioDetalleSerializador(serializers.ModelSerializer):
    ciudad_origen__nombre = serializers.CharField(source='ciudad_origen.nombre', read_only=True, allow_null=True, default=None)
    ciudad_destino__nombre = serializers.CharField(source='ciudad_destino.nombre', read_only=True, allow_null=True, default=None)    
    class Meta:
        model = VerPrecioDetalle
        fields = [  
                    'id', 'empresa', 'contenedor_id', 'schema_name', 'tonelada', 'tonelada_pago',
                    'ciudad_origen',
                    'ciudad_origen_id',
                    'ciudad_origen__nombre',
                    'ciudad_destino',
                    'ciudad_destino_id',
                    'ciudad_destino__nombre'                    
                ]        
        select_related_fields = ['ciudad_origen', 'ciudad_destino']

               
        