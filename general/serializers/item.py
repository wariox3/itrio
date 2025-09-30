from general.models.item import GenItem
from contabilidad.models.cuenta import ConCuenta
from rest_framework import serializers
from decouple import config

class GenItemSerializador(serializers.ModelSerializer):
    class Meta:
        model = GenItem
        fields = ['id', 'codigo', 'nombre', 'referencia', 'costo', 'costo_promedio', 'precio', 'producto', 'servicio', 'inventario', 'negativo',
                  'existencia', 'remision', 'disponible', 'favorito', 'venta', 'inactivo', 'imagen',
                  'cuenta_venta', 'cuenta_compra', 'cuenta_costo_venta', 'cuenta_inventario']

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