from general.models.item import GenItem
from contabilidad.models.cuenta import ConCuenta
from rest_framework import serializers
from decouple import config

class GenItemSerializador(serializers.HyperlinkedModelSerializer):
    cuenta_venta = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all(), default=None, allow_null=True)
    cuenta_compra = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all(), default=None, allow_null=True)
    class Meta:
        model = GenItem
        fields = ['id', 'codigo', 'nombre', 'referencia', 'costo', 'costo_promedio', 'precio', 'producto', 'servicio', 'inventario', 'negativo',
                  'existencia', 'remision', 'disponible',
                  'cuenta_venta', 'cuenta_compra', 'favorito', 'venta', 'inactivo', 'imagen']

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
            'costo_promedio': instance.costo_promedio,
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
            'cuenta_compra_nombre': cuenta_compra_nombre,            
            'imagen': f"https://{config('DO_BUCKET')}.{config('DO_REGION')}.digitaloceanspaces.com/{instance.imagen}" if instance.imagen else None          
        } 
    
class GenItemListaSerializador(serializers.ModelSerializer):          
    imagen = serializers.SerializerMethodField()
    class Meta:
        model = GenItem
        fields = ['id', 
                  'codigo',
                  'nombre',
                  'referencia',
                  'precio',
                  'costo',
                  'costo_promedio',
                  'existencia',
                  'remision',
                  'disponible',
                  'producto',
                  'servicio',
                  'inventario',
                  'negativo',
                  'venta',
                  'favorito',
                  'inactivo',
                  'imagen']
        
    def get_imagen(self, obj):
        if obj.imagen:
            return f"https://{config('DO_BUCKET')}.{config('DO_REGION')}.digitaloceanspaces.com/{obj.imagen}"
        return None       

class GenItemSeleccionarSerializador(serializers.ModelSerializer):
    class Meta:
        model = GenItem
        fields = ['id', 'nombre']

class GenItemInformeExistenciaSerializador(serializers.ModelSerializer):
    class Meta:
        model = GenItem
        fields = ['id', 'nombre', 'codigo', 'referencia', 'precio', 'costo', 'costo_promedio', 'existencia', 'remision', 'disponible']