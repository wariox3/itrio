from decimal import Decimal
from rest_framework import serializers
from inventario.models.existencia import InvExistencia

class InvExistenciaSerializador(serializers.ModelSerializer):
    item__nombre = serializers.CharField(source='item.nombre', read_only=True)
    almacen__nombre = serializers.CharField(source='almacen.nombre', read_only=True)
    class Meta:
        model = InvExistencia
        fields = ['id', 'existencia', 'remision', 'disponible',
                  'item', 
                  'item__nombre',
                  'almacen',
                  'almacen__nombre',]  
        select_related_fields = ['item','almacen']          

         
        