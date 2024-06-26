from general.models.item import Item
from rest_framework import serializers

class ItemSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Item
        fields = ['id', 'codigo', 'nombre', 'referencia', 'costo', 'precio', 'producto', 'servicio', 'inventario', 'existencia', 'disponible']

    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'codigo': instance.codigo,
            'nombre': instance.nombre,
            'referencia': instance.referencia,
            'costo': instance.costo,
            'precio': instance.precio,
            'producto': instance.producto,
            'servicio': instance.servicio,
            'inventario': instance.inventario,
            'existencia': instance.existencia,
            'disponible': instance.disponible,
        } 
    
class ItemListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Item

    def to_representation(self, instance):
        return {
            'item_id': instance.id,            
            'item_nombre': instance.nombre,
        }     
    
class ItemExcelSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'codigo', 'nombre', 'referencia', 'costo', 'precio', 'producto', 'servicio', 'inventario', 'existencia', 'disponible']

    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'codigo': instance.codigo,
            'nombre': instance.nombre,
            'referencia': instance.referencia,
            'costo': instance.costo,
            'precio': instance.precio,
            'producto': instance.producto,
            'servicio': instance.servicio,
            'inventario': instance.inventario,
            'existencia': instance.existencia,
            'disponible': instance.disponible,
        }
     
class ItemListaBuscarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item 
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre            
        }    