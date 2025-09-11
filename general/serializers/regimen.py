from general.models.regimen import GenRegimen
from rest_framework import serializers

class GenRegimenSerializador(serializers.ModelSerializer):
    class Meta:
        model = GenRegimen
        fields = ['id', 'nombre', 'inactivo']  