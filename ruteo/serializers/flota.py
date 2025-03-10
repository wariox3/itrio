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
        vehiculo_capacidad = 0
        vehiculo_tiempo = 0
        vehiculo_franja_id = ""
        vehiculo_franja_codigo = ""
        if instance.vehiculo:
            vehiculo_placa = instance.vehiculo.placa
            vehiculo_capacidad = instance.vehiculo.capacidad
            vehiculo_tiempo = instance.vehiculo.tiempo
            vehiculo_franja_id = instance.vehiculo.franja_id
            vehiculo_franja_codigo = instance.vehiculo.franja.codigo        

        return {
            'id': instance.id,  
            'vehiculo_id': instance.vehiculo_id,
            'vehiculo_placa': vehiculo_placa,
            'vehiculo_capacidad': vehiculo_capacidad,
            'vehiculo_tiempo': vehiculo_tiempo,
            'vehiculo_franja_id': vehiculo_franja_id,
            'vehiculo_franja_codigo': vehiculo_franja_codigo,
        }
    
