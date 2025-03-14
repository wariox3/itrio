from general.models.item import GenItem
from contabilidad.models.cuenta import ConCuenta
from rest_framework import serializers

class GenItemSerializador(serializers.HyperlinkedModelSerializer):
    cuenta_venta = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all(), default=None, allow_null=True)
    cuenta_compra = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all(), default=None, allow_null=True)
    class Meta:
        model = GenItem
        fields = ['id', 'codigo', 'nombre', 'referencia', 'costo', 'precio', 'producto', 'servicio', 'inventario', 'negativo',
                  'existencia', 'remision', 'disponible',
                  'cuenta_venta', 'cuenta_compra', 'favorito', 'venta', 'inactivo']

    def to_representation(self, instance):
        cuenta_venta_nombre = ''
        cuenta_venta_codigo = ''
        if instance.cuenta_venta:
            cuenta_venta_nombre = instance.cuenta_venta.nombre
            cuenta_venta_codigo = instance.cuenta_venta.codigo
        cuenta_compra_nombre = ''
        cuenta_compra_codigo = ''
        if instance.cuenta_compra:
            cuenta_compra_nombre = instance.cuenta_compra.nombre
            cuenta_compra_codigo = instance.cuenta_compra.codigo            
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
            'negativo': instance.negativo,
            'favorito': instance.favorito,
            'venta': instance.venta,
            'inactivo': instance.inactivo,
            'existencia': instance.existencia,
            'remision': instance.remision,
            'disponible': instance.disponible,
            'cuenta_venta_id': instance.cuenta_venta_id,
            'cuenta_venta_codigo': cuenta_venta_codigo,
            'cuenta_venta_nombre': cuenta_venta_nombre,
            'cuenta_compra_id': instance.cuenta_compra_id,
            'cuenta_compra_codigo': cuenta_compra_codigo,
            'cuenta_compra_nombre': cuenta_compra_nombre            
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