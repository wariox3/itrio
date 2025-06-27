from general.models.sede import GenSede
from rest_framework import serializers

class GenSedeSerializador(serializers.ModelSerializer):
    grupo__nombre = serializers.SerializerMethodField()
    class Meta:
        model = GenSede
        fields = ['id', 'nombre', 'grupo__nombre']  
        select_related_fields = ['grupo']        

    def get_grupo__nombre(self, obj):
        return obj.grupo.nombre if obj.grupo else '' 