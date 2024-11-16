from rest_framework import serializers
from ruteo.models.vehiculo import RutVehiculo
from ruteo.models.flota import RutFlota


class RutFlotaSerializador(serializers.HyperlinkedModelSerializer):    
    vehiculo = serializers.PrimaryKeyRelatedField(queryset=RutVehiculo.objects.all())
    class Meta:
        model = RutFlota
        fields = ['id', 'vehiculo']

    def validate(self, data):
        vehiculo_id = data.get('vehiculo') 
        flotas = RutFlota.objects.filter(
            vehiculo_id=vehiculo_id
        )       
        if self.instance:
            flotas = flotas.exclude(pk=self.instance.pk)

        if flotas.exists():            
            raise serializers.ValidationError({
                "vehiculo": "El vehiculo ya está en la flota."
            })
        return data

    def to_representation(self, instance):      
        vehiculo_placa = ""
        vehiculo_capacidad = ""
        if instance.vehiculo:
            vehiculo_placa = instance.vehiculo.placa
            vehiculo_capacidad = instance.vehiculo.capacidad
        return {
            'id': instance.id,  
            'vehiculo_id': instance.vehiculo_id,
            'vehiculo_placa': vehiculo_placa,
            'vehiculo_capacidad': vehiculo_capacidad
        }
    