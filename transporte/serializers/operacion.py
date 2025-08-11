from rest_framework import serializers
from transporte.models.operacion import TteOperacion

class TteOperacionSerializador(serializers.ModelSerializer):    
    ciudad__nombre = serializers.CharField(source='ciudad.nombre', read_only=True, allow_null=True, default=None)
    class Meta:
        model = TteOperacion
        fields = ['id', 'nombre', 'ciudad', 'ciudad__nombre']
        select_related_fields = ['ciudad']          

class TteOpercionSeleccionarSerializador(serializers.ModelSerializer):    
    class Meta:
        model = TteOperacion
        fields = ['id', 'nombre', 'ciudad']
