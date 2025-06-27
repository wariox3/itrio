from rest_framework import serializers
from humano.models.cargo import HumCargo

class HumCargoSeleccionarSerializador(serializers.ModelSerializer):
    class Meta:
        model = HumCargo
        fields = ['id', 'nombre']

class HumCargoListaSerializador(serializers.ModelSerializer):          
    class Meta:
        model = HumCargo
        fields = ['id', 
                  'nombre']

#deprecated
class HumCargoSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = HumCargo
        fields = ['id', 'nombre', 'codigo', 'estado_inactivo']

