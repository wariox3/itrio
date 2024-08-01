from general.models.item import GenItem
from rest_framework import serializers

class GenItemSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = GenItem
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
    
class GenItemListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = GenItem

    def to_representation(self, instance):
        return {
            'item_id': instance.id,            
            'item_nombre': instance.nombre,
        }     
    
class GenItemExcelSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenItem
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
     
class GenItemListaBuscarSerializador(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GenItem 
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'nombre': instance.nombre            
        }    