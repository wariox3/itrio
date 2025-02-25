from rest_framework import serializers
from inventario.models.existencia import InvExistencia
from inventario.models.almacen import InvAlmacen
from general.models.item import GenItem

class InvExistenciaSerializador(serializers.HyperlinkedModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=GenItem.objects.all())
    almacen = serializers.PrimaryKeyRelatedField(queryset=InvAlmacen.objects.all())
    class Meta:
        model = InvExistencia
        fields = ['id', 'item', 'almacen', 'existencia', 'remision', 'disponible']       
        