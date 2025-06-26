from rest_framework import serializers
from contabilidad.models.grupo import ConGrupo

class ConGrupoSerializador(serializers.ModelSerializer):   
    class Meta:
        model = ConGrupo
        fields = ['id', 'nombre', 'codigo']
  
        