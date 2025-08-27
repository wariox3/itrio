from rest_framework import serializers
from vertical.models.color import VerColor

class VerColorSerializador(serializers.ModelSerializer):

    class Meta:
        model = VerColor
        fields = ['id', 'nombre']
        