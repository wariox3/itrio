from decimal import Decimal
from rest_framework import serializers
from inventario.models.existencia import InvExistencia
from inventario.models.almacen import InvAlmacen
from general.models.item import GenItem

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

class InvExistenciaInventarioValorizadoSerializador(serializers.ModelSerializer):
    item__nombre = serializers.CharField(source='item.nombre', read_only=True)
    item__costo_promedio = serializers.CharField(source='item.costo_promedio', read_only=True)
    almacen__nombre = serializers.CharField(source='almacen.nombre', read_only=True)
    
    class Meta:
        model = InvExistencia
        fields = ['id', 'existencia', 'remision', 'disponible', 
                  'item', 
                  'item__nombre',
                  'item__costo_promedio',
                  'almacen',
                  'almacen__nombre']
        select_related_fields = ['item','almacen']         

         
        