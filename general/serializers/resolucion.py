from rest_framework import serializers
from general.models.resolucion import GenResolucion

class GenResolucionSerializador(serializers.ModelSerializer):
    class Meta:
        model = GenResolucion
        fields = ['id', 'prefijo', 'numero', 'consecutivo_desde', 'consecutivo_hasta', 'fecha_desde', 'fecha_hasta', 'venta', 'compra'] 

class GenResolucionSeleccionarSerializar(serializers.ModelSerializer):
    class Meta:
        model = GenResolucion
        fields = ['id', 'numero'] 