from general.models.sede import GenSede
from rest_framework import serializers

class GenSedeSerializador(serializers.HyperlinkedModelSerializer):
    grupo__nombre = serializers.CharField(source='grupo.nombre', read_only=True)
    class Meta:
        model = GenSede
        fields = ['id', 'nombre', 'grupo__nombre']  
        select_related_fields = ['grupo']        

  